import datetime

from django.db import models
from django.contrib.auth.models import User

from cleanteams.models import CleanTeam, CleanTeamMember, CleanChampion

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
	host_organization = models.TextField(blank=False, default="")
	user = models.ForeignKey(User)
	clean_team = models.ForeignKey(CleanTeam, blank=True, null=True, default=-1)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	class Meta:
		verbose_name_plural = u'Challenges'

	def __unicode__(self):
		return u'Challenge: %s' % self.title

	def newChallenge(self, user, form):
		self.user = user
		self.title = form.cleaned_data['title']
		self.event_date = form.cleaned_data['event_date']
		self.event_time = form.cleaned_data['event_time']
		self.address1 = form.cleaned_data['address1']
		self.address2 = form.cleaned_data['address2']
		self.city = form.cleaned_data['city']
		self.postal_code = form.cleaned_data['postal_code']
		self.province = form.cleaned_data['province']
		self.country = form.cleaned_data['country']
		self.description = form.cleaned_data['description']
		self.host_organization = form.cleaned_data['host_organization']
		self.clean_team = user.profile.clean_team_member.clean_team
		self.save()

		challenge_category = ChallengeCategory()
		challenge_category.challenge = self
		challenge_category.category = form.cleaned_data['category']
		challenge_category.save()

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

	def getChallengeTotalCleanCreds(self, total_hours):
		challenge_category = ChallengeCategory.objects.get(challenge=self)
		
		return int(challenge_category.category.clean_cred_value * total_hours)

	def getChallengeCleanCredsPerHour(self):
		challenge_category = ChallengeCategory.objects.get(challenge=self)

		return int(challenge_category.category.clean_cred_value)

	def getChallengeCategory(self):
		challenge_category = ChallengeCategory.objects.get(challenge=self)
		
		return challenge_category.category.name

	def save(self, *args, **kwargs):
		super(Challenge, self).save(*args, **kwargs)

"""
Name:           Category
Date created:   Dec 14, 2013
Description:    Categories that each Challenge will be in. These categories will 
				contain a CleanCred value per hour.
"""
class Category(models.Model):
	name = models.CharField(max_length=60, blank=False, default="None", verbose_name='Category')
	clean_cred_value = models.IntegerField(default=0, verbose_name='CleanCreds/Hour')

	class Meta:
		verbose_name_plural = u'Challenge categories'

	def __unicode__(self):
		return u'%s - %s CleanCreds/hour' %(self.name, self.clean_cred_value)

	def save(self, *args, **kwargs):
		super(Category, self).save(*args, **kwargs)

"""
Name:           ChallengeCategory
Date created:   Dec 14, 2013
Description:    Assign a Challenge to a ChallengeCategory.
"""
class ChallengeCategory(models.Model):
	challenge = models.ForeignKey(Challenge)
	category = models.ForeignKey(Category)

	class Meta:
		verbose_name_plural = u'Category that a Challenge belongs in'

	def __unicode__(self):
		return u'Challenge: %s is in %s' %(self.challenge, self.category)

	def save(self, *args, **kwargs):
		super(ChallengeCategory, self).save(*args, **kwargs)

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

	class Meta:
		verbose_name_plural = u'Challenges user participated in'

	def save(self, *args, **kwargs):
		super(UserChallenge, self).save(*args, **kwargs)

"""
Name:           CleanGrid
Date created:   Feb 3, 2013
Description:    The Clean Grid system for answer value calculation.
"""
class CleanGrid(models.Model):
	name = models.CharField(max_length=60, blank=False, default="None", verbose_name='Clean Grid Name')
	value = models.DecimalField(max_digits=10, decimal_places=6)

	class Meta:
		verbose_name_plural = u'Challenge question answer'

	def save(self, *args, **kwargs):
		super(CleanGrid, self).save(*args, **kwargs)

"""
Name:           ChallengeQuestion
Date created:   Feb 3, 2013
Description:    The questions that need to be answered to determine the
				CleanCred per hour value.
"""
class ChallengeQuestion(models.Model):
	question_number = models.IntegerField(default=0)	
	question = models.CharField(max_length=60, blank=False, default="None", verbose_name='Question')

	class Meta:
		verbose_name_plural = u'Challenge questions'

	def save(self, *args, **kwargs):
		super(ChallengeQuestion, self).save(*args, **kwargs)

"""
Name:           QuestionAnswer
Date created:   Feb 3, 2013
Description:    The answer to each question and the value of each answer.
"""
class QuestionAnswer(models.Model):
	question = models.ForeignKey(ChallengeQuestion)
	question_number = models.IntegerField(default=0)
	answer = models.CharField(max_length=60, blank=False, default="None", verbose_name='Answer')
	score = models.IntegerField(default=0)
	clean_grid = models.ForeignKey(CleanGrid)

	class Meta:
		verbose_name_plural = u'Challenge question answer'

	def save(self, *args, **kwargs):
		super(QuestionAnswer, self).save(*args, **kwargs)