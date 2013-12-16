import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404

from django.utils.timezone import utc

from django.views.generic import *
from django.views.generic.base import View

from challenges.forms import NewChallengeForm
from challenges.models import Challenge, UserChallenge, ChallengeCategory
from userprofile.models import UserProfile
from mycleancity.mixins import LoginRequiredMixin

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

	return HttpResponseRedirect('/challenges/%s' % str(cid))

def check_in_check_out(request):
	if request.method == "POST" and request.is_ajax:
		cid = request.POST['cid']
		uid = request.POST['uid']

		try:
			userchallenge = UserChallenge.objects.get(user_id=uid, challenge_id=cid)
			user = User.objects.get(id=userchallenge.user_id)
			challenge = Challenge.objects.get(id=cid)

			if not userchallenge.time_in:
				now = datetime.datetime.utcnow().replace(tzinfo=utc)

				userchallenge.time_in = now
				userchallenge.save()
			else:
				# Get current time and time out time
				now = str(datetime.datetime.utcnow().replace(tzinfo=utc))
				userchallenge.time_out = now

				now_str = datetime.datetime.strptime(str(now)[:19], "%Y-%m-%d %H:%M:%S")
				time_in_str = datetime.datetime.strptime(str(userchallenge.time_in)[:19], "%Y-%m-%d %H:%M:%S")

				diff = now_str - time_in_str
				total_hours = diff.seconds // 3600

				userchallenge.total_hours = total_hours

				# Add Clean Team points
				user.profile.clean_creds += challenge.getChallengeCleanCreds()

				if user.profile.clean_team_member.status == "approved":
					user.profile.clean_team_member.clean_team.clean_creds += challenge.getChallengeCleanCreds()
				else:
					challenge.clean_team.clean_creds += challenge.getChallengeCleanCreds()

				userchallenge.save()

		except Exception, e:
			print e

		return HttpResponse('')

class ChallengesFeedView(TemplateView):
	template_name = "challenges/challenge_centre.html"

	def get_context_data(self, **kwargs):
		context = super(ChallengesFeedView, self).get_context_data(**kwargs)
		context['challenges'] = Challenge.objects.all()[:10]
		context['user'] = self.request.user

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

	def form_valid(self, form):
		challenge = Challenge(user=self.request.user)
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
		challenge.clean_team = self.request.user.profile.clean_team_member.clean_team
		challenge.save()

		challenge_category = ChallengeCategory()
		challenge_category.challenge = challenge
		challenge_category.category = form.cleaned_data['category']
		challenge_category.save()

		return HttpResponseRedirect('/challenges')

class ChallengeParticipantsView(LoginRequiredMixin, TemplateView):
	template_name = "challenges/challenge_participants.html"

	def get(self, request, *args, **kwargs):
		challenge = None

		if 'cid' in self.kwargs:
			cid = self.kwargs['cid']
		else:
			return HttpResponseRedirect('/challenges/my-challenges/')

		try:
			challenge = Challenge.objects.get(id=cid, user=self.request.user)
		except Exception, e:
			return HttpResponseRedirect('/challenges/my-challenges/')			

		return self.render_to_response(self.get_context_data())

	def get_context_data(self, **kwargs):
		context = super(ChallengeParticipantsView, self).get_context_data(**kwargs)

		if 'cid' in self.kwargs:
			cid = self.kwargs['cid']

			context['participants'] = UserChallenge.objects.filter(challenge_id=cid)
			context['cid'] = cid

		return context

class MyChallengesView(LoginRequiredMixin, TemplateView):
	template_name = "challenges/my_challenges.html"
	
	def get_context_data(self, **kwargs):
		context = super(MyChallengesView, self).get_context_data(**kwargs)

		context['posted_challenges'] = Challenge.objects.filter(user=self.request.user)
		context['user_challenges'] = UserChallenge.objects.filter(user=self.request.user)
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
			context['challenge'] = get_object_or_404(Challenge, id=cid)
			context['participants'] = UserChallenge.objects.filter(challenge_id=cid)
			context['page_url'] = self.request.get_full_path()

		context['user'] = self.request.user
		return context