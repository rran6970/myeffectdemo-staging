import os
import csv
import datetime
import json

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.mail import EmailMessage
from django.utils.timezone import utc

from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic.base import View

from challenges.forms import *
from challenges.models import *
from cleanteams.models import CleanTeamMember, CleanChampion, Community
from userprofile.models import UserProfile
from mycleancity.actions import *
from mycleancity.mixins import LoginRequiredMixin

@login_required
def export_challenge_data(request, cid):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    if request.is_ajax:
        challenge = get_object_or_404(Challenge, id=cid)
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (challenge.title)

        if challenge.clean_team_only:
            challenge_participants = CleanTeamChallenge.objects.filter(challenge=challenge)

            writer.writerow(['Change Team ID', 'Team Name', 'Contact Person First Name', 'Contact Person Last Name', 'Contact Person Email', 'Date/Time (UTC) Signed Up for Challenge', 'Date/Time (UTC) Checked In', 'Date/Time (UTC) Checked Out', 'Total Hours', 'Total Change Creds'])

            for participant in challenge_participants:
                writer.writerow([participant.clean_team.id, participant.clean_team.name, participant.clean_team.contact_user.first_name, participant.clean_team.contact_user.last_name, participant.clean_team.contact_user.email, participant.timestamp, participant.time_in, participant.time_out, participant.total_hours, participant. total_clean_creds])
        else:
            challenge_participants = UserChallengeEvent.objects.filter(Q(challenge=challenge))

            writer.writerow(['User ID', 'First Name', 'Last Name', 'Email', 'Date/Time (UTC) Signed Up for Challenge', 'Date/Time (UTC) Checked In', 'Date/Time (UTC) Checked Out', 'Total Hours', 'Total Change Creds'])

            for participant in challenge_participants:
                if participant.user.profile.settings.data_privacy:
                    first_name = participant.user.first_name
                    last_name = participant.user.last_name
                else:
                    first_name = ""
                    last_name = ""

                email = participant.user.email

                writer.writerow([participant.user.id, first_name, last_name, email, participant.timestamp, participant.time_in, participant.time_out, participant.total_hours, participant. total_clean_creds])

    return response

@login_required
def survey_update_score(request):
    if request.is_ajax:
        aid = request.GET['aid']

        try:
            answer = int(aid)
            answer = QuestionAnswer.objects.get(id=answer)

            return HttpResponse(answer.get_answer_score())
        except Exception, e:
            print e

    return HttpResponse('')

@login_required
def participate_in_challenge(request):
    if request.method == 'POST':
        cid = request.POST['cid']
        message = request.POST.get('messgage', None)
        user = request.user

        challenge = Challenge.objects.get(id=cid)

        if 'staples_store' in request.POST:
            staples_store = request.POST['staples_store']
            staples_store = StaplesStores.objects.get(id=staples_store)

            participate = challenge.participate_in_challenge(user, message, staples_store)

            if not participate:
                return HttpResponseRedirect('/challenges/%s/?error=store_taken' % str(cid))
        else:
            challenge.participate_in_challenge(user, message)

    return HttpResponseRedirect('/challenges/%s' % str(cid))

@login_required
def unparticipate_in_challenge(request):
    if request.method == 'POST':
        cid = request.POST['cid']
        user = request.user

        challenge = Challenge.objects.get(id=cid)
        challenge.unparticipate_in_challenge(user)

    return HttpResponseRedirect('/challenges/%s' % str(cid))

# This is only called through the QR Code scanning...I think
def one_time_check_in(request, cid, token):
    user = request.user

    challenge = get_object_or_404(Challenge, id=cid)
    challenge.one_time_check_in_with_token(user, token)

    return HttpResponseRedirect('/challenges/my-challenges')

@login_required
def check_in_check_out(request):
    if request.method == "POST" and request.is_ajax:
        challenge_id = request.POST['challenge_id']
        participant_id = request.POST['participant_id']

        challenge = get_object_or_404(Challenge, id=challenge_id)

        if 'manual_clean_creds' in request.POST and 'manual_hours' in request.POST:
            manual_clean_creds = int(request.POST['manual_clean_creds'])
            manual_hours = int(request.POST['manual_hours'])
            response = challenge.check_in_check_out(participant_id, manual_clean_creds, manual_hours)
        else:
            response = challenge.check_in_check_out(participant_id)

        if response:
            return HttpResponse(response, content_type="text/html")

        return HttpResponse('')

