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

from cleanteams.forms import RegisterCleanTeamForm, CreateTeamOrJoinForm, RequestJoinTeamsForm, PostMessageForm, JoinTeamCleanChampionForm, InviteForm, InviteResponseForm
from cleanteams.models import CleanTeam, CleanTeamMember, CleanTeamPost, CleanChampion, CleanTeamInvite, CleanTeamLevelTask, CleanTeamLevelProgress
from challenges.models import Challenge

from notifications.models import Notification

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

		ct = CleanTeam()
		ct.user = user
		ct.name = form.cleaned_data['name']
		ct.region = form.cleaned_data['region']
		ct.team_type = form.cleaned_data['team_type']
		ct.group = form.cleaned_data['group']

		# TODO: Move to models
		if logo:
			conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
			bucket = conn.get_bucket(settings.AWS_BUCKET)
			k = Key(bucket)
			k.key = 'uploads/ct_logo_%s_%s' % (str(user.id), logo)
			k.set_contents_from_string(form.cleaned_data['logo'].read())
			ct.logo = k.key

		ct.save()
		ct.level_up()

		try:
			ctm = CleanTeamMember.objects.get(user=self.request.user)
		except Exception, e:
			print e
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
		# mail.send()

		# Send notification email to administrator
		template = get_template('emails/register_email_notification.html')
		content = Context({ 'email': user.email })
		content = template.render(content)

		subject, from_email, to = 'My Clean City - Clean Team Signup Successful', 'info@mycleancity.org', 'partner@mycleancity.org'

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		# mail.send()

		return HttpResponseRedirect('/clean-team/invite/')

class EditCleanTeamView(LoginRequiredMixin, FormView):
	template_name = "cleanteams/edit_clean_team.html"
	form_class = RegisterCleanTeamForm
	success_url = "mycleancity/index.html"

	def get_initial(self):
		if 'ctid' in self.kwargs:
			ctid = self.kwargs['ctid']

		try:
			clean_team = CleanTeam.objects.get(id=ctid)
		except Exception, e:
			print e
			return HttpResponseRedirect(u'/clean-team/%s' %(ctid))

		initial = {}
		initial['name'] = clean_team.name
		initial['website'] = clean_team.website
		initial['twitter'] = clean_team.twitter
		# initial['logo'] = clean_team.logo
		initial['about'] = clean_team.about
		initial['region'] = clean_team.region
		initial['team_type'] = clean_team.team_type
		initial['group'] = clean_team.group
		initial['clean_team_id'] = clean_team.id

		return initial

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		print form.errors

		return self.render_to_response(context)

	def form_valid(self, form):
		clean_team_id = form.cleaned_data['clean_team_id']

		try:
			clean_team_member = CleanTeamMember.objects.get(user=self.request.user)
			clean_team = CleanTeam.objects.get(id=clean_team_member.clean_team.id)
		except Exception, e:
			print e
		
		clean_team.name = form.cleaned_data['name']
		clean_team.website = form.cleaned_data['website']
		clean_team.twitter = form.cleaned_data['twitter']
		clean_team.about = form.cleaned_data['about']
		clean_team.region = form.cleaned_data['region']
		clean_team.team_type = form.cleaned_data['team_type']
		
		logo = form.cleaned_data['logo']

		# TODO: Move to models
		if logo:
			conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
			bucket = conn.get_bucket(settings.AWS_BUCKET)
			k = Key(bucket)
			k.key = 'uploads/ct_logo_%s_%s' % (str(self.request.user.id), logo)
			k.set_contents_from_string(form.cleaned_data['logo'].read())
			clean_team.logo = k.key

		clean_team.save()

		if clean_team.level.name == "Seedling":
			if clean_team.about:
				task = CleanTeamLevelTask.objects.get(name="ct_description")
				clean_team.complete_level_task(task)
			else:
				task = CleanTeamLevelTask.objects.get(name="ct_description")
				clean_team.uncomplete_level_task(task)

		if clean_team.level.name == "Seedling":
			if clean_team.twitter:
				task = CleanTeamLevelTask.objects.get(name="ct_twitter")
				clean_team.complete_level_task(task)
			else:
				task = CleanTeamLevelTask.objects.get(name="ct_twitter")
				clean_team.uncomplete_level_task(task)

		return HttpResponseRedirect(u'/clean-team/%s' %(clean_team_id))

