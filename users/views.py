from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from mycleancity.mixins import LoginRequiredMixin

from users.forms import PrelaunchEmailsForm, RegisterUserForm, ProfileForm
from userprofile.models import UserProfile

class LoginPageView(TemplateView):
	template_name = "users/login.html"

	def get_context_data(self, **kwargs):
		context = super(LoginPageView, self).get_context_data(**kwargs)
		return context

def auth_view(request):
	email = request.POST.get('email', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=email, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/users/loggedin')
	else:
		return HttpResponseRedirect('/users/invalid')

@login_required(login_url='/users/login')
def loggedin(request):
	return render_to_response('users/loggedin.html',
							 {'full_name' : request.user.username})

def invalid_login(request):
	return render_to_response('users/invalid_login.html')

def logout(request):
	auth.logout(request)
	return render_to_response('users/logout.html')

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
		# return super(PrelaunchView, self).form_valid(form)
		return HttpResponseRedirect(self.get_success_url())
		

	# def get_context_data(self, **kwargs):
	# 	context = super(PrelaunchView, self).get_context_data(**kwargs)
	# 	context['success'] = True
	# 	return context

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
		u.profile.save()
		u.save()

		user = auth.authenticate(username=u.username, password=form.cleaned_data['password'])
		auth.login(self.request, user)
		return HttpResponseRedirect('/users/loggedin')

class ProfileView(LoginRequiredMixin, FormView):
	template_name = "users/profile.html"
	form_class = ProfileForm
	success_url = "/users/profile"

	def get_initial(self):
		user = User.objects.get(id=self.request.user.id)

		initial = {}
		initial['first_name'] = user.first_name
		initial['last_name'] = user.last_name
		initial['email'] = user.email
		initial['organization'] = user.profile.organization
		initial['dob'] = user.profile.dob

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
		user_profile = UserProfile.objects.get(user=user)

		user.first_name = form.cleaned_data['first_name']
		user.last_name = form.cleaned_data['last_name']
		user.save()

		user_profile.dob = form.cleaned_data['dob'] 
		user_profile.organization = form.cleaned_data['organization'] 
		user_profile.save()

		return super(ProfileView, self).form_valid(form)