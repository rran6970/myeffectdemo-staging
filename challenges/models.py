import datetime

from django.db import models
from django.contrib.auth.models import User

from cleanteams.models import CleanTeam

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
	user = models.ForeignKey(User)
	clean_team = models.ForeignKey(CleanTeam, blank=True, null=True, default=-1)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	class Meta:
		verbose_name_plural = u'Challenges'

	def __unicode__(self):
		return u'Challenge: %s' % self.title

	def getChallengeCleanCreds(self):
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
	time_in	= models.DateTimeField(auto_now_add=True, blank=True, null=True)
	time_out = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	total_hours = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = u'Challenges user participated in'

	def save(self, *args, **kwargs):
		super(UserChallenge, self).save(*args, **kwargs)