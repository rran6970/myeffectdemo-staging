import urllib
import ftplib
import os
import tempfile

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from challenges.models import Challenge

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

from cleanteams.models import CleanChampion, CleanTeamMember, CleanTeamInvite

from users.forms import PrelaunchEmailsForm, RegisterUserForm, ProfileForm, OrganizationProfileForm
from userprofile.models import UserProfile, QRCodeSignups
from userorganization.models import UserOrganization

def upload(ftp, file):
	ext = os.path.splitext(file)[1]
	
	if ext in (".txt", ".htm", ".html", ".jpeg", ".jpg", ".png"):
		ftp.storlines("STOR " + file, open(file))
	else:
		ftp.storbinary("STOR " + file, open(file, "rb"), 1024)

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
		feb_24 = date(2014, 02, 24)

		if today <= feb_24:
			u.profile.add_clean_creds(50)

		if 'qrcode' in self.kwargs:
			qr_code_signup = QRCodeSignups()
			qr_code_signup.user = User.objects.latest('id')
			qr_code_signup.save()

		user = auth.authenticate(username=u.username, password=form.cleaned_data['password'])
		auth.login(self.request, user)

		# Send registration email to user
		template = get_template('emails/user_register_success.html')
		content = Context({ 'first_name': form.cleaned_data['first_name'] })
		content = template.render(content)

		subject, from_email, to = 'My Clean City - Signup Successful', 'info@mycleancity.org', form.cleaned_data['email']

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		mail.send()

		# Send notification email to administrator
		template = get_template('emails/register_email_notification.html')
		content = Context({ 'email': form.cleaned_data['email'], 'first_name': form.cleaned_data['first_name'], 'last_name': form.cleaned_data['last_name'], 'student': 'student' })
		content = template.render(content)

		subject, from_email, to = 'My Clean City - Student Signup Successful', 'info@mycleancity.org', 'communications@mycleancity.org'

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		mail.send()

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

		invite = CleanTeamInvite.objects.get(token=form.cleaned_data['token'])
		
		if invite.role == "clean-champion":
			clean_champion = CleanChampion()				
			clean_champion.becomeCleanChampion(u, invite.clean_team)

		elif invite.role == "clean-ambassador":
			ctm = CleanTeamMember()
			ctm.user = u
			ctm.clean_team = invite.clean_team
			ctm.role = invite.role
			ctm.status = "approved"
			ctm.save()

			u.profile.clean_team_member = CleanTeamMember.objects.latest('id')
			u.profile.save()

		invite.acceptInvite()
		invite.save()

		user = auth.authenticate(username=u.username, password=form.cleaned_data['password'])
		auth.login(self.request, user)

		# Send registration email to user
		template = get_template('emails/user_register_success.html')
		content = Context({ 'first_name': form.cleaned_data['first_name'] })
		content = template.render(content)

		subject, from_email, to = 'My Clean City - Signup Successful', 'info@mycleancity.org', form.cleaned_data['email']

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		mail.send()

		# Send notification email to administrator
		template = get_template('emails/register_email_notification.html')
		content = Context({ 'email': form.cleaned_data['email'], 'first_name': form.cleaned_data['first_name'], 'last_name': form.cleaned_data['last_name'], 'student': 'student' })
		content = template.render(content)

		subject, from_email, to = 'My Clean City - Student Signup Successful', 'info@mycleancity.org', 'communications@mycleancity.org'

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		mail.send()

		return HttpResponseRedirect('/')

class ProfilePublicView(LoginRequiredMixin, TemplateView):
	template_name = "users/public_profile.html"

	def get_context_data(self, **kwargs):
		context = super(ProfilePublicView, self).get_context_data(**kwargs)
		
		if 'uid' in self.kwargs:
			user_id = self.kwargs['uid']

			try:
				context['organization'] = UserOrganization.objects.get(user_id=user_id)
			except Exception, e:
				print e
				pass

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

		try:
			organization = UserOrganization.objects.get(user=self.request.user)
		except Exception, e:
			print e
			organization = None

		if organization:
			return HttpResponseRedirect('/users/organization-profile')

		return self.render_to_response(self.get_context_data(form=form))

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		return self.render_to_response(context)

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		user = User.objects.get(id=self.request.user.id)
		picture = form.cleaned_data['picture']

		user.first_name = form.cleaned_data['first_name']
		user.last_name = form.cleaned_data['last_name']
		user.save()

		# user.profile.dob = form.cleaned_data['dob']
		user.profile.about = form.cleaned_data['about']
		user.profile.twitter = form.cleaned_data['twitter']

		# TODO: Move to models
		if picture:			
			conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
			bucket = conn.get_bucket(settings.AWS_BUCKET)
			k = Key(bucket)
			k.key = 'uploads/user_picture_%s_%s' % (str(user.id), picture)
			k.set_contents_from_string(form.cleaned_data['picture'].read())
			user.profile.picture = k.key

		user.profile.save()

		return HttpResponseRedirect('/users/profile/%s' % str(user.id))

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
