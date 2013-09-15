import datetime

from django.db import models
from django.contrib.auth.models import User
from challenges.models import *

"""
Name:           CleanCredsMilestones
Date created:   Sept 8, 2013
Description:    The milestones a User can achieve with their Clean Creds.
"""
class CleanCredsMilestones(models.Model):
	title = models.CharField(max_length=60, blank=False, verbose_name="Title")
	description = models.TextField(blank=False, verbose_name="Description")
	cleancreds_needed = models.IntegerField()
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	class Meta:
		verbose_name_plural = u'User Clean Creds Milestones'

	def __unicode__(self):
		return u'%ss' % self.title

	def save(self, *args, **kwargs):
		super(CleanCredsMilestones, self).save(*args, **kwargs)

"""
Name:           CleanCredsAchievements
Date created:   Sept 8, 2013
Description:    Keeps track of all of the achievements a User has.
"""
class CleanCredsAchievements(models.Model):
	user = models.ForeignKey(User)
	milestone = models.ForeignKey(CleanCredsMilestones)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	class Meta:
		verbose_name_plural = u'User Clean Creds achievements by users'

	def __unicode__(self):
		return u'%ss' % self.title

	def save(self, *args, **kwargs):super(CleanCredsAchievements, self).save(*args, **kwargs)