@login_required
def check_out_all(request):
    challenge_id = request.POST['challenge_id']
    challenge = get_object_or_404(Challenge, id=challenge_id)
    challenge.check_out_all()

    return HttpResponseRedirect('/challenges/participants/%s/' % (challenge_id))

def dropdown_search_for_challenges(request):
    query = request.GET['q']
    city = request.GET['city']
    tag = request.GET['tag']
    title = request.GET['title']
    cat = request.GET['cat']
    national_challenges = request.GET['national_challenges']
    clean_team_only = request.GET['clean_team_only']
    if query:
        challenges = Challenge.search_challenges(query, national_challenges, clean_team_only, 10)
    else:
        challenges = Challenge.advenced_search_challenges(city, tag, title, cat, national_challenges, clean_team_only, 10)
    challenges_json = Challenge.search_results_to_json(challenges)

    if challenges_json != "{}":
        return HttpResponse(challenges_json)

    return HttpResponse(False)

class ChallengeCentreView(TemplateView):
    template_name = "challenges/challenge_centre.html"

    def get(self, request, *args, **kwargs):
        query = ""
        city = ""
        tag = ""
        title = ""
        cat = ""
        national_challenges = False
        clean_team_only = False

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                if 'city' in request.GET:
                    city = request.GET['city']
                if 'tag' in request.GET:
                    tag = request.GET['tag']
                if 'title' in request.GET:
                    title = request.GET['title']
                if 'cat' in request.GET:
                    cat = request.GET['cat']
        if 'national_challenges' in request.GET:
            national_challenges = request.GET['national_challenges']

        if 'clean_team_only' in request.GET:
            clean_team_only = request.GET['clean_team_only']

        if city or tag or title or cat:
            challenges = Challenge.advenced_search_challenges(city, tag, title, cat, national_challenges, clean_team_only)
        else:
            challenges = Challenge.search_challenges(query, national_challenges, clean_team_only)
        skilltags = ChallengeSkillTag.objects.filter(challenge__in=challenges)

        if self.request.user.is_authenticated():
            my_community = None
            my_team = None
            communities = Community.objects.filter(owner_user=self.request.user)
            if communities.count():
                my_community = communities[0]
            if self.request.user.profile.clean_team_member:
                my_team = self.request.user.profile.clean_team_member.clean_team
            if my_community:
                community_approved_challenges = set(m.challenge_id for m in ChallengeCommunityMembership.objects.filter(community=my_community.id))
            if my_team:
                team_approved_challenges = set(m.challenge_id for m in ChallengeTeamMembership.objects.filter(clean_team=my_team.id))

        return render(request, self.template_name, {'challenges': challenges, 'skilltags': skilltags, 'my_team': my_team, 'my_community': my_community, 'community_approved_challenges': community_approved_challenges, 'team_approved_challenges': team_approved_challenges})

    def get_context_data(self, **kwargs):
        context = super(ChallengeCentreView, self).get_context_data(**kwargs)
        context['challenges'] = Challenge.objects.all().order_by('-promote_top')

        return context

class VoucherView(LoginRequiredMixin, FormView):
    template_name = "challenges/voucher_code.html"
    form_class = UserVoucherForm
    success_url = "mycleancity/index.html"

    def get_initial(self):
        initial = {}
        initial['user_id'] = self.request.user.id

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
        context = self.get_context_data(**kwargs)

        voucher_code = form.cleaned_data['voucher']
        user = self.request.user

        voucher = Voucher.objects.get(voucher=voucher_code)
        voucher.claim_voucher(user)

        return HttpResponseRedirect(u'/users/profile/%s' % (user.id))

class HMVoucherView(LoginRequiredMixin, FormView):
    template_name = "challenges/hm_voucher_code.html"
    form_class = UserVoucherForm
    success_url = "mycleancity/index.html"

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)

        voucher_code = form.cleaned_data['voucher']
        user = self.request.user

        try:
            voucher = UserVoucher.objects.get(voucher=voucher_code, user__isnull=True)
            voucher.claim_voucher(user)
        except Exception, e:
            raise e

        return HttpResponseRedirect(u'/challenges/my-challenges/')

