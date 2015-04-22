import datetime
import urllib
import ftplib
import os
import tempfile
import re
import json
import sys
import csv

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.mail import EmailMessage
from django.core import serializers

from django.db.models import Q
from django import forms
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django.template.loader import get_template

from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView, UpdateView
import cleanteams.forms
from cleanteams.forms import RegisterCleanTeamForm, EditCommunityForm, EditCleanTeamForm, RegisterCommunityForm, RegisterOrganizationForm, RequestJoinTeamsForm, PostMessageForm, JoinTeamCleanChampionForm, InviteForm, InviteResponseForm, LeaderReferralForm, CleanTeamPresentationForm, EditCleanTeamMainContact
from cleanteams.models import CleanTeam, CleanTeamMember, CommunityPost, CleanTeamPost, CleanChampion, CleanTeamInvite, CleanTeamLevelTask, CleanTeamLevelProgress, LeaderReferral, CleanTeamPresentation, CleanTeamFollow, OrgProfile, Community, UserCommunityMembership, TeamCommunityMembership, UserCommunityMembershipRequest, TeamCommunityMembershipRequest
from challenges.models import Challenge, UserChallengeEvent, ChallengeTeamMembership, ChallengeCommunityMembership
from users.models import OrganizationLicense
from notifications.models import Notification

from mycleancity.actions import *
from mycleancity.mixins import LoginRequiredMixin

class RegisterCleanTeamView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/register_clean_team.html"
    form_class = RegisterCleanTeamForm
    success_url = "mycleancity/index.html"

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user = request.user
        if user.profile.clean_team_member:
            if user.profile.clean_team_member.status != "declined" and user.profile.clean_team_member.status != "removed":
                return HttpResponseRedirect('/clean-team/%s' % str(user.profile.clean_team_member.clean_team.id))
        

        return self.render_to_response(self.get_context_data(form=form))
    
    def get_initial(self):
        initial = {}

        user = self.request.user
        if user.profile.referral_token != '':
            referral = LeaderReferral.objects.get(token=user.profile.referral_token)
            initial['name'] = referral.organization

        initial['contact_first_name'] = self.request.user.first_name
        initial['contact_last_name'] = self.request.user.last_name
        initial['contact_email'] = self.request.user.email

        return initial

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form):
        user = self.request.user
        role = "leader"
        orgprofile = None
        if OrgProfile.objects.filter(user=user).exists():
            orgprofile = OrgProfile.objects.filter(user=user)[0]
            role = "manager"
        logo = form.cleaned_data['logo']

        ct = CleanTeam()
        ct.name = form.cleaned_data['name']
        ct.region = form.cleaned_data['region']
        ct.group = form.cleaned_data['group']
        ct.org_profile = orgprofile

        ct.contact_user = user
        ct.contact_phone = form.cleaned_data['contact_phone']
        if logo:
            key = 'uploads/ct_logo_%s_%s' % (str(user.id), logo)
            uploadFile = UploadFileToS3()
            ct.logo = uploadFile.upload(key, logo)

        ct.save()
        ct.add_team_clean_creds(50)
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
        ctm.role = role
        ctm.org_profile = orgprofile
        ctm.save()

        if user.profile.referral_token != '':
            try:
                referral = LeaderReferral.objects.get(token=user.profile.referral_token)
                if referral.status == "pending":
                    referral.status = "accepted"
                    referral.save()
                    referral.user.profile.add_clean_creds(50)
            except Exception, e:
                print e
        elif LeaderReferral.objects.filter(email=user.email).count() > 0:
            try:
                referral = LeaderReferral.objects.filter(email=user.email)[0]
                if referral.status == "pending":
                    referral.status = "accepted"
                    referral.save()
                    referral.user.profile.add_clean_creds(50)
            except Exception, e:
                print e
        elif 'referral_token' in self.request.session:
            try:
                referral_token = self.request.session.get('referral_token')
                referral = LeaderReferral.objects.get(token=referral_token)
                if referral.status == "pending":
                    referral.status = "accepted"
                    referral.save()
                    referral.user.profile.add_clean_creds(50)
                    user.profile.referral_token = referral_token
                del self.request.session['referral_token']
            except Exception, e:
                print e
        user.profile.clean_team_member = ctm
        user.profile.add_clean_creds(50)
        user.profile.save()

        lang = user.profile.settings.communication_language

        # Send registration email to user
        if lang == "English":
            template = get_template('emails/clean_team_register.html')
            subject = 'My Effect - Welcome to Our Team!'
        else:
            template = get_template('emails/french/clean_team_register_fr.html')
            subject = 'My Effect - Welcome to Our Team!'
        uri = self.request.build_absolute_uri()
        level_progress_uri = u'%s/clean-team/level-progress' %uri
        content = Context({ 'email': user.email, 'first_name': user.first_name, 'level_progress_uri': level_progress_uri})

        from_email, to = 'info@myeffect.ca', user.email

        send_email = SendEmail()
        send_email.send(template, content, subject, from_email, to)


        # Send notification email to administrator
        #template = get_template('emails/register_email_notification.html')
        #content = Context({ 'email': user.email })

        #subject, from_email, to = 'My Effect - Change Team Signup Successful', 'info@myeffect.ca', 'partner@mycleancity.org'

        #send_email = SendEmail()
        #send_email.send(template, content, subject, from_email, to)

        return HttpResponseRedirect('/clean-team/invite/')

    def get_context_data(self, **kwargs):
        context = super(RegisterCleanTeamView, self).get_context_data(**kwargs)
        context['isManager'] = OrgProfile.objects.filter(user=self.request.user).exists()

        if self.request.flavour == "mobile":
            self.template_name = "cleanteams/mobile/register_clean_team.html"

        return context

