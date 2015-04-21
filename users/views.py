import urllib
import ftplib
import json
import os
import tempfile
import mailchimp

from datetime import date

from django.db.models import Sum
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
<<<<<<< HEAD
import cleanteams.forms
from challenges.models import Challenge, UserChallengeEvent
=======

from challenges.models import Challenge, UserChallengeEvent, ChallengeParticipant
>>>>>>> d34d34bfb15dd13708079fe0a5c8ce8883eb8a2a
from cleanteams.models import CleanTeam, CleanChampion, CleanTeamMember, CleanTeamInvite, LeaderReferral, UserCommunityMembershipRequest, UserCommunityMembership, Community
import cleanteams.views
import users.forms
from mycleancity.mixins import LoginRequiredMixin
from mycleancity.actions import *
from users.models import ProfilePhase, ProfileTask, ProfileProgress, ProfilePhase
from users.forms import PrelaunchEmailsForm, RegisterUserForm, ProfileForm, UpgradeAccountForm, SettingsForm, CustomPasswordResetForm
from userprofile.models import UserSettings, UserProfile, QRCodeSignups, UserQRCode

from django.contrib.auth.views import password_reset as django_password_reset
def get_user_json(request):
    if request.is_ajax:
        uid = request.GET['uid']

        try:
            user = User.objects.get(id=uid)

            serialized_obj = serializers.serialize('json', [ user, ])
            return HttpResponse(serialized_obj)
        except Exception, e:
            print e

    return HttpResponse('')

def password_reset(*args, **kwargs):
    """
        Overriding the Email Password Resert Forms Save to be able to send HTML email
    """
    kwargs['password_reset_form'] = CustomPasswordResetForm
    return django_password_reset(*args, **kwargs)

def auth_view(request):
    c = {}
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=email, password=password)
    next_url = None

    if 'next' in request.GET:
        next_url = urllib.quote(request.GET['next'])

    if user is not None:
        auth.login(request, user)

        if next_url:
            return HttpResponseRedirect(urllib.unquote(next_url))
        else:
            return HttpResponseRedirect('/')
    else:
        c['invalid'] = True

    c['next_url'] = next_url
    c.update(csrf(request))
    return render_to_response('users/login.html', c, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def register_success(request):
    return render_to_response('register_success.html')

class LoginPageView(TemplateView):
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)

        if 'next' in self.request.GET:
            next_url = urllib.quote(self.request.GET['next'])
            print next_url
            context['next_url'] = next_url
        else:
            print "not there"
            
        return context

class PrelaunchView(FormView):
    template_name = "mycleancity/landing.html"
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
        form.save()

        return HttpResponseRedirect(self.get_success_url())

