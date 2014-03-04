import datetime
import math

from django.db import models
from django.contrib.auth.models import User

from cleanteams.models import CleanTeam, CleanTeamMember, CleanChampion, CleanTeamLevelTask

from notifications.models import Notification, UserNotification

from itertools import chain
"""
Name:           Challenge
Date created:   Sept 8, 2013
Description:    The challenge that each user will be allowed to created.
"""
class Challenge(models.Model):
	title = models.CharField(max_length=60, blank=False, verbose_name="Title")	
	event_date = models.DateField(blank=True, null=True)
	event_time = models.TimeField(blank=True, null=True)
	address1 = models.CharField(max_length=60, blank=False, verbose_name="Address")
	address2 = models.CharField(max_length=60, blank=True, verbose_name="Suite")
	city = models.CharField(max_length=60, blank=True, verbose_name='City')
	province = models.CharField(max_length=60, blank=True, verbose_name='Province')
	postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')
	country = models.CharField(max_length=60, blank=True, verbose_name='Country')
	description = models.TextField(blank=False, default="")
	host_organization = models.TextField(blank=True, null=True, default="")
	user = models.ForeignKey(User)
	clean_team = models.ForeignKey(CleanTeam, blank=True, null=True, default=-1)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	last_updated_by = models.ForeignKey(User, related_name='user_last_updated_by')
	clean_creds_per_hour = models.IntegerField(default=0)
	complete = models.BooleanField(default=False, verbose_name='Confirms the Challenge is created')

	class Meta:
		verbose_name_plural = u'Challenges'

	def __unicode__(self):
		return u'Challenge: %s' % self.title

	def new_challenge(self, user, form):
		self.user = user
		self.last_updated_by = user
		self.title = form['title']
		self.event_date = form['event_date']
		self.event_time = form['event_time']
		self.address1 = form['address1']
		self.address2 = form['address2']
		self.city = form['city']
		self.postal_code = form['postal_code']
		self.province = form['province']
		self.country = form['country']
		self.description = form['description']
		self.host_organization = form['host_organization']
		self.clean_team = user.profile.clean_team_member.clean_team
		self.save()

		survey = UserChallengeSurvey()
		survey.create_survey(self, form)		

		# Send notifications
		notification = Notification.objects.get(notification_type="challenge_posted")
		# The names that will go in the notification message template
		name_strings = [self.clean_team.name, self.title]
		link_strings = [str(self.id)]

		users_to_notify_str = notification.users_to_notify
		users_to_notify = users_to_notify_str.split(', ')

		# Notify all of the Users that have the roles within users_to_notify
		for role in users_to_notify:
			clean_team_members = CleanTeamMember.objects.filter(role=role, clean_team=self.clean_team, status="approved")

			members_list = list(clean_team_members)

			if role == "clean-champion":
				clean_champions = CleanChampion.objects.filter(clean_team=self.clean_team, status="approved")	

				members_list = list(chain(clean_team_members, clean_champions))

			for member in members_list:
				user_notification = UserNotification()
				user_notification.create_notification("challenge_posted", member.user, name_strings, link_strings)

		if self.clean_team.level.name == "Sprout":
			task = CleanTeamLevelTask.objects.get(name="1_challenge")
			self.clean_team.complete_level_task(task)

		elif self.clean_team.level.name == "Sapling":
			count_challenges = self.objects.filter(clean_team=self.clean_team).count()

			if count_challenges > 4:
				task = CleanTeamLevelTask.objects.get(name="5_challenges")
				self.clean_team.complete_level_task(task)

	def get_challenge_total_clean_creds(self, total_hours):
		return int(self.clean_creds_per_hour * total_hours)

	def save(self, *args, **kwargs):
		super(Challenge, self).save(*args, **kwargs)

"""
Name:           UserChallenge
Date created:   Sept 8, 2013
Description:    Will be used to keep track of all of the Users partcipating 
				within a challenge.
"""
class UserChallenge(models.Model):
	challenge = models.ForeignKey(Challenge)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	time_in	= models.DateTimeField(blank=True, null=True)
	time_out = models.DateTimeField(blank=True, null=True)
	total_hours = models.IntegerField(default=0)
	total_clean_creds = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = u'Challenges user participated in'

	def save(self, *args, **kwargs):
		super(UserChallenge, self).save(*args, **kwargs)

"""
Name:           CleanGrid
Date created:   Feb 3, 2014
Description:    The Clean Grid system for answer value calculation.
"""
class CleanGrid(models.Model):
	name = models.CharField(max_length=60, blank=False, default="None", verbose_name='Clean Grid Name')
	value = models.DecimalField(max_digits=10, decimal_places=6)

	class Meta:
		verbose_name_plural = u'Challenge question CleanGrid'

	def __unicode__(self):
		return u'CleanGrid: %s' %(self.name)

	def save(self, *args, **kwargs):
		super(CleanGrid, self).save(*args, **kwargs)