class CleanTeamMainContactView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/main_contact.html"
    form_class = EditCleanTeamMainContact
    success_url = "mycleancity/index.html"

    def get_initial(self, clean_team_member=None):
        initial = {}

        clean_team_member = self.request.user.profile.clean_team_member
        if clean_team_member:
            clean_team = clean_team_member.clean_team
            contact_user = clean_team.contact_user

            initial['contact_first_name'] = contact_user.first_name
            initial['contact_last_name'] = contact_user.last_name
            initial['contact_email'] = contact_user.email
            initial['contact_phone'] = clean_team.contact_phone
            initial['clean_ambassadors'] = clean_team.contact_user.id
            initial['clean_team_id'] = clean_team.id

        return initial

    # Initialize the form with initial values
    def get_form_kwargs(self):
        clean_team_member = self.request.user.profile.clean_team_member
        kwargs = {
            "initial": self.get_initial(clean_team_member),
            "clean_team": clean_team_member.clean_team
        }
        if self.request.method in ("POST", "PUT"):
            kwargs.update({
                "data": self.request.POST,
                "files": self.request.FILES
            })
        return kwargs

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form):
        clean_team_id = form.cleaned_data['clean_team_id']

        try:
            clean_team_member = CleanTeamMember.objects.get(user=self.request.user)
            clean_team_member.clean_team.update_main_contact(form.cleaned_data)
        except Exception, e:
            print e

        return HttpResponseRedirect(u'/clean-team/%s' %(clean_team_id))

