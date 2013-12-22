import urllib
import ftplib
import os
import tempfile

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from challenges.models import Challenge

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

from users.forms import PrelaunchEmailsForm, RegisterUserForm, ProfileForm, OrganizationProfileForm
from userprofile.models import UserProfile
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

		# if self.request.user.is_authenticated():
		# 	return HttpResponseRedirect('/challenges')
		# else:
		# 	print "uu"

		if 'next' in self.kwargs:
			next_url = urllib.quote(self.kwargs['next'])
			context['next'] = next_url
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
		u.profile.school_type = form.cleaned_data['school_type']
		u.profile.save()
		u.save()

		user = auth.authenticate(username=u.username, password=form.cleaned_data['password'])
		auth.login(self.request, user)

		# Send registration email to user
		template = get_template('emails/user_register_success.html')
		content = Context({ 'first_name': form.cleaned_data['first_name'] })
		content = template.render(content)

		subject, from_email, to = 'My Clean City - Signup Successful', 'info@mycleancity.org', form.cleaned_data['email']

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		# mail.send()

		# Send notification email to administrator
		template = get_template('emails/register_email_notification.html')
		content = Context({ 'email': form.cleaned_data['email'], 'first_name': form.cleaned_data['first_name'], 'last_name': form.cleaned_data['last_name'], 'student': 'student' })
		content = template.render(content)

		subject, from_email, to = 'My Clean City - Student Signup Successful', 'info@mycleancity.org', 'communications@mycleancity.org'

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		# mail.send()

		if form.cleaned_data['role'] == "clean-ambassador":
			return HttpResponseRedirect('/clean-team/create-or-request/')
		elif form.cleaned_data['role'] == "clean-champion":
			return HttpResponseRedirect('/clean-team/register-clean-champion/')

		return HttpResponseRedirect('/challenges')

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
		# initial['dob'] = user.profile.dob
		initial['school_type'] = user.profile.school_type
		initial['about'] = user.profile.about

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

		user.first_name = form.cleaned_data['first_name']
		user.last_name = form.cleaned_data['last_name']
		user.save()

		# user.profile.dob = form.cleaned_data['dob']
		user.profile.about = form.cleaned_data['about']
		user.profile.school_type = form.cleaned_data['school_type'] 
		user.profile.save()

		return HttpResponseRedirect('/users/profile/%s' % str(user.id))

class OrganizationProfileView(LoginRequiredMixin, FormView):
	template_name = "users/organization_profile.html"
	form_class = OrganizationProfileForm
	success_url = "/users/organization-profile"

	def get_initial(self):
		user = self.request.user

		try:
			organization = UserOrganization.objects.get(user=self.request.user)
		except Exception, e:
			print e
			organization = None	

		initial = {}
		initial['first_name'] = user.first_name
		initial['last_name'] = user.last_name
		initial['email'] = user.email
		initial['organization'] = organization.organization
		initial['city'] = user.profile.city
		initial['province'] = user.profile.province
		initial['website'] = organization.website
		initial['about'] = user.profile.about

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
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.

		user = User.objects.get(id=self.request.user.id)
		user_organization = UserOrganization.objects.get(user=user)

		user.first_name = form.cleaned_data['first_name']
		user.last_name = form.cleaned_data['last_name']
		user.email = form.cleaned_data['email']
		user.save()

		user.profile.about = form.cleaned_data['about']
		user.profile.city = form.cleaned_data['city']
		user.profile.province = form.cleaned_data['province']
		user.profile.save()

		user_organization.organization = form.cleaned_data['organization']
		user_organization.website = form.cleaned_data['website']
		user_organization.save()

		return HttpResponseRedirect('/users/profile/%s' % str(user.id))

		# return super(OrganizationProfileView, self).form_valid(form)

# class OrganizationProfilePublicView(TemplateView):
# 	template_name = "users/organization_profile_public.html"

# 	def get_context_data(self, **kwargs):
# 		context = super(OrganizationProfilePublicView, self).get_context_data(**kwargs)

# 		if 'uid' in self.kwargs:
# 			user_id = self.kwargs['uid']
# 			context['organization'] = get_object_or_404(User, id=user_id)
# 			context['challenges'] = Challenge.objects.filter(user_id=user_id)

# 		context['user'] = self.request.user
# 		return context

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