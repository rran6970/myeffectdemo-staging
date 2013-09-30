from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404

from django.views.generic import *
from django.views.generic.base import View

from challenges.form import NewChallengeForm
from challenges.models import Challenge, UserChallenge
from userprofile.models import UserProfile
from mycleancity.mixins import LoginRequiredMixin

def participate_in_challenge(request):
	if request.method == 'POST':
		cid = request.POST['cid']
		challenge = Challenge.objects.get(id=cid)
		
		user_challenge = UserChallenge(user=request.user)
		user_challenge.challenge = challenge
		user_challenge.save()

	return HttpResponseRedirect('/challenges')

def confirm_participants(request):
	cid = 1
	if request.method == 'POST':
		cid = request.POST['cid']
		uids = request.POST.getlist('uids')
		participated = request.POST.getlist('participated')

		print uids
		print participated
		
		# for u in uids:
		# 	try:
		# 		userchallenge = UserChallenge.objects.get(user_id=u, challenge_id=cid, complete=False)
		# 		userchallenge.complete = True
		# 		userchallenge.save()

		# 		challenge = Challenge.objects.get(id=cid)
			
		# 		user = User.objects.get(id=userchallenge.user_id)
				
		# 		user_profile = UserProfile.objects.get(user=user)
		# 		user_profile.clean_creds += challenge.cleancred_value
		# 		user_profile.save()
		# 	except Exception, e:
		# 		pass
			
	return HttpResponseRedirect('/challenges/participants/%s' %(cid))


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

		if self.request.user.profile.organization != "":
			return HttpResponseRedirect('/challenges')

		return self.render_to_response(self.get_context_data(form=form))

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
			context['cid'] = self.kwargs['cid']

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

		context['user'] = self.request.user
		return context