class EditCleanTeamView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/edit_clean_team.html"
    form_class = EditCleanTeamForm
    success_url = "mycleancity/index.html"

    def get_initial(self):
        initial = {}

        if self.request.user.profile.clean_team_member:
            clean_team = self.request.user.profile.clean_team_member.clean_team

            initial['name'] = clean_team.name
            initial['website'] = clean_team.website
            initial['twitter'] = clean_team.twitter
            initial['facebook'] = clean_team.facebook
            initial['instagram'] = clean_team.instagram
	    initial['focus'] = clean_team.focus
	  
	    
	    
            # initial['logo'] = clean_team.logo
            initial['about'] = clean_team.about
            initial['region'] = clean_team.region
            initial['group'] = clean_team.group
            initial['clean_team_id'] = clean_team.id

            community_memberships = TeamCommunityMembership.objects.filter(clean_team=clean_team.id)
            community_membership_requests = TeamCommunityMembershipRequest.objects.filter(clean_team=clean_team.id)

            if community_memberships:
                initial['community'] = community_memberships[0].community.name
            elif community_membership_requests:
                initial['community'] = community_membership_requests[0].community.name
            else:
                initial['community'] = ''

        return initial

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        print form.errors

        return self.render_to_response(context)

    def form_valid(self, form):
        clean_team_id = form.cleaned_data['clean_team_id']
        community_name = form.cleaned_data['community']
        if community_name and not community_name == "":
            community = Community.objects.get(name=community_name)
        else:
            community = None

        try:
            clean_team_member = CleanTeamMember.objects.get(user=self.request.user)
            clean_team = CleanTeam.objects.get(id=clean_team_member.clean_team.id)
        except Exception, e:
            print e

        #  Request an invitation to join the community if necessary
        if community:
            previous_memberships = TeamCommunityMembership.objects.filter(clean_team=clean_team_id)
            previous_memberships_requests = TeamCommunityMembershipRequest.objects.filter(clean_team=clean_team_id)
            if not previous_memberships and not previous_memberships_requests:
                membership_request = TeamCommunityMembershipRequest()
                membership_request.clean_team_id = clean_team.id
                membership_request.community_id = community.id
                membership_request.save()

        clean_team.name = form.cleaned_data['name']
        clean_team.website = form.cleaned_data['website']
        clean_team.twitter = form.cleaned_data['twitter']
        clean_team.facebook = form.cleaned_data['facebook']
        clean_team.instagram = form.cleaned_data['instagram']
        clean_team.about = form.cleaned_data['about']
        clean_team.region = form.cleaned_data['region']
	clean_team.focus =form.cleaned_data['focus']
        print clean_team.focus
        #print request.POST.getlist('category')
        logo = form.cleaned_data['logo']

        if logo:
            key = 'uploads/ct_logo_%s_%s' % (str(self.request.user.id), logo)
            uploadFile = UploadFileToS3()
            clean_team.logo = uploadFile.upload(key, logo)

        clean_team.save()

        if clean_team.level.name == "Seedling":
            if clean_team.about and clean_team.logo:
                task = CleanTeamLevelTask.objects.get(name="ct_description")
                clean_team.complete_level_task(task)
                clean_team.add_team_clean_creds(5)
            # only uncomment this if your testing turning this on, otherwise user can keep addidng 5CC to the team
            # else:
                # task = CleanTeamLevelTask.objects.get(name="ct_description")
                # clean_team.uncomplete_level_task(task)

            if clean_team.twitter:
                task = CleanTeamLevelTask.objects.get(name="ct_twitter")
                clean_team.complete_level_task(task)
                clean_team.add_team_clean_creds(5)
            # same here as above
            # else:
                # task = CleanTeamLevelTask.objects.get(name="ct_twitter")
                # clean_team.uncomplete_level_task(task)




        return HttpResponseRedirect(u'/clean-team/%s' %(clean_team_id))

    def get_context_data(self, **kwargs):
        context = super(EditCleanTeamView, self).get_context_data(**kwargs)
        context['community_search_url'] = self.request.build_absolute_uri("../../clean-team/community-search/?search=")

        if not self.request.user.profile.clean_team_member:
            context = None

        return context

class EditCommunityView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/edit_community.html"
    form_class = EditCommunityForm

    def get_initial(self):
        initial = {}

        community = get_object_or_404(Community, owner_user=self.request.user)
        if community:
            initial['category'] = community.category
            initial['region'] = community.region
            initial['name'] = community.name
            initial['website'] = community.website
            initial['twitter'] = community.twitter
            initial['facebook'] = community.facebook
            initial['instagram'] = community.instagram
            initial['about'] = community.about
            initial['community_id'] = community.id
        return initial

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form):
        community_id = form.cleaned_data['community_id']
        try:
            community = Community.objects.get(id=community_id)
        except Exception, e:
            print e

        community.name = form.cleaned_data['name']
        community.website = form.cleaned_data['website']
        community.twitter = form.cleaned_data['twitter']
        community.facebook = form.cleaned_data['facebook']
        community.instagram = form.cleaned_data['instagram']
        community.about = form.cleaned_data['about']
        community.region = form.cleaned_data['region']
        community.category = form.cleaned_data['category']

        logo = form.cleaned_data['logo']

        if logo:
            key = 'uploads/community_logo_%s_%s' % (str(self.request.user.id), logo)
            uploadFile = UploadFileToS3()
            community.logo = uploadFile.upload(key, logo)

        community.save()

        return HttpResponseRedirect(u'/clean-team/community/%s' %(community_id))

    def get_context_data(self, **kwargs):
        context = super(EditCommunityView, self).get_context_data(**kwargs)
        return context

class CreateCommunityView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/create_community.html"
    form_class = RegisterCommunityForm

    def get_form_kwargs(self):
        kwargs = super(CreateCommunityView, self).get_form_kwargs()
        kwargs.update({ "request": self.request })
        return kwargs

    def get_initial(self):
        initial = {}
        initial['current_user'] = self.request.user.id
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
        community = Community()
        community.name = form.cleaned_data['name']
        community.region = form.cleaned_data['region']
        community.category = form.cleaned_data['category']
        community.is_private = form.cleaned_data['is_private']
        community.owner_user = self.request.user
        community.contact_user = self.request.user

        logo = form.cleaned_data['logo']

        if logo:
            key = 'uploads/community_logo_%s_%s' % (str(self.request.user.id), logo)
            uploadFile = UploadFileToS3()
            community.logo = uploadFile.upload(key, logo)

        community.save()
        #  Asign the owner to belong to the community
        community_membership = UserCommunityMembership()
        community_membership.user = self.request.user
        community_membership.community = community
        community_membership.save()
        return HttpResponseRedirect("/")

    def get_context_data(self, **kwargs):
        context = super(CreateCommunityView, self).get_context_data(**kwargs)
        context['has_upgraded'] = self.request.user.profile.has_upgraded
        return context

