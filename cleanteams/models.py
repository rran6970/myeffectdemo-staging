from django.contrib.auth.models import User
from django.db import models

from time import time

def get_upload_file_name(instance, filename):
	return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)

"""
Name:           CleanTeam
Date created:   Nov 25, 2013
Description:    Users can be part of Clean Teams
"""
class CleanTeam(models.Model):
	name = models.CharField(max_length=60, blank=True, verbose_name='Clean Team Name')
	website = models.URLField(verbose_name = u'Website', default="http://")
	logo = models.ImageField(upload_to=get_upload_file_name, blank=True, null=True, default="", verbose_name='Logo [Not working yet - Zeeshan]')
	clean_creds = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = u'Clean Team'

	def __unicode__(self):
		return u'Clean Team: %s' % self.name

	def save(self, *args, **kwargs):
		super(CleanTeam, self).save(*args, **kwargs)

class CleanTeamMember(models.Model):
	user = models.ForeignKey(User)
	cleam_team = models.ForeignKey(CleanTeam)

	def __unicode__(self):
		return u'%s is on %s' %(self.user.username, clean_team)

	def save(self, *args, **kwargs):
		super(CleanTeamMember, self).save(*args, **kwargs)