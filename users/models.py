from django.db import models
from django.contrib.auth.models import User

"""
Name:           PrelaunchEmails
Date created:   Sept 9, 2013
Description:    Used to keep track of all of the prelaunch emails
"""
class PrelaunchEmails(models.Model):
	first_name = models.CharField(max_length=50, blank=False)
	email = models.EmailField(max_length = 70, blank=False)
	postal_code = models.CharField(max_length = 7, blank=False)
	school_type = models.CharField(max_length = 30, blank=False, default="High School")
	ambassador = models.BooleanField()
	join = models.BooleanField()
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	class Meta:
		verbose_name_plural = u'Prelaunch emails'

	def __unicode__(self):
		return u'Prelaunch : %s' % self.user.username

	def save(self, *args, **kwargs):
		super(PrelaunchEmails, self).save(*args, **kwargs)