def community_search(request):
    search = request.GET['search']
    query_results = list(Community.objects.filter(name__contains=search))
    result_objects = map(lambda item : { "name": item.name }, query_results)
    return HttpResponse(json.dumps(result_objects, indent=4, separators=(',', ': ')))

class TeamOrOrganization(LoginRequiredMixin, FormView):
    template_name = "cleanteams/create_team_or_org.html"
    form_class = RegisterOrganizationForm

    def get_initial(self):
        initial = {}
        initial['current_user'] = self.request.user.id
        return initial

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user = request.user
        if user.profile.clean_team_member:
            if user.profile.clean_team_member.status != "declined" and user.profile.clean_team_member.status != "removed":
                return HttpResponseRedirect('/clean-team/%s' % str(user.profile.clean_team_member.clean_team.id))
        

        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form):
        pass_url = "/clean-team/register-clean-team/"
        redirect = "/clean-team/create-team-or-org/"
        u = self.request.user
        access_code = form.cleaned_data['access_code']
        if OrgProfile.objects.filter(user=u).exists():
            OrgProfile.objects.filter(user=u).delete()
        if form.cleaned_data['create_team'] == 'change_team':
            redirect = pass_url
        if form.cleaned_data['create_team'] == 'representing':
            if form.cleaned_data['org_type'] == 'nonprofit_charity':
                if not OrganizationLicense.objects.filter(user=u).exists():
                    orgLicense = OrganizationLicense()
                    orgLicense.new_charity_license(u)
                orgProfile = OrgProfile()
                orgProfile.org_type = form.cleaned_data['org_type']
                orgProfile.registered_number = form.cleaned_data['registered_number']
                orgProfile.category = form.cleaned_data['category']
                orgProfile.user = u
                orgProfile.save()
                redirect = pass_url

            elif OrganizationLicense.objects.filter(user=u).exists() and not OrganizationLicense.objects.get(user=u).is_charity and OrganizationLicense.objects.get(user=u).to_date > date.today():
                orgProfile = OrgProfile()
                orgProfile.number_of_users = form.cleaned_data['number_of_users']
                orgProfile.user = u
                orgProfile.save()
                redirect = pass_url
            elif access_code and OrganizationLicense.objects.filter(code=access_code).exists():
                orgLicense = OrganizationLicense.objects.filter(code=access_code)[0]
                if not orgLicense.is_charity and orgLicense.to_date > date.today():
                    orgProfile = OrgProfile()
                    orgProfile.number_of_users = form.cleaned_data['number_of_users']
                    orgProfile.user = u
                    orgProfile.save()
                    if OrganizationLicense.objects.filter(user=u).exists():
                        OrganizationLicense.objects.filter(user=u).delete()
                    orgLicense.user = u
                    orgLicense.save()
                    redirect = pass_url

        return HttpResponseRedirect(redirect)

    def get_context_data(self, **kwargs):
        context = super(TeamOrOrganization, self).get_context_data(**kwargs)
        u = self.request.user
        context['user'] = u
        org_license = False
        if OrganizationLicense.objects.filter(user=u).exists():
            if not OrganizationLicense.objects.get(user=u).is_charity and OrganizationLicense.objects.get(user=u).to_date > date.today():
                org_license = True
        context['org_license'] = org_license

        return context

class ViewAllCleanTeams(TemplateView):
    template_name = "cleanteams/all_clean_teams.html"

    def get_context_data(self, **kwargs):
        context = super(ViewAllCleanTeams, self).get_context_data(**kwargs)

        teams = CleanTeam.objects.all()
        communities = Community.objects.all()

        following_map = {}

        if self.request.user.is_authenticated():
            clean_champions = CleanChampion.objects.filter(user=self.request.user)
            follow_list = CleanTeamFollow.objects.filter(user=self.request.user)
            for follow in follow_list:
                following_map[follow.clean_team_id] = follow.clean_team_id

            context['clean_champions'] = clean_champions

        context['teams'] = teams
        context['communities'] = communities
        context['user'] = self.request.user
        context['following_map'] = following_map

        return context

