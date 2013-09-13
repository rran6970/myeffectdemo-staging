from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from users.forms import PrelaunchEmailsForm, LoginUserForm, RegisterUserForm
from users.models import UserProfile

class PrelaunchView(FormView):
	template_name = "mycleancity/index.html"
	form_class = PrelaunchEmailsForm
	success_url = "mycleancity/index.html"

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		form.save()
		return super(PrelaunchView, self).form_valid(form)

class RegisterView(FormView):
	template_name = "users/register.html"
	form_class = RegisterUserForm
	success_url = "mycleancity/index.html"

	def form_valid(self, form):
		print "valid"

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

		#Create User Profile
		try:
			p = UserProfile(user=u)
			p.save()
		except Exception:
			print e

		user = authenticate(username=u.username, password=form.cleaned_data['password'])

		return super(RegisterView, self).form_valid(form)

class LoginView(FormView):
	template_name = "users/login.html"
	form_class = LoginUserForm
	success_url = "mycleancity/index.html"

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		form.save()
		return super(LoginView, self).form_valid(form)