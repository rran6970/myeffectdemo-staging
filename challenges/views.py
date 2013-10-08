from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404

from django.views.generic import *
from django.views.generic.base import View

from challenges.forms import NewChallengeForm
from challenges.models import Challenge, UserChallenge
from userorganization.models import UserOrganization
from userprofile.models import UserProfile
from mycleancity.mixins import LoginRequiredMixin

def participate_in_challenge(request):
	if request.method == 'POST':
		cid = request.POST['cid']
		challenge = Challenge.objects.get(id=cid)
		
		try:
			user_challenge = UserChallenge.objects.get(user=request.user, challenge=challenge)
			print user_challenge
		except Exception, e:
			user_challenge = UserChallenge(user=request.user)
			user_challenge.challenge = challenge
			user_challenge.save()

	return HttpResponseRedirect('/challenges/%s' % str(cid))

def confirm_participants(request):
	if request.method == 'POST' and request.is_ajax:
		cid = request.POST['cid']
		uid = request.POST['uid']
		participated = request.POST['participated']
		
		try:
			userchallenge = UserChallenge.objects.get(user_id=uid, challenge_id=cid)
			user = User.objects.get(id=userchallenge.user_id)
			challenge = Challenge.objects.get(id=cid)

			if participated == "true":
				userchallenge.complete = True
				user.profile.clean_creds += challenge.cleancred_value
			else:
				userchallenge.complete = False
				user.profile.clean_creds -= challenge.cleancred_value

			userchallenge.save()
			user.profile.save()
		except Exception, e:
			pass
			
	return HttpResponseRedirect('/challenges/')


class ChallengesFeedView(TemplateView):
	template_name = "challenges/challege_centre.html"

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

		try:
			organization = UserOrganization.objects.get(user=self.request.user)
		except Exception, e:
			organization = None

		if not organization:
			return HttpResponseRedirect('/challenges')

		if not self.request.user.is_active:
			return HttpResponseRedirect('/challenges')

		return self.render_to_response(self.get_context_data(form=form))

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		print form.errors
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

		print challenge

		challenge.save()

		return HttpResponseRedirect('/challenges')

class ChallengeParticipantsView(LoginRequiredMixin, TemplateView):
	template_name = "challenges/challenge_participants.html"

	def get_context_data(self, **kwargs):
		context = super(ChallengeParticipantsView, self).get_context_data(**kwargs)

		if 'cid' in self.kwargs:
			context['participants'] = UserChallenge.objects.filter(challenge_id=self.kwargs['cid'])
			context['cid'] = self.kwargs['cid']

		return context

class MyChallengesView(LoginRequiredMixin, TemplateView):
	template_name = "challenges/my_challenges.html"
	
	def get_context_data(self, **kwargs):
		context = super(MyChallengesView, self).get_context_data(**kwargs)

		context['challenges'] = Challenge.objects.filter(user=self.request.user)
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