class LevelProgressView(TemplateView):
    template_name = "cleanteams/level_progress.html"

    def get_context_data(self, **kwargs):
        context = super(LevelProgressView, self).get_context_data(**kwargs)
        user = self.request.user
        clean_team = user.profile.clean_team_member.clean_team
        countcomp = 0
        level_tasks = CleanTeamLevelTask.objects.filter(clean_team_level=clean_team.level)
        tasks = CleanTeamLevelProgress.objects.filter(clean_team=clean_team, level_task__in=level_tasks)
        tasks_complete = CleanTeamLevelProgress.objects.filter(clean_team=clean_team, level_task__in=level_tasks, completed=True).count()

        if CleanTeamLevelProgress.objects.filter(completed=1):
            countcomp += 1
        elif CleanTeamLevelProgress.objects.filter(completed=0):
            countcomp == countcomp

        context['tasks'] = tasks
        context['clean_team'] = clean_team
        context['user'] = user
        context['tasks_complete'] = tasks_complete
        return context

class CommunityView(TemplateView):
    template_name = "cleanteams/community_profile.html"

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(CommunityView, self).get_context_data(**kwargs)
        user = self.request.user

        if 'community_id' in self.kwargs:
            try:
                user_challenges = UserChallengeEvent.objects.filter(user=user, challenge__clean_team_id=ctid)
                user_challenges_list = UserChallengeEvent.objects.filter(user=user, challenge__clean_team_id=ctid).values_list('challenge_id', flat=True)
            except Exception, e:
                user_challenges = []
                user_challenges_list = []
            today = datetime.datetime.now()
            community_id = self.kwargs['community_id']
            challenge_ids = list(ChallengeCommunityMembership.objects.filter(community_id=community_id).values_list("challenge_id",flat=True))
            challenges = Challenge.objects.filter(Q(event_end_date__gte=today), Q(id__in=challenge_ids)).exclude(id__in=user_challenges_list).order_by('-promote_top', '-event_start_date')

            challenge_dict = {}

            count = 0
            for challenge in challenges:
                challenge_dict[count] = ["not-particpating", challenge]
                count += 1

            for user_challenge in user_challenges:
                challenge_dict[user_challenge.challenge.id] = ["particpating", user_challenge.challenge]

            context['challenges'] = challenge_dict

            context['community'] = get_object_or_404(Community, id=community_id)
            context['posts'] = CommunityPost.objects.filter(community=community_id).order_by('-timestamp')
            context['team_memberships'] = TeamCommunityMembership.objects.filter(community_id=community_id).order_by('clean_team__clean_creds')
            context['user_memberships'] = UserCommunityMembership.objects.filter(community_id=community_id)
            context['has_membership_request'] = UserCommunityMembershipRequest.objects.filter(community_id=community_id, user_id=user.id).count()
            context['is_member'] = UserCommunityMembership.objects.filter(community_id=community_id, user_id=user.id).count()

            #  Find out what community (if any) the user is a member of
            parent_communities = UserCommunityMembership.objects.filter(user=self.request.user)
            if parent_communities.count():
                #  Hide all challenges that are privately associated with communities other than the community they are a member of
                hidden_challenges = ChallengeCommunityMembership.objects.filter(Q(is_private=True) & ~Q(community=parent_communities[0])).values_list('challenge_id', flat=True)
            else:
                #  Hide all challenges that are privately associated with communities
                hidden_challenges = ChallengeCommunityMembership.objects.filter(is_private=True).values_list('challenge_id', flat=True)

            context['hidden_challenges'] = hidden_challenges

        return context

