import urllib
import ftplib
import os
import tempfile

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.mail import EmailMessage

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.views.generic.edit import FormView

from userorganization.forms import RegisterOrganizationForm
from userorganization.models import UserOrganization

class RegisterOrganizationView(FormView):
	template_name = "users/register_organization.html"
	form_class = RegisterOrganizationForm
	success_url = "mycleancity/index.html"

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
		u.is_active = False
		u.profile.city = form.cleaned_data['city']
		u.profile.province = form.cleaned_data['province']
		u.profile.save()
		u.save()

		logo = form.cleaned_data['logo']


		conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
		bucket = conn.get_bucket(settings.AWS_BUCKET)
		k = Key(bucket)
		k.key = 'uploads/organization_logo_%s' % str(u.id)
		k.set_contents_from_string(form.cleaned_data['logo'].read())

		o = UserOrganization(user=u)
		o.organization = form.cleaned_data['organization']
		o.website = form.cleaned_data['website']
		o.logo = k.key
		o.save()	

		# Send registration email to user
		template = get_template('emails/organization_register_success.html')
		content = Context({ 'email': form.cleaned_data['email'], 'first_name': form.cleaned_data['first_name'], 'last_name': form.cleaned_data['last_name'] })
		content = template.render(content)

		subject, from_email, to = 'My Effect - Signup Successful', 'info@mycleancity.org', form.cleaned_data['email']

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		mail.send()

		# Send notification email to administrator
		template = get_template('emails/register_email_notification.html')
		content = Context({ 'email': form.cleaned_data['email'] })
		content = template.render(content)

		subject, from_email, to = 'My Effect - Organization Signup Successful', 'info@mycleancity.org', 'partner@mycleancity.org'

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		# mail.attach(logo.name, logo.read(), logo.content_type)
		mail.send()

		return HttpResponseRedirect('/register-success/')