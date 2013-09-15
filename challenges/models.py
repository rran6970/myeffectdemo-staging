import datetime

from django.db import models
from django.contrib.auth.models import User

"""
Name:           Challenge
Date created:   Sept 8, 2013
Description:    The challenge that each user will be allowed to created.
"""
class Challenge(models.Model):
	title = models.CharField(max_length=60, blank=False, verbose_name="Title")
	datetime = models.DateTimeField()
	cleancred_value = models.IntegerField()
	address1 = models.CharField(max_length=60, blank=False, verbose_name="Address")
	address2 = models.CharField(max_length=60, blank=False, verbose_name="Suite")
	city = models.CharField(max_length=60, blank=True, verbose_name='City')
	postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')
	country = models.CharField(max_length=60, blank=True, verbose_name='Country')
	user = models.OneToOneField(User)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	class Meta:
		verbose_name_plural = u'Challenges'

	def __unicode__(self):
		return u'Challenge: %s' % self.title

	def save(self, *args, **kwargs):
		super(Challenge, self).save(*args, **kwargs)

"""
Name:           UserChallenge
Date created:   Sept 8, 2013
Description:    Will be used to keep track of all of the Users partcipaing within a challenge
"""
class UserChallenge(models.Model):
	challenge = models.ForeignKey(Challenge)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	complete = models.BooleanField()

	class Meta:
		verbose_name_plural = u'Challenges user participated in'

	def save(self, *args, **kwargs):
		super(UserChallenge, self).save(*args, **kwargs)