class CleanTeamView(TemplateView):
    template_name = "cleanteams/clean_team_profile.html"
    
    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(CleanTeamView, self).get_context_data(**kwargs)
        user = self.request.user
	
        if 'ctid' in self.kwargs:
            ctid = self.kwargs['ctid']
            context['clean_team'] = get_object_or_404(CleanTeam, id=ctid)
	    all_categories= cleanteams.forms.ORG_CATEGORIES
	    #print all_categories[0][0]
	    labeled_selected_categories=''
	    selected_categories=context['clean_team'].focus
	    for t in all_categories:
		if selected_categories and t[0] in selected_categories:
			labeled_selected_categories+=t[1]
	    context['focus']=labeled_selected_categories
	    #print labeled_selected_categories
            follows = CleanTeamFollow.objects.filter(clean_team_id=ctid, user_id=self.request.user.id).count()
            cas = CleanTeamMember.objects.filter(clean_team_id=ctid)
            ccs = CleanChampion.objects.filter(clean_team_id=ctid)
            posts = CleanTeamPost.objects.filter(clean_team_id=ctid).order_by('-timestamp')

            try:
                clean_champion = CleanChampion.objects.get(clean_team_id=ctid, user=user)
                context['clean_champion'] = clean_champion
            except Exception, e:
                print e

            try:
                invite = CleanTeamInvite.objects.get(email=user.email, clean_team_id=ctid)
                context['invite'] = invite
            except Exception, e:
                print e

            try:
                # TODO: Need to pass this to the template
                clean_ambassador = CleanTeamMember.objects.get(clean_team_id=ctid, user=user, status="approved", role="leader")
                context['clean_ambassador'] = clean_ambassador
            except Exception, e:
                print e

            try:
                user_challenges = UserChallengeEvent.objects.filter(user=user, challenge__clean_team_id=ctid)
                user_challenges_list = UserChallengeEvent.objects.filter(user=user, challenge__clean_team_id=ctid).values_list('challenge_id', flat=True)
            except Exception, e:
                user_challenges = []
                user_challenges_list = []

            today = datetime.datetime.now()
            team_approved_challenges = list(ChallengeTeamMembership.objects.filter(clean_team_id=ctid).values_list('challenge_id', flat=True))
            challenges = Challenge.objects.filter(Q(event_end_date__gte=today), Q(clean_team_id=ctid) | Q(id__in=team_approved_challenges)).exclude(id__in=user_challenges_list).order_by('-promote_top', '-event_start_date')

            challenge_dict = {}

            count = 0
            for challenge in challenges:
                challenge_dict[count] = ["not-particpating", challenge]
                count += 1

            for user_challenge in user_challenges:
                challenge_dict[user_challenge.challenge.id] = ["particpating", user_challenge.challenge]

            if user.is_authenticated():
                if user.profile.is_clean_ambassador():
                    leading_teams = user.profile.clean_team_member.clean_team.get_leading_teams()
                    context['leading_teams'] = leading_teams
                    context['pixels'] = user.profile.clean_team_member.clean_team.get_pixels_for_leading_teams(user.profile.clean_team_member.clean_team.clean_creds)

            context['challenges'] = challenge_dict
            context['page_url'] = self.request.get_full_path()
            context['cas'] = cas
            context['ccs'] = ccs
            context['posts'] = posts
            context['follows'] = follows

        context['user'] = user

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
            #TODO: Message saying that the Change Team ambassador count is full
            # pass

        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super(RegisterRequestJoinView, self).get_context_data(**kwargs)
        user = self.request.user

        context['user'] = user

        if self.request.flavour == "mobile":
            self.template_name = "cleanteams/mobile/register_request_join.html"

        return context

class CleanTeamMembersView(LoginRequiredMixin, TemplateView):
    template_name = "cleanteams/clean_team_members.html"

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(CleanTeamMembersView, self).get_context_data(**kwargs)
        user = self.request.user

        ct = user.profile.clean_team_member
        cas = CleanTeamMember.objects.filter(clean_team=ct.clean_team)
        ccs = CleanChampion.objects.filter(clean_team=ct.clean_team)
        # ctm = CleanTeamMember.objects.filter(clean_team=ct.clean_team)

        # TODO: HttpResponseRedirect is not working
        # Check if approved Clean Ambassador
        if ct.role not in ["leader","manager"] or ct.status != "approved":
            return HttpResponseRedirect("/challenges")

        context['user'] = user
        context['clean_team'] = ct.clean_team
        context['cas'] = cas
        context['ccs'] = ccs
        # context['clean_team_members'] = ctm

        return context

class CommunityMembersView(LoginRequiredMixin, TemplateView):
    template_name = "cleanteams/community_members.html"

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(CommunityMembersView, self).get_context_data(**kwargs)
        user = self.request.user

        community = Community.objects.get(owner_user=self.request.user.id)

        context['user'] = user
        context['community'] = community
        context['team_membership_requests'] = TeamCommunityMembershipRequest.objects.filter(community=community.id)
        context['user_membership_requests'] = UserCommunityMembershipRequest.objects.filter(community=community.id)
        context['team_memberships'] = TeamCommunityMembership.objects.filter(community=community.id)
        context['user_memberships'] = UserCommunityMembership.objects.filter(community=community.id)
        return context

class PostMessageView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/post_message.html"
    form_class = PostMessageForm

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form):
        user = self.request.user
        clean_team = user.profile.clean_team_member.clean_team
        message = form.cleaned_data['message']

        clean_team_post = CleanTeamPost()
        clean_team_post.newPost(user, message, clean_team)

        return HttpResponseRedirect('/clean-team/%s' % str(clean_team.id))

    def get_context_data(self, **kwargs):
        context = super(PostMessageView, self).get_context_data(**kwargs)
        user = self.request.user

        context['user'] = user

        return context

