import datetime
import urllib
import ftplib
import os
import tempfile
import re

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.mail import EmailMessage

from django.db.models import Q
from django import forms

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django.template.loader import get_template

from django.views.generic import *
from django.views.generic.base import View
from django.views.generic.edit import FormView, UpdateView

from cleanteams.forms import RegisterCleanTeamForm, EditCleanTeamForm, RegisterOrganizationForm, RequestJoinTeamsForm, PostMessageForm, JoinTeamCleanChampionForm, InviteForm, InviteResponseForm, LeaderReferralForm, CleanTeamPresentationForm, EditCleanTeamMainContact
from cleanteams.models import CleanTeam, CleanTeamMember, CleanTeamPost, CleanChampion, CleanTeamInvite, CleanTeamLevelTask, CleanTeamLevelProgress, LeaderReferral, CleanTeamPresentation, OrgProfile
from challenges.models import Challenge, UserChallenge

from notifications.models import Notification

from mycleancity.actions import *
from mycleancity.mixins import LoginRequiredMixin

class RegisterCleanTeamView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/register_clean_team.html"
    form_class = RegisterCleanTeamForm
    success_url = "mycleancity/index.html"

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
                    referral.clean_team.add_team_clean_creds(50)
            except Exception, e:
                print e
        elif LeaderReferral.objects.filter(email=user.email).count() > 0:
            try:
                referral = LeaderReferral.objects.filter(email=user.email)[0]
                if referral.status == "pending":
                    referral.status = "accepted"
                    referral.save()
                    referral.clean_team.add_team_clean_creds(50)
            except Exception, e:
                print e
        elif 'referral_token' in self.request.session:
            try:
                referral_token = self.request.session.get('referral_token')
                referral = LeaderReferral.objects.get(token=referral_token)
                if referral.status == "pending":
                    referral.status = "accepted"
                    referral.save()
                    referral.clean_team.add_team_clean_creds(50)
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
            subject = 'My Effect - Change Team Signup Successful'
        else:
            template = get_template('emails/french/clean_team_register_fr.html')
            subject = 'My Effect - Change Team Signup Successful'

        content = Context({ 'email': user.email, 'first_name': user.first_name })

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
            # initial['logo'] = clean_team.logo
            initial['about'] = clean_team.about
            initial['region'] = clean_team.region
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
        clean_team.facebook = form.cleaned_data['facebook']
        clean_team.instagram = form.cleaned_data['instagram']
        clean_team.about = form.cleaned_data['about']
        clean_team.region = form.cleaned_data['region']

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
                clean_team.clean_creds += 5
            else:
                task = CleanTeamLevelTask.objects.get(name="ct_description")
                clean_team.uncomplete_level_task(task)

            if clean_team.twitter:
                task = CleanTeamLevelTask.objects.get(name="ct_twitter")
                clean_team.complete_level_task(task)
            else:
                task = CleanTeamLevelTask.objects.get(name="ct_twitter")
                clean_team.uncomplete_level_task(task)

        return HttpResponseRedirect(u'/clean-team/%s' %(clean_team_id))

    def get_context_data(self, **kwargs):
        context = super(EditCleanTeamView, self).get_context_data(**kwargs)

        if not self.request.user.profile.clean_team_member:
            context = None

        return context

class TeamOrOrganization(LoginRequiredMixin, FormView):
    template_name = "cleanteams/create_team_or_org.html"
    form_class = RegisterOrganizationForm

    def get_initial(self):
        initial = {}
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
        u = self.request.user
        if OrgProfile.objects.filter(user=u).exists():
            OrgProfile.objects.filter(user=u).delete()
        if form.cleaned_data['create_team'] != 'change team':
            orgProfile = OrgProfile()
            orgProfile.org_type = form.cleaned_data['org_type']
            orgProfile.registered_number = form.cleaned_data['registered_number']
            orgProfile.category = form.cleaned_data['category']
            orgProfile.user = u
            orgProfile.save()

        return HttpResponseRedirect('/clean-team/register-clean-team/')

    def get_context_data(self, **kwargs):
        context = super(TeamOrOrganization, self).get_context_data(**kwargs)
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
        user = self.request.user

        if 'ctid' in self.kwargs:
            ctid = self.kwargs['ctid']
            context['clean_team'] = get_object_or_404(CleanTeam, id=ctid)

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
                user_challenges = UserChallenge.objects.filter(user=user, challenge__clean_team_id=ctid)
                user_challenges_list = UserChallenge.objects.filter(user=user, challenge__clean_team_id=ctid).values_list('challenge_id', flat=True)
            except Exception, e:
                user_challenges = []
                user_challenges_list = []

            today = datetime.datetime.now()
            challenges = Challenge.objects.filter(Q(event_end_date__gte=today), clean_team_id=ctid).exclude(id__in=user_challenges_list).order_by('-promote_top', '-event_start_date')

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
        except Exception, e:
            print e
            clean_champion = CleanChampion()

        clean_champion.becomeCleanChampion(self.request.user, selected_team)

        return HttpResponseRedirect('/clean-team/%s' % selected_team.id)

    def get_context_data(self, **kwargs):
        context = super(RegisterCleanChampionView, self).get_context_data(**kwargs)
        user = self.request.user

        context['clean_champions'] = CleanChampion.objects.filter(user=self.request.user)
        context['user'] = user

        if self.request.flavour == "mobile":
            self.template_name = "cleanteams/mobile/register_clean_champion.html"

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
        ctid = request.POST['ctid']

        clean_team = get_object_or_404(CleanTeam, id=ctid)

        clean_team_post = CleanTeamPost()
        post = clean_team_post.newPost(user, message, clean_team)

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
        uri = self.request.build_absolute_uri()

        print email

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

        invitees = CleanTeamInvite.objects.filter(clean_team=self.request.user.profile.clean_team_member.clean_team)

        context['invitees'] = invitees
        context['user'] = self.request.user

        return context

class InviteOrganizationView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/invite_organization.html"
    form_class = LeaderReferralForm

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
        clean_team = user.profile.clean_team_member.clean_team
        uri = self.request.build_absolute_uri()

        leader_referral = LeaderReferral()
        leader_referral.new_referral(user, form, clean_team, uri)

        return HttpResponseRedirect('/clean-team/invite-org/')

    def get_context_data(self, **kwargs):
        context = super(InviteOrganizationView, self).get_context_data(**kwargs)

        referers = LeaderReferral.objects.filter(clean_team=self.request.user.profile.clean_team_member.clean_team)

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

                if invite.role == "catalyst":
                    clean_champion = CleanChampion()
                    clean_champion.becomeCleanChampion(self.request.user, invite.clean_team)

                elif invite.role == "ambassador":
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

class LeaderReferralView(LoginRequiredMixin, FormView):
    template_name = "cleanteams/leader_referral.html"
    form_class = LeaderReferralForm

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        print form.errors

        return self.render_to_response(context)

    def form_valid(self, form):
        user = self.request.user
        clean_team = user.profile.clean_team_member.clean_team

        leader_referral = LeaderReferral()
        leader_referral.new_referral(user, form, clean_team, url)

        return HttpResponseRedirect('/clean-team/level-progress')

    def get_context_data(self, **kwargs):
        context = super(LeaderReferralView, self).get_context_data(**kwargs)

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