class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterUserForm
    success_url = "/users/profile/"

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if 'invite_token' in request.session:
            token = request.session.get('invite_token')
            return HttpResponseRedirect('/register-invite/%s' % token)
        return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self):
        referral_token = ''
        initial = {}
        if 'referral_token' in self.request.session:
            referral_token = self.request.session.get('referral_token')
            referral = LeaderReferral.objects.get(token=referral_token)
            if referral is not None:
                initial['email'] = referral.email
                initial['first_name'] = referral.first_name
                initial['last_name'] = referral.last_name
        
        initial['referral_token'] = referral_token
        return initial

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form):
        uName = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
        suffix = ''
        i = 0
        while User.objects.filter(username=uName+suffix):
            i=i+1
            suffix = str(i)

        u = User.objects.create_user(
            uName+suffix,
            form.cleaned_data['email'],
            form.cleaned_data['password']
        )
        u.first_name = form.cleaned_data['first_name']
        u.last_name = form.cleaned_data['last_name']
        u.profile.hear_about_us = form.cleaned_data['hear_about_us']
        #u.profile.settings.communication_language = form.cleaned_data['communication_language']
        u.profile.referral_token = form.cleaned_data['referral_token']
        u.profile.settings.data_privacy = 1
        u.profile.settings.save()
        u.profile.save()
        u.save()

        if 'referral_token' in self.request.session:
            del self.request.session['referral_token']

        today = date.today()
        early_bird_date = date(2014, 03, 19)

        if today <= early_bird_date:
            u.profile.add_clean_creds(50)

        if 'qrcode' in self.kwargs:
            qr_code_signup = QRCodeSignups()
            qr_code_signup.user = User.objects.latest('id')
            qr_code_signup.save()

        user = auth.authenticate(username=u.username, password=form.cleaned_data['password'])
        auth.login(self.request, user)

        lang = u.profile.settings.communication_language
        
        # Send registration email to user
        try:
            list = mailchimp.utils.get_connection().get_list_by_id(settings.MAILCHIMP_MEMBERS_LIST_ID)
            list.subscribe(form.cleaned_data['email'], {'EMAIL': form.cleaned_data['email'], 'FNAME': form.cleaned_data['first_name'], 'LNAME': form.cleaned_data['last_name']})
        except Exception, e:
            print e

        if lang == "English":
            template = get_template('emails/user_register_success.html')
            subject = 'My Effect - Signup Successful'
        else:
            template = get_template('emails/french/user_register_success_fr.html')
            subject = 'My Effect - Signup Successful'
        
        #content = Context({ 'first_name': form.cleaned_data['first_name'] })

        #from_email, to = 'info@mycleancity.org', form.cleaned_data['email']

        #send_email = SendEmail()
        #send_email.send(template, content, subject, from_email, to)


        # Send notification email to administrator
        #template = get_template('emails/register_email_notification.html')
        #content = Context({ 'email': form.cleaned_data['email'], 'first_name': form.cleaned_data['first_name'], 'last_name': form.cleaned_data['last_name'], 'student': 'student' })

        #subject, from_email, to = 'My Effect - Student Signup Successful', 'info@mycleancity.org', 'communications@mycleancity.org'

        #send_email = SendEmail()
        #send_email.send(template, content, subject, from_email, to)

        return HttpResponseRedirect('/users/profile/')


    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)

        if 'qrcode' in self.kwargs:
            context['popup'] = True
    
        context['page_url'] = self.request.get_full_path()
        context['user'] = self.request.user

        #if self.request.flavour == "mobile":
            #self.template_name = "users/mobile/register.html"

        return context  

# TODO: Pretty much a copy and paste of RegisterView,
# find a more efficient way of doing this.
class RegisterInviteView(FormView):
    template_name = "users/register.html"
    form_class = RegisterUserForm
    success_url = "/users/profile/"

    def get_initial(self):
        if 'token' in self.kwargs:
            token = self.kwargs['token']
        elif 'invite_token' in self.request.session:
            token = self.request.session.get('invite_token')
        else:
            return HttpResponseRedirect('/register/')

        invite = CleanTeamInvite.objects.get(token=token)
        referral_token = ''
        if 'referral_token' in self.request.session:
            referral_token = self.request.session.get('referral_token')
        # TODO: Need to make the fields read-only
        initial = {}
        initial['email'] = invite.email
        initial['token'] = invite.token
        initial['referral_token'] = referral_token

        return initial

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
        u.profile.hear_about_us = form.cleaned_data['hear_about_us']
        u.profile.referral_token = form.cleaned_data['referral_token']
        u.profile.settings.data_privacy = 1
        u.profile.settings.save()
        u.profile.save()
        u.save()

        today = date.today()
        early_bird_date = date(2014, 03, 19)

        if today <= early_bird_date:
            u.profile.add_clean_creds(50)

        invite = CleanTeamInvite.objects.get(token=form.cleaned_data['token'])
        
        invite.acceptInvite(u)
        invite.save()
        if 'invite_token' in self.request.session:
            del self.request.session['invite_token']
        if 'referral_token' in self.request.session:
            del self.request.session['referral_token']
        user = auth.authenticate(username=u.username, password=form.cleaned_data['password'])
        auth.login(self.request, user)

        lang = u.profile.settings.communication_language

        if invite.community:
            community_membership = UserCommunityMembership()
            community_membership.user = user
            community_membership.community = invite.community
            community_membership.save()
        # Send registration email to user
        try:
            list = mailchimp.utils.get_connection().get_list_by_id(settings.MAILCHIMP_MEMBERS_LIST_ID)
            list.subscribe(form.cleaned_data['email'], {'EMAIL': form.cleaned_data['email'], 'FNAME': form.cleaned_data['first_name'], 'LNAME': form.cleaned_data['last_name']})
        except Exception, e:
            print e

        #template = get_template('emails/user_register_success.html')
        #subject = 'My Effect - Signup Successful'
        
        #content = Context({ 'first_name': form.cleaned_data['first_name'] })

        #from_email, to = 'info@mycleancity.org', form.cleaned_data['email']

        #send_email = SendEmail()
        #send_email.send(template, content, subject, from_email, to)


        # Send notification email to administrator
        #template = get_template('emails/register_email_notification.html')
        #content = Context({ 'email': form.cleaned_data['email'], 'first_name': form.cleaned_data['first_name'], 'last_name': form.cleaned_data['last_name'], 'student': 'student' })

        #subject, from_email, to = 'My Effect - Student Signup Successful', 'info@mycleancity.org', 'communications@mycleancity.org'

        #send_email = SendEmail()
        #send_email.send(template, content, subject, from_email, to)


        return HttpResponseRedirect('/users/profile/')