def post_message_ajax(request):
    if request.method == 'POST' and request.is_ajax:
        user = request.user
        message = request.POST['message']
        ctid = request.POST.get('ctid', None)
        community_id = request.POST.get('community_id', None)

        if ctid:
            clean_team = get_object_or_404(CleanTeam, id=ctid)
            clean_team_post = CleanTeamPost()
            post = clean_team_post.newPost(user, message, clean_team)
        elif community_id:
            community = get_object_or_404(Community, id=community_id)
            community_post = CommunityPost()
            post = community_post.newPost(user, message, community)
        else:
            raise Exception("Unexpected post type.")

    return HttpResponse(post)

def resend_invite(request):
    if request.method == 'POST' and request.is_ajax:
        invite_id = request.POST['invite_id']
        uri = request.build_absolute_uri()

        try:
            invite = CleanTeamInvite.objects.get(id=invite_id)
            invite.resendInvite(uri)
        except Exception, e:
            raise e

    return HttpResponse("success")

class InviteView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/invite.html"
    form_class = InviteForm
    success_url = "cleanteams/invite.html"

    def get_initial(self):
        initial = {}
        if self.request.user.profile.clean_team_member and self.request.user.profile.clean_team_member.status == "approved":
            initial['clean_team_id'] = self.request.user.profile.clean_team_member.clean_team.id
            role = self.request.GET.get('role', 'agent')
            initial['role'] = role
        return initial

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form):
        user = self.request.user
        email = form.cleaned_data['email']
        role = form.cleaned_data['role']
        uri = self.request.build_absolute_uri().rstrip('/')

        emails = re.split(',', email)

        for e in emails:
            e = e.strip()

            if e == "":
                continue

            invite = CleanTeamInvite()
            invite.inviteUser(user, role, e, uri)

        return HttpResponseRedirect('/clean-team/invite')

    def get_context_data(self, **kwargs):
        context = super(InviteView, self).get_context_data(**kwargs)

        if self.request.user.profile.clean_team_member and self.request.user.profile.clean_team_member.status == "approved":
            invitees = CleanTeamInvite.objects.filter(clean_team=self.request.user.profile.clean_team_member.clean_team)
            context['clean_team'] = self.request.user.profile.clean_team_member.clean_team
            role = self.request.GET.get('role', 'agent')
            context['role'] = role
        else:
            invitees = CleanTeamInvite.objects.filter(user=self.request.user)

        context['invitees'] = invitees
        context['user'] = self.request.user

        return context

class InviteOrganizationView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/invite_organization.html"
    form_class = LeaderReferralForm

    def get_initial(self):
        initial = {}
        if self.request.user.profile.clean_team_member and self.request.user.profile.clean_team_member.status == "approved":
            initial['clean_team_id'] = self.request.user.profile.clean_team_member.clean_team.id

        return initial

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form):
        user = self.request.user
        clean_team = None
        if user.profile.clean_team_member and user.profile.clean_team_member.status == "approved":
            clean_team = user.profile.clean_team_member.clean_team
        uri = self.request.build_absolute_uri()

        leader_referral = LeaderReferral()
        leader_referral.new_referral(user, form, clean_team, uri)

        return HttpResponseRedirect('/clean-team/invite-org/')

    def get_context_data(self, **kwargs):
        context = super(InviteOrganizationView, self).get_context_data(**kwargs)

        if self.request.user.profile.clean_team_member and self.request.user.profile.clean_team_member.status == "approved":
            referers = LeaderReferral.objects.filter(clean_team=self.request.user.profile.clean_team_member.clean_team)
            context['clean_team'] = self.request.user.profile.clean_team_member.clean_team
        else:
            referers = LeaderReferral.objects.filter(user=self.request.user)
        context['referers'] = referers
        context['user'] = self.request.user

        return context

# Coming from the invite email
def unsubscribe(request, token):
    invite = CleanTeamInvite.objects.get(token=token)
    invite.unsubscribe()

    return render_to_response('mycleancity/unsubscribe.html', context_instance=RequestContext(request))

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

                if invite.role == "agent":
                    clean_champion = CleanChampion()
                    clean_champion.becomeCleanChampion(self.request.user, invite.clean_team)

                elif invite.role == "leader":
                    try:
                        ctm = CleanTeamMember.objects.get(user=self.request.user)
                    except Exception, e:
                        ctm = CleanTeamMember(user=self.request.user)

                    ctm.becomeCleanAmbassador(self.request.user, invite.clean_team, False)
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

