import urllib

from challenges.models import Challenge

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.mail import EmailMultiAlternatives

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from mycleancity.mixins import LoginRequiredMixin

from users.forms import PrelaunchEmailsForm, RegisterUserForm, RegisterOrganizationForm, ProfileForm, OrganizationProfileForm
from userprofile.models import UserProfile
from userorganization.models import UserOrganization


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
			return HttpResponseRedirect('/challenges/')
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
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		form.save()
		return HttpResponseRedirect(self.get_success_url())
		
class RegisterView(FormView):
	template_name = "users/register.html"
	form_class = RegisterUserForm
	success_url = "mycleancity/index.html"

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		return self.render_to_response(context)

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.

		u = User.objects.create_user(
	        form.cleaned_data['email'],
	        form.cleaned_data['email'],
	        form.cleaned_data['password']
	    )
		u.first_name = form.cleaned_data['first_name']
		u.last_name = form.cleaned_data['last_name']
		u.profile.dob = form.cleaned_data['dob']
		u.profile.school_type = form.cleaned_data['school_type']
		u.profile.ambassador = form.cleaned_data['ambassador']
		u.profile.save()
		u.save()

		user = auth.authenticate(username=u.username, password=form.cleaned_data['password'])
		auth.login(self.request, user)

		# plaintext = get_template('emails/user_register_success.txt')
		# htmly = get_template('emails/user_register_success.html')

		# d = Context({ 'first_name': form.cleaned_data['first_name'] })

		# subject, from_email, to = 'My Clean City - Sign Successful', 'zee@hakstudio.com', form.cleaned_data['email']
		# text_content = plaintext.render(d)
		# html_content = htmly.render(d)
		# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		# msg.attach_alternative(html_content, "text/html")
		# msg.send()

		return HttpResponseRedirect('/challenges')

class RegisterOrganizationView(FormView):
	template_name = "users/register_organization.html"
	form_class = RegisterOrganizationForm
	success_url = "mycleancity/index.html"

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		return self.render_to_response(context)

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.

		u = User.objects.create_user(
	        form.cleaned_data['email'],
	        form.cleaned_data['email'],
	        form.cleaned_data['password']
	    )
		u.first_name = form.cleaned_data['first_name']
		u.last_name = form.cleaned_data['last_name']
		u.is_active = False
		u.save()

		o = UserOrganization(user=u)
		o.organization = form.cleaned_data['organization']
		o.city = form.cleaned_data['city']
		o.province = form.cleaned_data['province']
		o.website = form.cleaned_data['website']
		o.save()

		# plaintext = get_template('emails/organization_register_success.txt')
		# htmly = get_template('emails/organization_register_success.html')

		# d = Context({ 'first_name': form.cleaned_data['first_name'] })

		# subject, from_email, to = 'My Clean City - Sign Successful', 'zee@hakstudio.com', form.cleaned_data['email']
		# text_content = plaintext.render(d)
		# html_content = htmly.render(d)
		# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		# msg.attach_alternative(html_content, "text/html")
		# msg.send()

		return HttpResponseRedirect('/register-success/')

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
		user.profile.school_type = form.cleaned_data['school_type'] 
		user.profile.save()

		return super(ProfileView, self).form_valid(form)

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
		initial['city'] = organization.city
		initial['province'] = organization.province
		initial['website'] = organization.website

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

		user_organization.organization = form.cleaned_data['organization']
		user_organization.city = form.cleaned_data['city']
		user_organization.province = form.cleaned_data['province']
		user_organization.website = form.cleaned_data['website']
		user_organization.save()

		return super(OrganizationProfileView, self).form_valid(form)

class OrganizationProfilePublicView(TemplateView):
	template_name = "users/organization_profile_public.html"

	def get_context_data(self, **kwargs):
		context = super(OrganizationProfilePublicView, self).get_context_data(**kwargs)

		if 'uid' in self.kwargs:
			user_id = self.kwargs['uid']
			context['organization'] = get_object_or_404(User, id=user_id)
			context['challenges'] = Challenge.objects.filter(user_id=user_id)

		context['user'] = self.request.user
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