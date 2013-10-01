from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from userorganization.models import UserOrganization

"""
Name:           UserProfile
Date created:   Sept 8, 2013
Description:    Used as an extension to the User model.
"""
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	dob = models.DateField(auto_now_add=True, blank=True, null=True)
	city = models.CharField(max_length=60, blank=True, null=True, verbose_name='City')
	postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Postal Code')
	country = models.CharField(max_length=60, blank=True, null=True, verbose_name='Country')
	clean_creds = models.IntegerField(default=0)
	school_type = models.CharField(max_length = 30, blank=True, default="High School")
	ambassador = models.BooleanField()	

	class Meta:
		verbose_name_plural = u'User Profiles'

	def __unicode__(self):
		return u'UserProfile: %s' % self.user.username

	def is_organization(self):
		try:
			organization = UserOrganization.objects.get(user=self.user)
			return True
		except Exception, e:
			print e
			return False

	def save(self, *args, **kwargs):
		super(UserProfile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  
 
post_save.connect(create_user_profile, sender=User) 
User.profile = property(lambda u: u.get_profile())