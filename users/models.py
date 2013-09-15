from django.db import models
from django.contrib.auth.models import User

"""
Name:           UserProfile
Date created:   Sept 8, 2013
Description:    Used as an extension to the User model.
"""
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	organization = models.CharField(max_length=60, blank=True, verbose_name='Organization')
	dob = models.DateField()
	city = models.CharField(max_length=60, blank=True, verbose_name='City')
	postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')
	country = models.CharField(max_length=60, blank=True, verbose_name='Country')
	clean_creds = models.IntegerField()

	class Meta:
		verbose_name_plural = u'User Profiles'

	def __unicode__(self):
		return u'UserProfile: %s' % self.user.username

	def save(self, *args, **kwargs):
		super(UserProfile, self).save(*args, **kwargs)

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
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	class Meta:
		verbose_name_plural = u'Prelaunch emails'

	def __unicode__(self):
		return u'Prelaunch : %s' % self.user.username

	def save(self, *args, **kwargs):
		super(PrelaunchEmails, self).save(*args, **kwargs)