class NewChallengeView(LoginRequiredMixin, FormView):
    template_name = "challenges/new_challenge.html"
    form_class = NewChallengeForm
    success_url = "mycleancity/index.html"

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if not self.request.user.is_active:
            return HttpResponseRedirect('/challenges')

        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        challenge = Challenge()
        challenge.new_challenge(self.request.user, form.cleaned_data)

        context = self.get_context_data(**kwargs)
        context['form'] = form

        return HttpResponseRedirect(u'/challenges/%s' %(challenge.id))

    def get_context_data(self, **kwargs):
        context = super(NewChallengeView, self).get_context_data(**kwargs)
        context['skill_tags'] = SkillTag.objects.all()

        return context

class NewActionSurveyView(LoginRequiredMixin, FormView):
    template_name = "challenges/new_challenge_survey.html"
    form_class = NewActionSurveyForm
    success_url = "mycleancity/index.html"

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if not self.request.user.is_active:
            return HttpResponseRedirect('/challenges')

        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        survey = UserChallengeSurvey()
        survey.create_survey(self.request.user, form.cleaned_data)

        return HttpResponseRedirect(u'/challenges/new-challenge/')

class EditChallengeView(LoginRequiredMixin, FormView):
    template_name = "challenges/edit_challenge.html"
    form_class = EditChallengeForm
    success_url = "mycleancity/index.html"

    def get_initial(self):
        if 'cid' in self.kwargs:
            cid = self.kwargs['cid']

        try:
            challenge = Challenge.objects.get(id=cid)
        except Exception, e:
            print e

        initial = {}
        initial['title'] = challenge.title
        initial['event_start_date'] = challenge.event_start_date
        initial['event_start_time'] = challenge.event_start_time
        initial['event_end_date'] = challenge.event_end_date
        initial['event_end_time'] = challenge.event_end_time
        initial['address1'] = challenge.address1
        initial['address2'] = challenge.address2
        initial['city'] = challenge.city
        initial['province'] = challenge.province
        initial['country'] = challenge.country
        initial['postal_code'] = challenge.postal_code
        initial['description'] = challenge.description
        initial['link'] = challenge.link

        if challenge.organization == self.request.user.profile.clean_team_member.clean_team.name:
            initial['host_is_clean_team'] = True

        initial['organization'] = challenge.organization
        initial['contact_first_name'] = challenge.contact_first_name
        initial['contact_last_name'] = challenge.contact_last_name
        initial['contact_phone'] = challenge.contact_phone
        initial['contact_email'] = challenge.contact_email

        initial['type'] = challenge.type
        initial['national_challenge'] = challenge.national_challenge
        initial['clean_team_only'] = challenge.clean_team_only
        initial['challenge_id'] = challenge.id

        return initial

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form):
        challenge = Challenge.objects.get(id=form.cleaned_data['challenge_id'])
        challenge.title = form.cleaned_data['title']
        challenge.event_start_date = form.cleaned_data['event_start_date']
        challenge.event_start_time = form.cleaned_data['event_start_time']
        challenge.event_end_date = form.cleaned_data['event_end_date']
        challenge.event_end_time = form.cleaned_data['event_end_time']
        challenge.address1 = form.cleaned_data['address1']
        challenge.address2 = form.cleaned_data['address2']
        challenge.city = form.cleaned_data['city']
        challenge.postal_code = form.cleaned_data['postal_code']
        challenge.province = form.cleaned_data['province']
        challenge.country = form.cleaned_data['country']
        challenge.description = form.cleaned_data['description']
        challenge.link = form.cleaned_data['link']

        challenge.organization = form.cleaned_data['organization']
        challenge.contact_first_name = form.cleaned_data['contact_first_name']
        challenge.contact_last_name = form.cleaned_data['contact_last_name']
        challenge.contact_phone = form.cleaned_data['contact_phone']
        challenge.contact_email = form.cleaned_data['contact_email']

        if form.cleaned_data['type'] is not None:
            challenge.type = form.cleaned_data['type']
        else:
            challenge.type = ChallengeType.objects.get(id=1)

        challenge.national_challenge = form.cleaned_data['national_challenge']
        challenge.clean_team_only = form.cleaned_data['clean_team_only']
        challenge.last_updated_by = self.request.user
        challenge.save()

        return HttpResponseRedirect(u'/challenges/%s' %(challenge.id))

    def get_context_data(self, **kwargs):
        context = super(EditChallengeView, self).get_context_data(**kwargs)

        if 'cid' in self.kwargs:
            cid = self.kwargs['cid']

        try:
            challenge = Challenge.objects.get(id=cid)

            #TODO: Shouldn't be able to access all Challenges
            if self.request.user.profile.is_clean_ambassador and self.request.user.profile.clean_team_member.clean_team == challenge.clean_team:

                pass
            else:
                context = None
                return context
        except Exception, e:
            print e
            return HttpResponseRedirect(u'/challenges/%s' %(cid))

        return context

