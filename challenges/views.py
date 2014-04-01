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

from django.utils.timezone import utc

from django.views.generic import *
from django.views.generic.base import View

from challenges.forms import *
from challenges.models import *
from cleanteams.models import CleanTeamMember, CleanChampion
from userprofile.models import UserProfile
from mycleancity.actions import *
from mycleancity.mixins import LoginRequiredMixin

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

def participate_in_challenge(request):
	if request.method == 'POST':
		cid = request.POST['cid']
		challenge = Challenge.objects.get(id=cid)
		
		try:
			user_challenge = UserChallenge.objects.get(user=request.user, challenge=challenge)
		except Exception, e:
			user_challenge = UserChallenge(user=request.user)
			user_challenge.challenge = challenge
			user_challenge.save()

			print e

		if request.user.profile.clean_team_member.clean_team.level.name == "Tree":
			count_challenges = UserChallenge.objects.filter(user=request.user, challenge__national_challenge=True).count()

			if count_challenges > 1:
				task = CleanTeamLevelTask.objects.get(name="2_national_challenges_signup")
				self.clean_team.complete_level_task(task)

	return HttpResponseRedirect('/challenges/%s' % str(cid))

@login_required
def one_time_check_in(request, cid, token):
	user = request.user
	
	challenge = get_object_or_404(Challenge, id=cid)
	challenge.one_time_check_in_with_token(user, token)
	
	return HttpResponseRedirect('/challenges/my-challenges')

@login_required
def check_in_check_out(request):
	if request.method == "POST" and request.is_ajax:
		cid = request.POST['cid']
		uid = request.POST['uid']

		challenge = get_object_or_404(Challenge, id=cid)
		response = challenge.check_in_check_out(uid)

		if response:
			return HttpResponse(response, content_type="text/html")

		return HttpResponse('')

def dropdown_search_for_challenges(request):
	
	query = request.GET['q']
	national_challenges = request.GET['national_challenges']

	challenges = Challenge.search_challenges(query, national_challenges, 10)
	challenges_json = Challenge.search_results_to_json(challenges)

	if challenges_json != "{}":
		return HttpResponse(challenges_json)
			
	return HttpResponse(False)

class ChallengesFeedView(TemplateView):
	template_name = "challenges/challenge_centre.html"

	def get(self, request, *args, **kwargs):
		query = ""
		national_challenges = False
		
		if 'q' in request.GET:
			query = request.GET['q']
		
		if 'national_challenges' in request.GET:
			national_challenges = request.GET['national_challenges']

		challenges = Challenge.search_challenges(query, national_challenges)			

		return render(request, self.template_name, {'challenges': challenges})

	def get_context_data(self, **kwargs):
		context = super(ChallengesFeedView, self).get_context_data(**kwargs)
		context['challenges'] = Challenge.objects.all()

		return context

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
		initial['event_date'] = challenge.event_date
		initial['event_time'] = challenge.event_time
		initial['address1'] = challenge.address1
		initial['address2'] = challenge.address2
		initial['city'] = challenge.city
		initial['province'] = challenge.province
		initial['country'] = challenge.country
		initial['postal_code'] = challenge.postal_code
		initial['description'] = challenge.description
		initial['host_organization'] = challenge.host_organization
		initial['type'] = challenge.type
		initial['national_challenge'] = challenge.national_challenge
		initial['challenge_id'] = challenge.id

		return initial

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		return self.render_to_response(context)

	def form_valid(self, form):
		challenge = Challenge.objects.get(id=form.cleaned_data['challenge_id'])
		challenge.title = form.cleaned_data['title']
		challenge.event_date = form.cleaned_data['event_date']
		challenge.event_time = form.cleaned_data['event_time']
		challenge.address1 = form.cleaned_data['address1']
		challenge.address2 = form.cleaned_data['address2']
		challenge.city = form.cleaned_data['city']
		challenge.postal_code = form.cleaned_data['postal_code']
		challenge.province = form.cleaned_data['province']
		challenge.country = form.cleaned_data['country']
		challenge.description = form.cleaned_data['description']
		challenge.host_organization = form.cleaned_data['host_organization']
		
		if form.cleaned_data['type'] is not None:
			challenge.type = form.cleaned_data['type']
			print True
		else:
			challenge.type = ChallengeType.objects.get(id=1)
			print False
			
		challenge.national_challenge = form.cleaned_data['national_challenge']
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

			participants = UserChallenge.objects.raw("SELECT id, user_id, challenge_id, max(time_in) AS time_in FROM challenges_userchallenge WHERE challenge_id = %s GROUP BY user_id, challenge_id" % (cid))

			context['participants'] = participants
			context['cid'] = cid
			context['challenge'] = challenge

		return context

class MyChallengesView(LoginRequiredMixin, TemplateView):
	template_name = "challenges/my_challenges.html"
	
	def get_context_data(self, **kwargs):
		context = super(MyChallengesView, self).get_context_data(**kwargs)

		if self.request.user.profile.is_clean_ambassador():
			try:
				ctm = CleanTeamMember.objects.get(user=self.request.user, role="clean-ambassador", status="approved")
				context['posted_challenges'] = Challenge.objects.filter(clean_team=ctm.clean_team).order_by("event_date")
			except Exception, e:
				print e

		context['user_challenges'] = UserChallenge.objects.filter(user=self.request.user).order_by("time_in")
		context['user'] = self.request.user

		return context

class ChallengeView(TemplateView):
	template_name = "challenges/challenge_details.html"	

	def get_object(self):
		return get_object_or_404(User, pk=self.request.user.id)

	def get_context_data(self, **kwargs):
		context = super(ChallengeView, self).get_context_data(**kwargs)

		if 'cid' in self.kwargs:
			cid = self.kwargs['cid']
			challenge = get_object_or_404(Challenge, id=cid)
			
			context['challenge'] = challenge
			
			try:
				context['user_challenge'] = UserChallenge.objects.get(user=self.request.user, challenge=challenge)
			except Exception, e:
				print e
				pass
			
			participants = UserChallenge.objects.raw("SELECT id, user_id FROM challenges_userchallenge WHERE challenge_id = %s GROUP BY user_id, challenge_id" % (cid))
			
			context['participants'] = participants
			context['page_url'] = self.request.get_full_path()

		context['user'] = self.request.user
		return context