class ProfilePublicView(LoginRequiredMixin, TemplateView):
    template_name = "users/public_profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfilePublicView, self).get_context_data(**kwargs)
        if 'uid' in self.kwargs:
            user_id = self.kwargs['uid']

            user = User.objects.get(id=user_id)
            total_hours = user.profile.get_total_hours()
            
            context['has_upgraded'] = user.profile.has_upgraded
            context['clean_champion_clean_teams'] = CleanChampion.objects.filter(user_id=user_id)
            context['total_hours'] = total_hours
            context['user_profile'] = get_object_or_404(User, id=user_id)
            if user.profile.focus is None:
                context['focus']=user.profile.focus
            else:
                all_categories= users.forms.ORG_CATEGORIES
                print all_categories[0][0]
                labeled_selected_categories=''
                selected_categories=context['user_profile'].profile.focus.split(',')
                for t in all_categories:
                    if t[0] in selected_categories:
                        labeled_selected_categories+=t[1]
                        labeled_selected_categories+=" ,   "
                        labeled_selected_categories=labeled_selected_categories[0:len(labeled_selected_categories)-1]
                        context['focus']=labeled_selected_categories
                        print labeled_selected_categories
            
            try:
                context['community'] = Community.objects.get(id=UserCommunityMembership.objects.get(user=user_id).community_id)
            except:
                context['community'] = None
                
        context['user'] = self.request.user
        return context