class ChallengeParticipantsView(LoginRequiredMixin, TemplateView):
    template_name = "challenges/challenge_participants.html"

    def get_context_data(self, **kwargs):
        context = super(ChallengeParticipantsView, self).get_context_data(**kwargs)

        if 'cid' in self.kwargs:
            cid = self.kwargs['cid']
            challenge = get_object_or_404(Challenge, id=cid)
            user = self.request.user

            if not user.profile.is_clean_ambassador():
                context = None
                return context
            elif challenge.clean_team != user.profile.clean_team_member.clean_team:
                context = None
                return context

            participants = challenge.get_participants_to_check_in()

            context['participants'] = participants
            context['cid'] = cid
            context['challenge'] = challenge

        return context

class ChallengeParticipantManageView(LoginRequiredMixin, TemplateView):
    template_name = "challenges/participants_manage.html"

    def get_context_data(self, **kwargs):
        context = super(ChallengeParticipantManageView, self).get_context_data(**kwargs)

        if 'cid' in self.kwargs:
            cid = self.kwargs['cid']
            challenge = get_object_or_404(Challenge, id=cid)
            user = self.request.user

            if not user.profile.is_clean_ambassador():
                context = None
                return context
            elif challenge.clean_team != user.profile.clean_team_member.clean_team:
                context = None
                return context

            participants = challenge.get_all_participants()
            approvedparticipants = challenge.get_participants()

            context['participants'] = participants
            context['count'] = sum(1 for p in approvedparticipants)
            context['cid'] = cid
            context['challenge'] = challenge

        return context

class ChallengeParticipantEmailView(LoginRequiredMixin, FormView):
    template_name = "challenges/participants_email.html"
    form_class = ParticipantEmailForm
    success_url = "challenges/participants_email.html"

    def get_initial(self):
        initial = {}
        emailfile = open(os.path.join(settings.BASE_DIR, 'templates/emails/email_defualt.html'))
        message=emailfile.read()
        initial['message'] = message

        return initial

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        cid = self.kwargs['cid']
        challenge = get_object_or_404(Challenge, id=cid)
        user = self.request.user
        if user.profile.is_clean_ambassador() and challenge.clean_team == user.profile.clean_team_member.clean_team:
            from_email = self.request.user.email
            to_email = []
            for leader in CleanTeamMember.objects.filter(clean_team=challenge.clean_team, status="approved"):
                to_email.append(leader.user.email)
            approvedparticipants = challenge.get_participants()
            for p in approvedparticipants:
                to_email.append(p.user.email)
            mail = EmailMessage(subject, message, from_email, to_email)
            mail.content_subtype = "html"
            mail.send()
            self.request.session['email_sent_success'] = True
        return HttpResponseRedirect(u'/challenges/participants-email/%s' %(challenge.id))

    def get_context_data(self, **kwargs):
        context = super(ChallengeParticipantEmailView, self).get_context_data(**kwargs)

        if 'cid' in self.kwargs:
            cid = self.kwargs['cid']
            challenge = get_object_or_404(Challenge, id=cid)
            user = self.request.user

            if not user.profile.is_clean_ambassador():
                context = None
                return context
            elif challenge.clean_team != user.profile.clean_team_member.clean_team:
                context = None
                return context

            if self.request.session.get('email_sent_success', False):
                context['success'] = True
                del self.request.session['email_sent_success']

            approvedparticipants = challenge.get_participants()

            context['participants'] = approvedparticipants
            context['count'] = sum(1 for p in approvedparticipants)
            context['cid'] = cid
            context['challenge'] = challenge

        return context

