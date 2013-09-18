from django.contrib.auth import authenticate, login, logout, SESSION_KEY
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from users.forms import PrelaunchEmailsForm, LoginUserForm, RegisterUserForm
from users.models import UserProfile

class PrelaunchView(FormView):
	template_name = "mycleancity/index.html"	
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
		u.save()

		dob = form.cleaned_data['dob']

		#Create User Profile
		try:
			p = UserProfile(dob=dob, clean_creds=0, user=u)
			p.save()
		except Exception, e:
			print e

		user = authenticate(username=u.username, password=form.cleaned_data['password'])

		return super(RegisterView, self).form_valid(form)

class LoginView(FormView):
	template_name = "users/login.html"
	form_class = LoginUserForm
	success_url = "mycleancity/index.html"

	def form_valid(self, form):
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']

		user = authenticate(username=email, password=password)
		return super(LoginView, self).form_valid(form)

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		return self.render_to_response(context)