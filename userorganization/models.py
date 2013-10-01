from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

"""
Name:           UserOrganization
Date created:   Sept 30, 2013
Description:    Used as an extension to the User model for organizations.
"""
class UserOrganization(models.Model):
	user = models.OneToOneField(User)
	organization = models.CharField(max_length=60, blank=True, verbose_name='Organization')
	city = models.CharField(max_length=60, blank=True, verbose_name='City')
	postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')
	country = models.CharField(max_length=60, blank=True, verbose_name='Country')

	class Meta:
		verbose_name_plural = u'User Organization'

	def __unicode__(self):
		return u'UserOrganization: %s' % self.user.username

	def save(self, *args, **kwargs):
		super(UserOrganization, self).save(*args, **kwargs)

def create_user_organization(sender, instance, created, **kwargs):  
    if created:  
       organization, created = UserOrganization.objects.get_or_create(user=instance)  

post_save.connect(create_user_organization, sender=User) 
# User.organization = property(lambda u: u.get_profile())