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

from django.views.generic import *
from django.views.generic.base import View
from django.views.generic.edit import FormView

from cleanteams.forms import RegisterCleanTeamForm
from cleanteams.models import CleanTeam, CleanTeamMember

from mycleancity.mixins import LoginRequiredMixin

class RegisterCleanTeamView(LoginRequiredMixin, FormView):
	template_name = "cleanteams/register_clean_team.html"
	form_class = RegisterCleanTeamForm
	success_url = "mycleancity/index.html"

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		return self.render_to_response(context)

	def form_valid(self, form):
		user = self.request.user
		logo = form.cleaned_data['logo']

		conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
		bucket = conn.get_bucket(settings.AWS_BUCKET)
		k = Key(bucket)
		k.key = 'uploads/ct_logo_%s' % str(user.id)
		k.set_contents_from_string(form.cleaned_data['logo'].read())

		ct = CleanTeam()
		ct.user = user
		ct.name = form.cleaned_data['name']
		ct.website = form.cleaned_data['website']
		ct.logo = k.key
		ct.save()

		ct = CleanTeam.objects.latest('id')
		ctm = CleanTeamMember()
		ctm.clean_team = ct
		ctm.user = user
		ctm.save()

		user.profile.clean_team_member = ctm
		user.profile.save()

		# Send registration email to user
		template = get_template('emails/organization_register_success.html')
		content = Context({ 'email': user.email, 'first_name': user.first_name })
		content = template.render(content)

		subject, from_email, to = 'My Clean City - Clean Team Signup Successful', 'info@mycleancity.org', user.email

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		mail.send()

		# Send notification email to administrator
		template = get_template('emails/register_email_notification.html')
		content = Context({ 'email': user.email })
		content = template.render(content)

		subject, from_email, to = 'My Clean City - Clean Team Signup Successful', 'info@mycleancity.org', 'partner@mycleancity.org'

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		mail.send()

		return HttpResponseRedirect('/')

class CleamTeamView(TemplateView):
	template_name = "cleanteams/clean_team_profile.html"	

	def get_object(self):
		return get_object_or_404(User, pk=self.request.user.id)

	def get_context_data(self, **kwargs):
		context = super(CleamTeamView, self).get_context_data(**kwargs)

		if 'ctid' in self.kwargs:
			ctid = self.kwargs['ctid']

			context['clean_team'] = get_object_or_404(CleanTeam, id=ctid)

		context['user'] = self.request.user
		return context

class CleanTeamMembersView(LoginRequiredMixin, TemplateView):
	template_name = "cleanteams/clean_team_members.html"	

	def get_object(self):
		return get_object_or_404(User, pk=self.request.user.id)

	def get_context_data(self, **kwargs):
		context = super(CleanTeamMembersView, self).get_context_data(**kwargs)
		user = self.request.user

		ct = CleanTeamMember.objects.get(user=user)
		ctm = CleanTeamMember.objects.filter(clean_team=ct.clean_team)
		
		context['user'] = user
		context['clean_team'] = ct.clean_team
		context['clean_team_members'] = ctm

		return context

def request_join_clean_team(request):
	if request.method == 'POST':
		ctid = request.POST['ctid']

		ct = get_object_or_404(CleanTeam, id=ctid)
		
		ctm = CleanTeamMember()
		ctm.user = request.user
		ctm.clean_team = ct
		ctm.status = "pending"
		ctm.save()

		request.user.profile.clean_team_member = CleanTeamMember.objects.latest('id')
		request.user.profile.save()

	return HttpResponseRedirect('/clean-team/%s' % str(ctid))

def clean_team_member_action(request):
	if request.method == 'POST' and request.is_ajax:
		ctid = request.POST['ctid']
		uid = request.POST['uid']
		action = request.POST['action']
		
		if action == "approve":
			CleanTeamMember.objects.filter(clean_team_id=ctid, user_id=uid).update(status="approved")
		elif action == "remove":
			CleanTeamMember.objects.filter(clean_team_id=ctid, user_id=uid).update(status="removed")
			
	return HttpResponse("success")