class MyChallengesView(LoginRequiredMixin, TemplateView):
    template_name = "challenges/my_challenges.html"

    def get_context_data(self, **kwargs):
        context = super(MyChallengesView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.profile.is_clean_ambassador():
            try:
                ctm = CleanTeamMember.objects.get(user=user, status="approved")
                context['posted_challenges'] = Challenge.objects.filter(clean_team=ctm.clean_team).order_by("event_start_date")
            except Exception, e:
                print e

            clean_team_challenges = CleanTeamChallenge.objects.filter(clean_team=user.profile.clean_team_member.clean_team).order_by("time_in")
            context['clean_team_challenges'] = clean_team_challenges

            try:
                staples_challenge = StaplesChallenge.get_participating_store(user.profile.clean_team_member.clean_team)
                print staples_challenge
                context['staples_challenge'] = staples_challenge
            except Exception, e:
                print e

        #user_challenges = UserChallengeEvent.objects.filter(user=user).order_by("time_in")
        user_challenges = ChallengeParticipant.objects.filter(user=user, status="approved")

        context['total_hours'] = user.profile.get_total_hours()
        context['user_challenges'] = user_challenges

        return context

class ChallengeView(TemplateView):
    template_name = "challenges/challenge_details.html"

    def get_context_data(self, **kwargs):
        context = super(ChallengeView, self).get_context_data(**kwargs)

        if 'cid' in self.kwargs:
            cid = self.kwargs['cid']
            challenge = get_object_or_404(Challenge, Q(url=cid) | Q(id=cid))
            user = self.request.user

            if 'error' in self.request.GET:
                context['error'] = "That store is already taken, please select another."

            if user.is_authenticated():
                user_challenge = challenge.get_participating_challenge(user)
                context['user_challenge'] = user_challenge
                context['can_unparticipate'] = challenge.can_unparticipate(user)

            participants = challenge.get_participants()

            # Only for the Staples CleanAct, have to find a more efficient way
            if challenge.url == "staples-cleanact":
                staples_challenge_participants = StaplesChallenge.objects.filter(clean_team__isnull=False).values_list('staples_store', flat=True)
                staples_stores = StaplesStores.objects.all().exclude(id__in=staples_challenge_participants)

                if user_challenge:
                    context['participating_store'] = StaplesChallenge.get_participating_store(user.profile.clean_team_member.clean_team)
                    context['user_challenge'] = user_challenge

                context['staples_stores'] = staples_stores
            skilltags = ChallengeSkillTag.objects.filter(challenge=challenge)
            if skilltags:
                context['skilltags'] = skilltags
            context['files'] = ChallengeUploadFile.objects.filter(challenge=challenge)
            context['challenge'] = challenge
            context['count'] = sum(1 for participant in participants)
            context['participants'] = participants
            context['page_url'] = self.request.get_full_path()
            if self.request.session.get('upload_error_msg', False):
                context['error_msg'] = self.request.session.get('upload_error_msg')
                del self.request.session['upload_error_msg']

        return context

def participant_action(request):
    if request.method == 'POST' and request.is_ajax:
        pid = request.POST['pid']
        action = request.POST['action']

        participant = ChallengeParticipant.objects.get(id=pid)

        if action == "approve":
            participant.status="approved"
            participant.save()
        elif action == "remove":
            participant.status="removed"
            participant.save()

    return HttpResponse("success")

def upload_action_form(request):
    if request.method == 'POST':
        challenge_id = request.POST['challenge_id']
        form = ChallengeUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            challenge_id = form.cleaned_data['challenge_id']
            upload_file = form.cleaned_data['upload_file']
            st = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            key = 'uploads/upload_file_%s_%s' % (st, upload_file)
            uploadFile = UploadFileToS3()
            fileUrl = uploadFile.upload(key, upload_file)
            challengeform = ChallengeUploadFile()
            challengeform.challenge_id = challenge_id
            challengeform.file_name = upload_file
            challengeform.upload_file = fileUrl
            challengeform.save()
        else:
            request.session['upload_error_msg'] = form.non_field_errors()

    return HttpResponseRedirect('/challenges/%s' % str(challenge_id))

def approve_challenge(request):
    if request.method == 'POST' and request.is_ajax:
        clean_team_id = request.POST.get('clean_team_id', None)
        community_id = request.POST.get('community_id', None)
        challenge_id = request.POST.get('challenge_id', None)

        if clean_team_id:
            challenge_team_membership = ChallengeTeamMembership()
            challenge_team_membership.clean_team_id = clean_team_id
            challenge_team_membership.challenge_id = challenge_id
            challenge_team_membership.save()

        if community_id:
            challenge_community_membership = ChallengeCommunityMembership()
            challenge_community_membership.community_id = community_id
            challenge_community_membership.challenge_id = challenge_id
            challenge_community_membership.is_private = False
            challenge_community_membership.save()

    return HttpResponse("success")
