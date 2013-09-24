from challenges.form import NewChallengeForm

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404

from django.views.generic import *
from django.views.generic.base import View
# from django.views.generic.base import TemplateView
# from django.views.generic.edit import FormView
# from django.views.generic.detail import DetailView

from challenges.models import Challenge, UserChallenge
from mycleancity.mixins import LoginRequiredMixin

def participate_in_challenge(request):
	if request.method == 'POST':
		cid = request.POST['cid']
		challenge = Challenge.objects.get(id=cid)
		
		user_challenge = UserChallenge(user=request.user)
		user_challenge.challenge = challenge
		user_challenge.save()

	return HttpResponseRedirect('/challenges')

class ChallengesFeedView(TemplateView):
	template_name = "challenges/challeges_feed.html"

	def get_context_data(self, **kwargs):
		context = super(ChallengesFeedView, self).get_context_data(**kwargs)
		context['challenges'] = Challenge.objects.all()[:10]

		return context

class NewChallengeView(LoginRequiredMixin, FormView):
	template_name = "challenges/new_challenge.html"
	form_class = NewChallengeForm
	success_url = "mycleancity/index.html"

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		return self.render_to_response(context)

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.

		challenge = Challenge(user=self.request.user)
		challenge.title = form.cleaned_data['title']
		challenge.event_date = form.cleaned_data['event_date']
		challenge.event_time = form.cleaned_data['event_time']
		challenge.cleancred_value = form.cleaned_data['cleancred_value']
		challenge.address1 = form.cleaned_data['address1']
		challenge.address2 = form.cleaned_data['address2']
		challenge.city = form.cleaned_data['city']
		challenge.postal_code = form.cleaned_data['postal_code']
		challenge.country = form.cleaned_data['country']
		challenge.save()

		return HttpResponseRedirect('/challenges/new-challenge')

class ChallengeParticipantsView(LoginRequiredMixin, TemplateView):
	template_name = "challenges/challenge_participants.html"

	def get_context_data(self, **kwargs):
		context = super(ChallengeParticipantsView, self).get_context_data(**kwargs)

		if 'cid' in self.kwargs:
			context['participants'] = UserChallenge.objects.filter(challenge_id=self.kwargs['cid'])

		return context

class ChallengeView(TemplateView):
	template_name = "challenges/challenge_details.html"
	model = Challenge

	def get_object(self):
		return get_object_or_404(User, pk=self.request.user.id)

	def get_context_data(self, **kwargs):
		context = super(ChallengeView, self).get_context_data(**kwargs)

		if 'cid' in self.kwargs:
			context['challenge'] = get_object_or_404(Challenge, id=self.kwargs['cid'])

		return context