class CleanTeamPresentationView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/clean_team_presentation.html"
    form_class = CleanTeamPresentationForm

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        print form.errors

        return self.render_to_response(context)

    def form_valid(self, form):
        user = self.request.user
        clean_team = user.profile.clean_team_member.clean_team

        presentation = CleanTeamPresentation()
        presentation.new_submission(user, form, clean_team)

        return HttpResponseRedirect('/clean-team/level-progress')

    def get_context_data(self, **kwargs):
        context = super(CleanTeamPresentationView, self).get_context_data(**kwargs)

        return context

# Check if the invitee email address is a registered User
def invite_check(request, token):
    if token:
        request.session['invite_token'] = token
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

# Check if the referee email address is a registered User
def referral_check(request, token):
    if token:
        request.session['referral_token'] = token
        try:
            referral = LeaderReferral.objects.get(token=token)
            user = User.objects.get(email=referral.email)
        except User.DoesNotExist, e:
            return HttpResponseRedirect('/register/')
        except referral.DoesNotExist, e:
            print e
        except Exception, e:
            print e

    return HttpResponseRedirect('/clean-team/register-clean-team/')

# On the Change Team's Profile
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
            #TODO: Message saying that the Change Team ambassador count is full
            # pass

    return HttpResponseRedirect('/clean-team/%s' % str(ctid))

def follow_team(request):
    if request.method == 'POST':
        ctid = request.POST.get('ctid')

        try:
            selected_team = CleanTeam.objects.get(id=ctid)
            follow_object = CleanTeamFollow()
            follow_object.user_id = request.user.id
            follow_object.clean_team_id = selected_team.id
            follow_object.save()
        except Exception, e:
            print e

    return HttpResponseRedirect('/clean-team')

def community_membership_request(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')

        try:
            membership_request = UserCommunityMembershipRequest()
            membership_request.user_id = request.user.id
            membership_request.community_id = community_id
            membership_request.save()
        except Exception, e:
            print e

    return HttpResponse("success")

def unfollow_team(request):
    if request.method == 'POST':
        ctid = request.POST.get('ctid')

        try:
            selected_team = CleanTeam.objects.get(id=ctid)
            follow_object = CleanTeamFollow.objects.get(user=request.user, clean_team=selected_team)
            follow_object.delete()
        except Exception, e:
            print e

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

        if action == "approve" and request.POST['role']:
            if request.POST['role'] == "leader":
                clean_team_member.approveCleanAmbassador()
            elif request.POST['role'] == "agent":
                u = User.objects.get(id=uid)
                ct = CleanTeam.objects.get(id=ctid)
                try:
                    clean_champion = CleanChampion.objects.get(user=u, clean_team=ct)
                except Exception, e:
                    clean_champion = CleanChampion()
                    clean_champion.becomeCleanChampion(u, ct)
                    clean_team_member.removedCleanAmbassador()
        elif action == "remove":
            clean_team_member.removedCleanAmbassador()

    return HttpResponse("success")

def community_member_action(request):
    if request.method == 'POST' and request.is_ajax:
        clean_team_id = request.POST.get('clean_team_id', None)
        user_id = request.POST.get('user_id', None)
        action = request.POST['action']

        if clean_team_id:
            if action == "approve":
                team_community_membership_request = TeamCommunityMembershipRequest.objects.get(clean_team_id=clean_team_id)
                team_community_membership = TeamCommunityMembership()
                team_community_membership.clean_team_id = team_community_membership_request.clean_team.id
                team_community_membership.community_id = team_community_membership_request.community.id
                team_community_membership.save()
                team_community_membership_request.delete()
            elif action == "remove":
                team_community_membership = TeamCommunityMembership.objects.get(clean_team_id=clean_team_id)
                team_community_membership.delete()

        if user_id:
            if action == "approve":
                user_community_membership_request = UserCommunityMembershipRequest.objects.get(user_id=user_id)
                user_community_membership = UserCommunityMembership()
                user_community_membership.user_id = user_community_membership_request.user.id
                user_community_membership.community_id = user_community_membership_request.community.id
                user_community_membership.save()
                user_community_membership_request.delete()
            elif action == "remove":
                user_community_membership = UserCommunityMembership.objects.get(user_id=user_id)
                user_community_membership.delete()

    return HttpResponse("success")

def get_nav_data(request):
  #  This function can be used to make variables available to every page so they can be used on the nav header.
  glbl_my_community = None
  if request.user.is_authenticated():
    if Community.objects.filter(owner_user=request.user).count():
      glbl_my_community = Community.objects.get(owner_user=request.user)
  return {'glbl_my_community': glbl_my_community}