class CreateOrRequest(LoginRequiredMixin, FormView):
	template_name = "cleanteams/create_team_or_join.html"
	form_class = CreateTeamOrJoinForm

	def get(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		return self.render_to_response(self.get_context_data(form=form))

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

class ViewAllCleanTeams(TemplateView):
	template_name = "cleanteams/all_clean_teams.html"	

	def get_context_data(self, **kwargs):
		context = super(ViewAllCleanTeams, self).get_context_data(**kwargs)

		teams = CleanTeam.objects.all()
		
		if self.request.user.is_authenticated():
			clean_champions = CleanChampion.objects.filter(user=self.request.user)
			context['clean_champions'] = clean_champions

		context['teams'] = teams
		context['user'] = self.request.user

		return context

class LevelProgressView(TemplateView):
	template_name = "cleanteams/level_progress.html"	

	def get_context_data(self, **kwargs):
		context = super(LevelProgressView, self).get_context_data(**kwargs)
		user = self.request.user
		clean_team = user.profile.clean_team_member.clean_team

		level_tasks = CleanTeamLevelTask.objects.filter(clean_team_level=clean_team.level)
		tasks = CleanTeamLevelProgress.objects.filter(clean_team=clean_team, level_task__in=level_tasks)
	
		context['tasks'] = tasks
		context['clean_team'] = clean_team
		context['user'] = user

		return context

class CleanTeamView(TemplateView):
	template_name = "cleanteams/clean_team_profile.html"	

	def get_object(self):
		return get_object_or_404(User, pk=self.request.user.id)

	def get_context_data(self, **kwargs):
		context = super(CleanTeamView, self).get_context_data(**kwargs)

		if 'ctid' in self.kwargs:
			ctid = self.kwargs['ctid']
			cas = CleanTeamMember.objects.filter(clean_team_id=ctid)
			ccs = CleanChampion.objects.filter(clean_team_id=ctid)
			posts = CleanTeamPost.objects.filter(clean_team_id=ctid).order_by('-timestamp')

			try:
				clean_champion = CleanChampion.objects.get(clean_team_id=ctid, user=self.request.user)
				context['clean_champion'] = clean_champion
			except Exception, e:
				print e

			try:
				invite = CleanTeamInvite.objects.get(email=self.request.user.email, clean_team_id=ctid)
				context['invite'] = invite
			except Exception, e:
				print e

			try:
				# TODO: Need to pass this to the template
				# context['clean_ambassador']
				clean_ambassador = CleanTeamMember.objects.get(clean_team_id=ctid, user=self.request.user, status="approved", role="clean-ambassador")
			except Exception, e:
				print e

			context['page_url'] = self.request.get_full_path()
			context['clean_team'] = get_object_or_404(CleanTeam, id=ctid)
			context['cas'] = cas
			context['ccs'] = ccs
			context['posts'] = posts
			context['challenges'] = Challenge.objects.filter(clean_team_id=ctid)

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
		try:
			ctm = CleanTeamMember.objects.get(user=self.request.user)
		except Exception, e:
			print e
			ctm = CleanTeamMember()

		selected_team = form.cleaned_data['team']

		# if not ctm.has_max_clean_ambassadors():
		ctm.requestBecomeCleanAmbassador(self.request.user, selected_team)
		# else:
			#TODO: Message saying that the Clean Team ambassador count is full
			# pass

		return HttpResponseRedirect('/')

	def get_context_data(self, **kwargs):
		context = super(RegisterRequestJoinView, self).get_context_data(**kwargs)
		user = self.request.user
		
		context['user'] = user

		return context

class RegisterCleanChampionView(LoginRequiredMixin, FormView):
	template_name = "cleanteams/register_clean_champion.html"
	form_class = JoinTeamCleanChampionForm

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		
		return self.render_to_response(context)

	def form_valid(self, form):
		selected_team = form.cleaned_data['team']

		try:
			clean_champion = CleanChampion.objects.get(user=self.request.user, clean_team=selected_team)
			print clean_champion
		except Exception, e:
			print e
			clean_champion = CleanChampion()

		clean_champion.becomeCleanChampion(self.request.user, selected_team)

		return HttpResponseRedirect('/clean-team/invite/')

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
		cas = CleanTeamMember.objects.filter(clean_team=ct.clean_team)
		ccs = CleanChampion.objects.filter(clean_team=ct.clean_team)
		# ctm = CleanTeamMember.objects.filter(clean_team=ct.clean_team)
		
		# TODO: HttpResponseRedirect is not working
		# Check if approved Clean Ambassador
		if ct.role != "clean-ambassador" or ct.status != "approved":
			print "kkkkk"
			return HttpResponseRedirect("/challenges")

		context['user'] = user
		context['clean_team'] = ct.clean_team
		context['cas'] = cas
		context['ccs'] = ccs
		# context['clean_team_members'] = ctm

		return context

class PostMessageView(LoginRequiredMixin, FormView):
	template_name = "cleanteams/post_message.html"
	form_class = PostMessageForm

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		
		return self.render_to_response(context)

	def form_valid(self, form):
		clean_team = self.request.user.profile.clean_team_member.clean_team

		clean_team_post = CleanTeamPost()
		clean_team_post.newPost(self.request.user, form, clean_team)

		return HttpResponseRedirect('/clean-team/%s' % str(clean_team.id))

	def get_context_data(self, **kwargs):
		context = super(PostMessageView, self).get_context_data(**kwargs)
		user = self.request.user
		
		context['user'] = user

		return context

class InviteView(LoginRequiredMixin, FormView):
	template_name = "cleanteams/invite.html"
	form_class = InviteForm
	success_url = "cleanteams/invite.html"

	def get_initial(self):
		initial = {}
		initial['clean_team_id'] = self.request.user.profile.clean_team_member.clean_team.id

		return initial

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		return self.render_to_response(context)

	def form_valid(self, form):
		user = self.request.user
		email = form.cleaned_data['email']
		role = form.cleaned_data['role']
		uri = self.request.build_absolute_uri()

		invite = CleanTeamInvite()
		invite.inviteUsers(user, role, email, uri)

		return HttpResponseRedirect('/clean-team/invite')

	def get_context_data(self, **kwargs):
		context = super(InviteView, self).get_context_data(**kwargs)

		invitees = CleanTeamInvite.objects.filter(clean_team=self.request.user.profile.clean_team_member.clean_team)

		context['invitees'] = invitees
		context['user'] = self.request.user

		return context

class InviteResponseView(LoginRequiredMixin, FormView):
	template_name = "cleanteams/invite_response.html"
	form_class = InviteResponseForm

	def get_initial(self):
		initial = {}
		if 'token' in self.kwargs:
			token = self.kwargs['token']

			try:
				invite = CleanTeamInvite.objects.get(token=token)
				initial['token'] = invite.token
			except Exception, e:
				# TDOD: Redirect to error page
				print e
	
		return initial

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		print form.errors
		
		return self.render_to_response(context)

	def form_valid(self, form):
		response = form.cleaned_data['selections']
		token = form.cleaned_data['token']
		
		try:
			invite = CleanTeamInvite.objects.get(token=token)
			
			if response == "accepted":
				invite.status = "accepted"

				if invite.role == "clean-champion":
					clean_champion = CleanChampion()				
					clean_champion.becomeCleanChampion(self.request.user, invite.clean_team)

				elif invite.role == "clean-ambassador":
					try:
						ctm = CleanTeamMember.objects.get(user=self.request.user)
					except Exception, e:
						ctm = CleanTeamMember(user=self.request.user)
						
					ctm.becomeCleanAmbassador(self.request.user, invite.clean_team, True)
			else:
				invite.status = "declined"

			invite.save()
		except Exception, e:
			# TDOD: Redirect to error page
			print e

		return HttpResponseRedirect('/clean-team/%s' % str(invite.clean_team.id))

	def get_context_data(self, **kwargs):
		context = super(InviteResponseView, self).get_context_data(**kwargs)
		
		if 'token' in self.kwargs:
			token = self.kwargs['token']

			try:
				invite = CleanTeamInvite.objects.get(token=token)
			except Exception, e:
				# TDOD: Redirect to error page
				print e

			context['invite'] = invite

		user = self.request.user
		context['user'] = user

		return context

# Check if the invitee email address is a registered User
def invite_check(request, token):
	if token:
		try:
			invite = CleanTeamInvite.objects.get(token=token)
			user = User.objects.get(email=invite.email)
		except User.DoesNotExist, e:
			return HttpResponseRedirect('/register-invite/%s' % invite.token)
		except Invite.DoesNotExist, e:
			print e
		except Exception, e:
			print e
		
	return HttpResponseRedirect('/clean-team/invite-response/%s' % invite.token)

# On the Clean Team's Profile
def request_join_clean_team(request):
	if request.method == 'POST':
		ctid = request.POST.get('ctid')

		try:
			selected_team = CleanTeam.objects.get(id=ctid)
			ctm = CleanTeamMember.objects.get(user=request.user)
		except Exception, e:
			print e
			ctm = CleanTeamMember()

		# if not ctm.has_max_clean_ambassadors():
		ctm.requestBecomeCleanAmbassador(request.user, selected_team)
		# else:
			#TODO: Message saying that the Clean Team ambassador count is full
			# pass

	return HttpResponseRedirect('/clean-team/%s' % str(ctid))

def be_clean_champion(request):
	if request.method == 'POST':
		ctid = request.POST.get('ctid')

		try:
			selected_team = CleanTeam.objects.get(id=ctid)
			clean_champion = CleanChampion.objects.get(user=request.user, clean_team=selected_team)
		except Exception, e:
			print e
			clean_champion = CleanChampion()
			
		clean_champion.becomeCleanChampion(request.user, selected_team)

	return HttpResponseRedirect('/clean-team/%s' % str(ctid))

# Coming from the email invite link
def accept_invite(request, token):
	invite = CleanTeamInvite.objects.get(token=token)

	if not invite.accept_invite():
		return HttpResponseRedirect('/register-invite/')

	return HttpResponseRedirect('/clean-team/invite/')

def clean_team_member_action(request):
	if request.method == 'POST' and request.is_ajax:
		ctid = request.POST['ctid']
		uid = request.POST['uid']
		action = request.POST['action']
		
		clean_team_member = CleanTeamMember.objects.get(clean_team_id=ctid, user_id=uid)

		if action == "approve":
			clean_team_member.approveCleanAmbassador()
		elif action == "remove":
			clean_team_member.removedCleanAmbassador()
			
	return HttpResponse("success")