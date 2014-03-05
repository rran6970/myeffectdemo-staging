import urllib
import ftplib
import os
import tempfile

from challenges.models import Challenge
from cleanteams.models import CleanChampion, CleanTeamMember, CleanTeamInvite

from datetime import date

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from mycleancity.mixins import LoginRequiredMixin
from mycleancity.actions import *

from users.forms import PrelaunchEmailsForm, RegisterUserForm, ProfileForm, SettingsForm
from userprofile.models import UserSettings, UserProfile, QRCodeSignups, UserQRCode

class LoginPageView(TemplateView):
	template_name = "users/login.html"

	def get_context_data(self, **kwargs):
		context = super(LoginPageView, self).get_context_data(**kwargs)

		if 'next' in self.request.GET:
			next_url = urllib.quote(self.request.GET['next'])
			print next_url
			context['next_url'] = next_url
		else:
			print "not there"
			
		return context

def auth_view(request):
	c = {}
	email = request.POST.get('email', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=email, password=password)
	next_url = None

	if 'next' in request.GET:
		next_url = urllib.quote(request.GET['next'])

	if user is not None:
		auth.login(request, user)

		if next_url:
			return HttpResponseRedirect(urllib.unquote(next_url))
		else:
			return HttpResponseRedirect('/')
	else:
		c['invalid'] = True
	
	c['next_url'] = next_url
	c.update(csrf(request))
	return render_to_response('users/login.html', c, context_instance=RequestContext(request))

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

def register_success(request):
	return render_to_response('register_success.html')

class PrelaunchView(FormView):
	template_name = "mycleancity/landing.html"	
	success_url = "/success"
	form_class = PrelaunchEmailsForm

	def get(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		return self.render_to_response(self.get_context_data(form=form))

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form, **kwargs)

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		return self.render_to_response(context)

	def form_valid(self, form):
		form.save()

		return HttpResponseRedirect(self.get_success_url())
		
class RegisterView(FormView):
	template_name = "users/register.html"
	form_class = RegisterUserForm
	success_url = "mycleancity/index.html"

	def get_initial(self):
		initial = {}
		initial['role'] = 'individual'

		return initial

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		return self.render_to_response(context)

	def form_valid(self, form):
		u = User.objects.create_user(
	        form.cleaned_data['email'],
	        form.cleaned_data['email'],
	        form.cleaned_data['password']
	    )
		u.first_name = form.cleaned_data['first_name']
		u.last_name = form.cleaned_data['last_name']
		u.profile.city = form.cleaned_data['city']
		u.profile.province = form.cleaned_data['province']
		u.profile.age = form.cleaned_data['age']
		u.profile.smartphone = form.cleaned_data['smartphone']
		u.profile.hear_about_us = form.cleaned_data['hear_about_us']
		u.profile.settings.communication_language = form.cleaned_data['communication_language']
		u.profile.settings.save()
		u.profile.save()
		u.save()

		today = date.today()
		early_bird_date = date(2014, 03, 19)

		if today <= early_bird_date:
			u.profile.add_clean_creds(50)

		if 'qrcode' in self.kwargs:
			qr_code_signup = QRCodeSignups()
			qr_code_signup.user = User.objects.latest('id')
			qr_code_signup.save()

		user = auth.authenticate(username=u.username, password=form.cleaned_data['password'])
		auth.login(self.request, user)

		lang = u.profile.settings.communication_language
		
		# Send registration email to user
		if lang == "English":
			template = get_template('emails/user_register_success.html')
			subject = 'My Clean City - Signup Successful'
		else:
			template = get_template('emails/french/user_register_success_fr.html')
			subject = 'My Clean City - Signup Successful'
		
		content = Context({ 'first_name': form.cleaned_data['first_name'] })

		from_email, to = 'info@mycleancity.org', form.cleaned_data['email']

		send_email = SendEmail()
		send_email.send(template, content, subject, from_email, to)


		# Send notification email to administrator
		template = get_template('emails/register_email_notification.html')
		content = Context({ 'email': form.cleaned_data['email'], 'first_name': form.cleaned_data['first_name'], 'last_name': form.cleaned_data['last_name'], 'student': 'student' })

		subject, from_email, to = 'My Clean City - Student Signup Successful', 'info@mycleancity.org', 'communications@mycleancity.org'

		send_email = SendEmail()
		send_email.send(template, content, subject, from_email, to)

		if form.cleaned_data['role'] == "clean-ambassador":
			return HttpResponseRedirect('/clean-team/create-or-request/')
		elif form.cleaned_data['role'] == "clean-champion":
			return HttpResponseRedirect('/clean-team/register-clean-champion/')

		return HttpResponseRedirect('/')


	def get_context_data(self, **kwargs):
		context = super(RegisterView, self).get_context_data(**kwargs)

		if 'qrcode' in self.kwargs:
			context['popup'] = True
	
		context['page_url'] = self.request.get_full_path()
		context['user'] = self.request.user

		return context	

