from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from time import time

from mycleancity.actions import *

"""
Name:           UserOrganization
Date created:   Sept 30, 2013
Description:    Used as an extension to the User model for organizations.
"""
class UserOrganization(models.Model):
	user = models.OneToOneField(User)
	organization = models.CharField(max_length=60, blank=True, verbose_name='Organization')
	website = models.URLField(verbose_name = u'Website', default="http://")
	logo = models.ImageField(upload_to=get_upload_file_name, blank=True, null=True, default="",verbose_name='Logo [Not working yet - Zeeshan]')

	class Meta:
		verbose_name_plural = u'User Organization'

	def __unicode__(self):
		return u'UserOrganization: %s' % self.user.username

	def save(self, *args, **kwargs):
		super(UserOrganization, self).save(*args, **kwargs)