"""
Name:           ChallengeQuestionType
Date created:   Feb 3, 2014
Description:    The questions types.
"""
class ChallengeQuestionType(models.Model):
	name = models.CharField(max_length=60, blank=False, default="None", unique=True, verbose_name='Question Type Name')
	description = models.TextField(blank=False, default="")

	class Meta:
		verbose_name_plural = u'Challenge question type'

	def __unicode__(self):
		return u'Question Type: %s' %(self.name)

	def save(self, *args, **kwargs):
		super(ChallengeQuestionType, self).save(*args, **kwargs)

"""
Name:           AnswerType
Date created:   Feb 3, 2014
Description:    The asnwer types.
"""
class AnswerType(models.Model):
	name = models.CharField(max_length=60, blank=False, default="None", unique=True, verbose_name='Answer Type Name')
	description = models.TextField(blank=False, default="")

	class Meta:
		verbose_name_plural = u'Challenge answer type'

	def __unicode__(self):
		return u'Answer Type: %s' %(self.name)

	def save(self, *args, **kwargs):
		super(AnswerType, self).save(*args, **kwargs)

"""
Name:           ChallengeQuestion
Date created:   Feb 3, 2014
Description:    The questions that need to be answered to determine the
				CleanCred per hour value.
"""
class ChallengeQuestion(models.Model):
	question_number = models.IntegerField(default=0)	
	question = models.TextField(blank=False, default="None", verbose_name='Question')
	type = models.ForeignKey(ChallengeQuestionType, blank=True, default=1)
	answer_type = models.ForeignKey(AnswerType, blank=True, default=1)
	required = models.BooleanField(default=True)

	class Meta:
		verbose_name_plural = u'Challenge questions'

	def __unicode__(self):
		return u'Question: %s. %s' %(self.question_number, self.question)

	def save(self, *args, **kwargs):
		super(ChallengeQuestion, self).save(*args, **kwargs)

"""
Name:           QuestionAnswer
Date created:   Feb 3, 2014
Description:    The answer to each question and the value of each answer.
"""
class QuestionAnswer(models.Model):
	question = models.ForeignKey(ChallengeQuestion)
	answer_number = models.CharField(max_length=1, blank=False, null=False, default="A", verbose_name="Answer Number")
	answer = models.CharField(max_length=60, blank=False, default="None", verbose_name='Answer')
	score = models.IntegerField(blank=True, null=True, default=None)
	clean_grid = models.ForeignKey(CleanGrid, null=True, blank=True, default=None)

	class Meta:
		verbose_name_plural = u'Challenge question answer'

	def get_answer_score(self):
		if self.score is not None:
			return self.score
		else:
			return int(math.ceil(self.clean_grid.value))

	def __unicode__(self):
		return u'Question Answer: %s: %s' %(self.question, self.answer)

	def save(self, *args, **kwargs):
		super(QuestionAnswer, self).save(*args, **kwargs)

"""
Name:           UserChallengeSurvey
Date created:   Feb 17 2014
Description:    The survey each User creates for the Challenge.
"""
class UserChallengeSurvey(models.Model): 
	user = models.ForeignKey(User)
	clean_team = models.ForeignKey(CleanTeam)
	challenge = models.ForeignKey(Challenge)
	total_score = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = u'User Challenge Surveys'

	def create_survey(self, challenge, form):
		self.user = challenge.user
		self.clean_team = challenge.clean_team
		self.challenge = challenge
		self.save()

		total_score = 0

		for question, answers in form.items():			
			if question.startswith("question_"):
				if isinstance(answers, list):
					for answer in answers:
						try:	
							if answer != "":
								answer = int(answer)
								ans = QuestionAnswer.objects.get(id=answer)

								total_score += ans.get_answer_score()

								user_answer = UserChallengeSurveyAnswers(survey=self, answer=ans)
								user_answer.save()
						except Exception, e:
							print e
							return False
				else:
					try:
						if answers != "":
							answers = int(answers)
							ans = QuestionAnswer.objects.get(id=answers)

							total_score += ans.get_answer_score()

							user_answer = UserChallengeSurveyAnswers(survey=self, answer=ans)
							user_answer.save()
					except Exception, e:
						print e
						return False

		self.total_score = total_score
		self.save()

		challenge.clean_creds_per_hour = total_score
		challenge.save()

		return True

	def __unicode__(self):
		return u'User Challenge Survey: %s:' %(self.user)

	def save(self, *args, **kwargs):
		super(UserChallengeSurvey, self).save(*args, **kwargs)

"""
Name:           UserChallengeSurveyAnswers
Date created:   Feb 17 2014
Description:    The survey answer that each User gives for the Challenge.
"""
class UserChallengeSurveyAnswers(models.Model): 
	survey = models.ForeignKey(UserChallengeSurvey)
	answer = models.ForeignKey(QuestionAnswer)

	class Meta:
		verbose_name_plural = u'User Challenge Survey Answers'

	def __unicode__(self):
		return u'User Challenge Survey Answer: %s' %(self.answer)

	def save(self, *args, **kwargs):
		super(UserChallengeSurveyAnswers, self).save(*args, **kwargs)