from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django import http
from django.template.loader import get_template
from django.template import Context

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from mycleancity.forms import ContactForm

def error404(request):
    return render(request,'mycleancity/404.html')

class HomePageView(TemplateView):
	template_name = "mycleancity/index.html"

	# def dispatch(self, request, *args, **kwargs):
	# 	if request.user.is_authenticated():
	# 		return HttpResponseRedirect('/challenges')
	# 	return super(HomePageView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(HomePageView, self).get_context_data(**kwargs)
		context['user'] = self.request.user
		
		return context

class AboutPageView(TemplateView):
	template_name = "mycleancity/about.html"

	def get_context_data(self, **kwargs):
		context = super(AboutPageView, self).get_context_data(**kwargs)
		return context

class ContactPageView(FormView):
	template_name = "mycleancity/contact.html"
	success_url = "mycleancity/index.html"
	form_class = ContactForm

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		return self.render_to_response(context)

	def form_valid(self, form):
		name = form.cleaned_data['name']
		email = form.cleaned_data['email']
		subject = "%s - %s" % (name, form.cleaned_data['subject'])
		message = form.cleaned_data['message']

		subject_line, from_email, to = subject, 'zee@hakstudio.com', email
		text_content = message
		html_content = message
		msg = EmailMultiAlternatives(subject_line, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

		return HttpResponseRedirect('/')

class RegisterSuccessView(TemplateView):
	template_name = "users/register_success.html"

	def get_context_data(self, **kwargs):
		context = super(RegisterSuccessView, self).get_context_data(**kwargs)
		return context

class MediaHubPageView(TemplateView):
	template_name = "mycleancity/media_hub.html"

	def get_context_data(self, **kwargs):
		context = super(MediaHubPageView, self).get_context_data(**kwargs)
		return context

class StudentsPageView(TemplateView):
	template_name = "mycleancity/students.html"

	def get_context_data(self, **kwargs):
		context = super(StudentsPageView, self).get_context_data(**kwargs)
		return context

class OrganizationsPageView(TemplateView):
	template_name = "mycleancity/organizations.html"

	def get_context_data(self, **kwargs):
		context = super(OrganizationsPageView, self).get_context_data(**kwargs)
		return context