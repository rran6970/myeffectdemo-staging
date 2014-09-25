import os

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.conf import settings
from django.contrib.auth import authenticate, login, logout, SESSION_KEY
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMessage
from django.core.servers.basehttp import FileWrapper

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django import http

from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import get_template
from django.template import Context

from django.utils.encoding import smart_str

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from users.models import PrelaunchEmails

from mycleancity.forms import ContactForm
from cleanteams.models import CleanTeamLevelTask
from users.forms import PrelaunchEmailsForm

from django.contrib.auth.models import User

def relaunch_signup(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		email = request.POST['email']
		postal_code = request.POST['postal_code']
		school_type = request.POST['school_type']
		ambassador = request.POST['ambassador']
		join = request.POST['join']

		prelaunch_emails = PrelaunchEmails()
		prelaunch_emails.first_name = first_name
		prelaunch_emails.email = email
		prelaunch_emails.postal_code = postal_code
		prelaunch_emails.school_type = school_type
		prelaunch_emails.ambassador = ambassador
		prelaunch_emails.join = join
		prelaunch_emails.save()

def error404(request):
	return render_to_response('mycleancity/404.html')

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

class PrivacyPolicyView(TemplateView):
	template_name = "mycleancity/privacy.html"

	def get_context_data(self, **kwargs):
		context = super(PrivacyPolicyView, self).get_context_data(**kwargs)
		return context

class ContactPageView(FormView):
	template_name = "mycleancity/contact.html"
	success_url = "mycleancity/index.html"
	form_class = ContactForm

	def get_initial(self):
		initial = {}

		if 'subject' in self.request.GET:
			subject = self.request.GET.get('subject','')
			initial['subject'] = subject

		return initial

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		return self.render_to_response(context)

	def form_valid(self, form):
		name = form.cleaned_data['name']
		email = form.cleaned_data['email']
		subject = "%s - %s" % (name, form.cleaned_data['subject'])
		message = form.cleaned_data['message']

		subject_line, from_email, to = subject, email, 'info@mycleancity.org'

		mail = EmailMessage(subject, message, from_email, [to])
		mail.content_subtype = "html"
		mail.send()

		return HttpResponseRedirect('/')

class RegisterSuccessView(TemplateView):
	template_name = "users/register_success.html"

	def get_context_data(self, **kwargs):
		context = super(RegisterSuccessView, self).get_context_data(**kwargs)
		return context

def download_file(request):
	filename = request.GET.get('filename', None)

	filename = "downloadable/%s" % (filename)
	conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
	bucket = conn.get_bucket(settings.AWS_BUCKET)
	k = bucket.get_key(filename)
	url = k.generate_url(6000)

	if request.user.is_active:
		if filename == "downloadable/MCC_welcome_package_FR.pdf" or filename == "downloadable/Welcome_package_cgd.pdf":
			if request.user.profile.has_clean_team():
				if request.user.profile.clean_team_member.clean_team.level.name == "Seedling":
					task = CleanTeamLevelTask.objects.get(name="download_welcome_package")
					request.user.profile.clean_team_member.clean_team.complete_level_task(task)


	# TODO: Fix this so there is a redirect, as well as a link to download
	# return HttpResponseRedirect('/clean-team/level-progress/')
	return HttpResponseRedirect(url)

# Coming from the invite email
def unsubscribe(request):
	return render_to_response('mycleancity/unsubscribe.html', context_instance=RequestContext(request))

@user_passes_test(lambda u: (u.is_staff))
def su(request, username, redirect_url='/members/welcome'):
    su_user = get_object_or_404(User, username=username)
    if su_user.is_active:
        request.session[SESSION_KEY] = su_user.id
        request.session["su_old_id"] = request.user.id
        return HttpResponseRedirect(redirect_url)

def su_exit(request, redirect_url='/admin/'):
	if request.session.get('su_old_id', False):
		request.session[SESSION_KEY] = request.session["su_old_id"]
		return HttpResponseRedirect(redirect_url)

	return HttpResponseRedirect('/')