class ProfileView(LoginRequiredMixin, FormView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = "/users/profile"

    def get_initial(self):
        user = self.request.user
        if 'referral_token' in self.request.session:
            user.profile.set_referral_token(self.request.session.get('referral_token'))
            user.profile.save()
            del self.request.session['referral_token']

        initial = {}
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email
        initial['about'] = user.profile.about
        initial['emergency_phone'] = user.profile.emergency_phone
        initial['dob'] = user.profile.dob
        initial['category'] = user.profile.category
        initial['emergency_contact_fname'] = user.profile.emergency_contact_fname
        initial['emergency_contact_lname'] = user.profile.emergency_contact_lname
        initial['street_address'] = user.profile.street_address
        initial['city'] = user.profile.city
        initial['province'] = user.profile.province
        initial['country'] = user.profile.country
        initial['postal_code'] = user.profile.country
        if user.profile.focus is None:
            initial['focus']=user.profile.focus
        else:
            categories= [str(x) for x in user.profile.focus.split(',')]
            initial['focus'] = categories
            
        if user.profile.website:
            initial['website'] = user.profile.website

        community_memberships = UserCommunityMembership.objects.filter(user=user.id)
        community_membership_requests = UserCommunityMembershipRequest.objects.filter(user=user.id)

        if community_memberships:
            initial['community'] = community_memberships[0].community.name
        elif community_membership_requests:
            initial['community'] = community_membership_requests[0].community.name
        else:
            initial['community'] = ''

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
        user = User.objects.get(id=self.request.user.id)
        picture = form.cleaned_data['picture']
        resume = form.cleaned_data['resume']
        community_name = form.cleaned_data['community']
        if community_name and not community_name == "":
            community = Community.objects.get(name=community_name)
        else:
            community = None

        #  Request an invitation to join the community if necessary
        if community:
            previous_memberships = UserCommunityMembership.objects.filter(user=user.id)
            previous_memberships_requests = UserCommunityMembershipRequest.objects.filter(user=user.id)
            #  Remove any previous membership request
            previous_memberships_requests.delete()
            if not previous_memberships:
                membership_request = UserCommunityMembershipRequest()
                membership_request.user_id = user.id
                membership_request.community_id = community.id
                membership_request.save()
        
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        user.profile.street_address = form.cleaned_data['street_address']
        user.profile.city = form.cleaned_data['city']
        user.profile.province = form.cleaned_data['province']
        user.profile.country = form.cleaned_data['country']
        user.profile.postal_code = form.cleaned_data['postal_code']
        user.profile.about = form.cleaned_data['about']
        user.profile.website = form.cleaned_data['website']
        user.profile.emergency_phone = form.cleaned_data['emergency_phone']
        user.profile.dob = form.cleaned_data['dob']
        user.profile.category = form.cleaned_data['category']
        user.profile.emergency_contact_fname = form.cleaned_data['emergency_contact_fname']
        user.profile.emergency_contact_lname = form.cleaned_data['emergency_contact_lname']
	user.profile.focus =','.join( form.cleaned_data['focus'])
	print user.profile.focus
        if picture:
            key = 'uploads/user_picture_%s_%s' % (str(user.id), picture)
            uploadFile = UploadFileToS3()
            user.profile.picture = uploadFile.upload(key, picture)

        if resume:
            key = 'uploads/user_resume_%s_%s' % (str(user.id), resume)
            uploadFile = UploadFileToS3()
            user.profile.resume = uploadFile.upload(key, resume)

        user.profile.save()

        if user.profile.about and user.profile.category and user.profile.city and user.profile.country and user.profile.emergency_contact_fname and user.profile.emergency_contact_lname and user.profile.picture:
            task = ProfileTask.objects.get(name="profile")
            user.profile.complete_level_task(task)
            user.profile.add_clean_creds(5)

        return HttpResponseRedirect('/users/profile/%s' % str(user.id))

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['community_search_url'] = self.request.build_absolute_uri("../../clean-team/community-search/?search=")
        return context

class SettingsView(LoginRequiredMixin, FormView):
    template_name = "users/settings.html"
    form_class = SettingsForm
    success_url = "/users/settings"

    def get_initial(self):
        settings = self.request.user.profile.settings

        initial = {}
        initial['communication_language'] = settings.communication_language
        initial['email_privacy'] = settings.email_privacy
        initial['data_privacy'] = settings.data_privacy
        initial['receive_newsletters'] = settings.receive_newsletters
        initial['timezone'] = settings.timezone
        return initial

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        user = self.request.user

        if form.cleaned_data['data_privacy'] == "True":
            user.profile.settings.data_privacy = 1
        else:
            user.profile.settings.data_privacy = 0

        if form.cleaned_data['email_privacy'] == "True":
            user.profile.settings.email_privacy = 1
        else:
            user.profile.settings.email_privacy = 0

        if form.cleaned_data['receive_newsletters'] == "True":
            user.profile.settings.receive_newsletters = 1
        else:
            user.profile.settings.receive_newsletters = 0

        user.profile.settings.timezone = form.cleaned_data['timezone']
        user.profile.settings.communication_language = form.cleaned_data['communication_language']
        user.profile.settings.save()

        challenge_articipants = ChallengeParticipant.objects.filter(user=self.request.user, status="approved")
        for cp in challenge_articipants:
            cp.receive_email = self.request.POST.get(str(cp.id), False)
            cp.save()

        context = self.get_context_data(**kwargs)
        context['form'] = form

        return HttpResponseRedirect('/users/profile/%s' % str(user.id))

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        context['receive_emails'] = ChallengeParticipant.objects.filter(user=self.request.user, status="approved")
        return context

class UpgradeAccountView(LoginRequiredMixin, FormView):
    template_name = "users/upgrade_account.html"
    form_class = UpgradeAccountForm
    success_url = "/"

    def get_initial(self):
        initial = super(UpgradeAccountView, self).get_initial()
        return initial

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        upgrade_type = self.request.POST.get('upgrade_type', None)
        if upgrade_type == "community":
          self.request.user.profile.has_upgraded = True
          self.request.user.profile.save()
        elif upgrade_type == "manager":
          self.request.user.profile.clean_team_member.role = "manager"
          self.request.user.profile.clean_team_member.save()
          self.request.user.profile.save()
        else:
          raise Exception("Unknown upgrade type.")
        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super(UpgradeAccountView, self).get_context_data(**kwargs)
        context['clean_team_member_id'] = self.request.user.profile.clean_team_member
        context['has_upgraded'] = self.request.user.profile.has_upgraded
        context['is_manager'] = CleanTeamMember.objects.filter(user_id=self.request.user.id,role="manager").count() > 0
        return context

class QRCodeView(LoginRequiredMixin, TemplateView):
    template_name = "users/qr_code.html"

    def get_context_data(self, **kwargs):
        context = super(QRCodeView, self).get_context_data(**kwargs)

        context['qr_code'] = UserQRCode.objects.get(user=self.request.user)

        return context

class PrintableCardView(LoginRequiredMixin, TemplateView):
    template_name = "users/printable_card.html"

    def get_context_data(self, **kwargs):
        context = super(PrintableCardView, self).get_context_data(**kwargs)

        context['qr_code'] = UserQRCode.objects.get(user=self.request.user)

        return context

class ReportCardView(TemplateView):
    template_name = "users/report_card.html"

    def get_context_data(self, **kwargs):
        context = super(ReportCardView, self).get_context_data(**kwargs)
        challenges = self.request.user.profile.get_my_challenges()
        
        # print challenges[0]['posted_challenges']
        # print challenges[1]
        # print challenges[2]
        # print challenges[3]

        context['challenges'] = challenges

        return context

class PrintableReportCardView(TemplateView):
    template_name = "users/printable_report_card.html"

    def get_context_data(self, **kwargs):
        context = super(PrintableReportCardView, self).get_context_data(**kwargs)
        challenges = self.request.user.profile.get_my_challenges()
        
        context['challenges'] = challenges

        return context

class LeaderboardView(TemplateView):
    template_name = "users/leaderboard.html"

    def get_context_data(self, **kwargs):
        context = super(LeaderboardView, self).get_context_data(**kwargs)

        individual_leaders = UserProfile.objects.filter(clean_creds__gte=1, user__is_superuser=False, user__is_staff=False).order_by('-clean_creds')[:10]
        clean_team_leaders = CleanTeam.objects.filter(clean_creds__gte=1, admin=False).order_by('-clean_creds')[:10]

        context['individual_leaders'] = individual_leaders
        context['clean_team_leaders'] = clean_team_leaders
        context['user'] = self.request.user
        return context

def follow_on_twitter(request):
    if request.method == "POST" and request.is_ajax:
        user = request.user

        if user.profile.has_clean_team():
            if user.profile.clean_team_member.clean_team.level.name == "Sprout":
                task = CleanTeamLevelTask.objects.get(name="follow_twitter")
                user.profile.clean_team_member.clean_team.complete_level_task(task)

    return HttpResponse(True)

class ProfileProgressView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile_progress.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileProgressView, self).get_context_data(**kwargs)
        user = self.request.user


        profile_tasks = ProfileTask.objects.filter(profile_phase=user.profile.phase)
        for task in profile_tasks:
            if not ProfileProgress.objects.filter(user=user , profile_task=task):
                profileprogress = ProfileProgress()
                profileprogress.user = user
                profileprogress.phase = ProfilePhase.objects.get(id=user.profile.phase)
                profileprogress.profile_task = task
                profileprogress.save()

        tasks = ProfileProgress.objects.filter(user=user , profile_task__in=profile_tasks)

        context['tasks'] = tasks
        context['user'] = user

        return context