# TODO: Pretty much a copy and paste of RegisterView,
# find a more efficient way of doing this.
class RegisterInviteView(FormView):
	template_name = "users/register.html"
	form_class = RegisterUserForm
	success_url = "mycleancity/index.html"

	def get_initial(self):
		if 'token' in self.kwargs:
			token = self.kwargs['token']
		else:
			return HttpResponseRedirect('/register/')

		invite = CleanTeamInvite.objects.get(token=token)

		# TODO: Need to make the fields read-only
		initial = {}
		initial['email'] = invite.email
		initial['role'] = invite.role
		initial['token'] = invite.token

		return initial

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		return self.render_to_response(context)

	def form_valid(self, form):
		u = User.objects.create_user(
	        form.cleaned_data['email'],
	        form.cleaned_data['email'],
	        form.cleaned_data['password']
	    )
		u.first_name = form.cleaned_data['first_name']
		u.last_name = form.cleaned_data['last_name']
		u.profile.city = form.cleaned_data['city']
		u.profile.province = form.cleaned_data['province']
		u.profile.age = form.cleaned_data['age']
		u.profile.smartphone = form.cleaned_data['smartphone']
		u.profile.hear_about_us = form.cleaned_data['hear_about_us']
		u.profile.save()
		u.save()	

		today = date.today()
		early_bird_date = date(2014, 03, 19)

		if today <= early_bird_date:
			u.profile.add_clean_creds(50)

		invite = CleanTeamInvite.objects.get(token=form.cleaned_data['token'])
		
		invite.acceptInvite(u)
		invite.save()

		user = auth.authenticate(username=u.username, password=form.cleaned_data['password'])
		auth.login(self.request, user)

		lang = u.profile.settings.communication_language
		
		# Send registration email to user
		if lang == "English":
			template = get_template('emails/user_register_success.html')
			subject = 'My Clean City - Signup Successful'
		else:
			template = get_template('emails/french/user_register_success_fr.html')
			subject = 'My Clean City - Signup Successful'
		
		content = Context({ 'first_name': form.cleaned_data['first_name'] })

		from_email, to = 'info@mycleancity.org', form.cleaned_data['email']

		send_email = SendEmail()
		send_email.send(template, content, subject, from_email, to)


		# Send notification email to administrator
		template = get_template('emails/register_email_notification.html')
		content = Context({ 'email': form.cleaned_data['email'], 'first_name': form.cleaned_data['first_name'], 'last_name': form.cleaned_data['last_name'], 'student': 'student' })

		subject, from_email, to = 'My Clean City - Student Signup Successful', 'info@mycleancity.org', 'communications@mycleancity.org'

		send_email = SendEmail()
		send_email.send(template, content, subject, from_email, to)


		return HttpResponseRedirect('/')

class ProfilePublicView(LoginRequiredMixin, TemplateView):
	template_name = "users/public_profile.html"

	def get_context_data(self, **kwargs):
		context = super(ProfilePublicView, self).get_context_data(**kwargs)
		
		if 'uid' in self.kwargs:
			user_id = self.kwargs['uid']

			context['clean_champion_clean_teams'] = CleanChampion.objects.filter(user_id=user_id)
			context['challenges'] = Challenge.objects.filter(user_id=user_id)
			context['user_profile'] = get_object_or_404(User, id=user_id)

		context['user'] = self.request.user
		return context

class ProfileView(LoginRequiredMixin, FormView):
	template_name = "users/profile.html"
	form_class = ProfileForm
	success_url = "/users/profile"

	def get_initial(self):
		user = self.request.user

		initial = {}
		initial['first_name'] = user.first_name
		initial['last_name'] = user.last_name
		initial['email'] = user.email
		initial['about'] = user.profile.about

		if user.profile.twitter:
			initial['twitter'] = user.profile.twitter

		return initial

	def get(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		return self.render_to_response(self.get_context_data(form=form))

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		return self.render_to_response(context)

	def form_valid(self, form):
		user = User.objects.get(id=self.request.user.id)
		picture = form.cleaned_data['picture']

		user.first_name = form.cleaned_data['first_name']
		user.last_name = form.cleaned_data['last_name']
		user.save()

		# user.profile.dob = form.cleaned_data['dob']
		user.profile.about = form.cleaned_data['about']
		user.profile.twitter = form.cleaned_data['twitter']

		if picture:		
			key = 'uploads/user_picture_%s_%s' % (str(user.id), picture)
			uploadFile = UploadFileToS3()
			user.profile.picture = uploadFile.upload(key, picture)

		user.profile.save()

		return HttpResponseRedirect('/users/profile/%s' % str(user.id))

class SettingsView(LoginRequiredMixin, FormView):
	template_name = "users/settings.html"
	form_class = SettingsForm
	success_url = "/users/settings"

	def get_initial(self):
		settings = self.request.user.profile.settings

		initial = {}
		initial['communication_language'] = settings.communication_language
		initial['email_privacy'] = settings.email_privacy

		return initial

	def get(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		return self.render_to_response(self.get_context_data(form=form))

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		return self.render_to_response(context)

	def form_valid(self, form, **kwargs):
		user = self.request.user

		if form.cleaned_data['email_privacy'] == "True":
			user.profile.settings.email_privacy = 1
		else:
			user.profile.settings.email_privacy = 0

		user.profile.settings.communication_language = form.cleaned_data['communication_language']
		user.profile.settings.save()

		context = self.get_context_data(**kwargs)
		context['form'] = form

		return HttpResponseRedirect('/users/profile/%s' % str(user.id))

class QRCodeView(TemplateView):
	template_name = "users/qr_code.html"

	def get_context_data(self, **kwargs):
		context = super(QRCodeView, self).get_context_data(**kwargs)
			
		context['qr_code'] = UserQRCode.objects.get(user=self.request.user)

		return context

class LeaderboardView(TemplateView):
	template_name = "users/leaderboard.html"
	
	def get_context_data(self, **kwargs):
		context = super(LeaderboardView, self).get_context_data(**kwargs)

		leaders = UserProfile.objects.filter(clean_creds__gte=1).order_by('-clean_creds')[:8]
		user_profile = None

		if self.request.user.is_authenticated():
			user_profile = UserProfile.objects.get(user=self.request.user)

		context['user_profile'] = user_profile
		context['leaders'] = leaders
		context['user'] = self.request.user
		return context
