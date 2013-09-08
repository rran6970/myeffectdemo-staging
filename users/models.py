from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	organization = models.CharField(max_length=60, blank=True, verbose_name='Organization')
	dob = models.DateField()
	city = models.CharField(max_length=60, blank=True, verbose_name='City')
	postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')
	country = models.CharField(max_length=60, blank=True, verbose_name='Country')

	class Meta:
		verbose_name_plural = u'User Profiles'

	def __unicode__(self):
		return u'UserProfile: %s' % self.user.username

	def save(self, *args, **kwargs):
		super(UserProfile, self).save(*args, **kwargs)