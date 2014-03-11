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

from challenges.forms import *
from challenges.models import *
from cleanteams.models import CleanTeamMember, CleanChampion
from userprofile.models import UserProfile
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
	try:
		challenge = Challenge.objects.get(id=cid, token=token)

		user = request.user
		userchallenge, created = UserChallenge.objects.get_or_create(user=user, challenge_id=cid)
		challenge = userchallenge.challenge

		now = datetime.datetime.utcnow().replace(tzinfo=utc)
		total_clean_creds = challenge.clean_creds_per_hour

		userchallenge.time_in = now
		userchallenge.time_out = now
		userchallenge.total_hours = 0
		userchallenge.total_clean_creds = total_clean_creds
		userchallenge.save()

		# Add CleanCreds to individual
		user.profile.add_clean_creds(total_clean_creds)

		# Add CleanCreds to Clean Teams if applicable
		clean_champions = CleanChampion.objects.filter(user=user)

		for clean_champion in clean_champions:
			if clean_champion.status == "approved":
				clean_champion.clean_team.add_team_clean_creds(total_clean_creds)
				
		# Clean Ambassador
		if user.profile.is_clean_ambassador():
			user.profile.clean_team_member.clean_team.add_team_clean_creds(total_clean_creds)
		
		# Clean Team posting challenge	
		challenge.clean_team.add_team_clean_creds(total_clean_creds)
	except Exception, e:
		print e

	return HttpResponseRedirect('/challenges/my-challenges')

def check_in_check_out(request):
	if request.method == "POST" and request.is_ajax:
		cid = request.POST['cid']
		uid = request.POST['uid']

		try:
			userchallenge = UserChallenge.objects.get(user_id=uid, challenge_id=cid)
			user = userchallenge.user
			challenge = userchallenge.challenge

			if challenge.type.challenge_type == "hourly":
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
					total_hours = (diff.days * 24) + (diff.seconds // 3600)

					total_clean_creds = challenge.get_challenge_total_clean_creds(total_hours)

					userchallenge.total_hours = total_hours
					userchallenge.total_clean_creds = total_clean_creds
					userchallenge.save()

					# Add CleanCreds to individual
					user.profile.add_clean_creds(total_clean_creds)

					# Add CleanCreds to Clean Teams if applicable
					clean_champions = CleanChampion.objects.filter(user=user)

					for clean_champion in clean_champions:
						if clean_champion.status == "approved":
							clean_champion.clean_team.add_team_clean_creds(total_clean_creds)
							
					# Clean Ambassador
					if user.profile.is_clean_ambassador():
						user.profile.clean_team_member.clean_team.add_team_clean_creds(total_clean_creds)
					
					# Clean Team posting challenge	
					challenge.clean_team.add_team_clean_creds(total_clean_creds)

					return HttpResponse("%s Hours<br/>%s <span class='green bold'>Clean</span><span class='blue bold'>Creds</span>" % (str(total_hours), str(total_clean_creds)), content_type="text/html")
			else:
				now = datetime.datetime.utcnow().replace(tzinfo=utc)
				total_clean_creds = challenge.clean_creds_per_hour

				userchallenge.time_in = now
				userchallenge.time_out = now
				userchallenge.total_hours = 0
				userchallenge.total_clean_creds = total_clean_creds
				userchallenge.save()

				# Add CleanCreds to individual
				user.profile.add_clean_creds(total_clean_creds)

				# Add CleanCreds to Clean Teams if applicable
				clean_champions = CleanChampion.objects.filter(user=user)

				for clean_champion in clean_champions:
					if clean_champion.status == "approved":
						clean_champion.clean_team.add_team_clean_creds(total_clean_creds)
						
				# Clean Ambassador
				if user.profile.is_clean_ambassador():
					user.profile.clean_team_member.clean_team.add_team_clean_creds(total_clean_creds)
				
				# Clean Team posting challenge	
				challenge.clean_team.add_team_clean_creds(total_clean_creds)

				return HttpResponse('Confirmed', content_type="text/html")

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
		
		challenge.type = ChallengeType.object.get(id=1)
		# if form.cleaned_data['type'] is not None:
		# 	# challenge.type = form.cleaned_data['type']
		# 	print True
		# else:
		# 	print False
			
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

	def get(self, request, *args, **kwargs):
		challenge = None

		if 'cid' in self.kwargs:
			cid = self.kwargs['cid']
		else:
			return HttpResponseRedirect('/challenges/my-challenges/')

		try:
			challenge = Challenge.objects.get(id=cid, clean_team=self.request.user.profile.clean_team_member.clean_team)
		except Exception, e:
			print e
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

		# print self.request.user.profile.is_clean_ambassador()

		if self.request.user.profile.is_clean_ambassador():
			try:
				ctm = CleanTeamMember.objects.get(user=self.request.user, role="clean-ambassador", status="approved")
				context['posted_challenges'] = Challenge.objects.filter(clean_team=ctm.clean_team).order_by("event_date")
			except Exception, e:
				print e
				pass

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
			challenge = get_object_or_404(Challenge, id=cid)
			
			context['challenge'] = challenge
			
			try:
				context['user_challenge'] = UserChallenge.objects.get(user=self.request.user, challenge=challenge)
			except Exception, e:
				print e
				pass
			
			context['participants'] = UserChallenge.objects.filter(challenge=challenge)
			
			context['page_url'] = self.request.get_full_path()

		context['user'] = self.request.user
		return context