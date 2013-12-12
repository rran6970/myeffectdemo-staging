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

from cleanteams.forms import RegisterCleanTeamForm, CreateTeamOrJoinForm, RequestJoinTeamsForm
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

		try:
			ctm = CleanTeamMember.objects.get(user=self.request.user)
		except Exception, e:
			ctm = CleanTeamMember()

		ct = CleanTeam.objects.latest('id')
		ctm.clean_team = ct
		ctm.user = user
		ctm.status = "approved"
		ctm.role = "clean-ambassador"
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

class CreateOrRequest(LoginRequiredMixin, FormView):
	template_name = "cleanteams/create_team_or_join.html"
	form_class = CreateTeamOrJoinForm

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		return self.render_to_response(context)

	def form_valid(self, form):
		if form.cleaned_data['selections'] == 'create-new-team':
			return HttpResponseRedirect('/clean-team/register-clean-team')
		else:
			return HttpResponseRedirect('/clean-team/register-request-join')

	def get_context_data(self, **kwargs):
		context = super(CreateOrRequest, self).get_context_data(**kwargs)
		user = self.request.user

		if user.profile.clean_team_member:
			# TODO: Not working
			if user.profile.clean_team_member.status != "declined" and user.profile.clean_team_member.status != "removed":
				return HttpResponseRedirect('/clean-team/%s' % str(user.profile.clean_team_member.clean_team.id))
		
		context['user'] = self.request.user
		return context

class CleanTeamView(TemplateView):
	template_name = "cleanteams/clean_team_profile.html"	

	def get_object(self):
		return get_object_or_404(User, pk=self.request.user.id)

	def get_context_data(self, **kwargs):
		context = super(CleanTeamView, self).get_context_data(**kwargs)

		if 'ctid' in self.kwargs:
			ctid = self.kwargs['ctid']
			ctms = CleanTeamMember.objects.filter(clean_team_id=ctid)
			
			context['clean_team'] = get_object_or_404(CleanTeam, id=ctid)
			context['ctms'] = ctms

		context['user'] = self.request.user
		return context

class RegisterRequestJoinView(LoginRequiredMixin, FormView):
	template_name = "cleanteams/register_request_join.html"
	form_class = RequestJoinTeamsForm

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		
		return self.render_to_response(context)

	def form_valid(self, form):
		ct = form.cleaned_data['team']

		try:
			ctm = CleanTeamMember.objects.get(user=self.request.user)
		except Exception, e:
			ctm = CleanTeamMember()

		if not ctm.has_max_clean_ambassadors:
			ctm.request_join_clean_team(request.user, ct)
		else:
			#TODO: Message saying that the Clean Team ambassador count is full
			pass

		return HttpResponseRedirect('/')

	def get_context_data(self, **kwargs):
		context = super(RegisterRequestJoinView, self).get_context_data(**kwargs)
		user = self.request.user
		
		context['user'] = user

		return context

class RegisterCleanChampionView(LoginRequiredMixin, FormView):
	template_name = "cleanteams/register_clean_champion.html"
	form_class = RequestJoinTeamsForm

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		
		return self.render_to_response(context)

	def form_valid(self, form):
		selected_team = form.cleaned_data['team']

		try:
			clean_team_member = CleanTeamMember.objects.get(user=self.request.user)
		except Exception, e:
			clean_team_member = CleanTeamMember()

		clean_team_member.user = self.request.user
		clean_team_member.clean_team = selected_team
		clean_team_member.status = "approved"
		clean_team_member.role = "clean-champion"
		clean_team_member.save()

		self.request.user.profile.clean_team_member = CleanTeamMember.objects.latest('id')
		self.request.user.profile.save()

		return HttpResponseRedirect('/')

	def get_context_data(self, **kwargs):
		context = super(RegisterCleanChampionView, self).get_context_data(**kwargs)
		user = self.request.user
		
		context['user'] = user

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
		
		# TODO: HttpResponseRedirect is not working
		# Check if approved Clean Ambassador
		if ct.role != "clean-ambassador" or ct.status != "approved":
			print "kkkkk"
			return HttpResponseRedirect("/challenges")

		context['user'] = user
		context['clean_team'] = ct.clean_team
		context['clean_team_members'] = ctm

		return context

# On the Clean Team's Profile
def request_join_clean_team(request):
	if request.method == 'POST':
		ctid = request.POST['ctid']

		ct = get_object_or_404(CleanTeam, id=ctid)
		
		try:
			ctm = CleanTeamMember.objects.get(user=self.request.user)
		except Exception, e:
			ctm = CleanTeamMember()

		if not ctm.has_max_clean_ambassadors:
			ctm.request_join_clean_team(request.user, ct)
		else:
			#TODO: Message saying that the Clean Team ambassador count is full
			pass

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