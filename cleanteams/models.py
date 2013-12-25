from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count

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
	logo = models.ImageField(upload_to=get_upload_file_name, blank=True, null=True, default="", verbose_name='Logo')
	about = models.TextField(blank=True, null=True, default="")
	twitter = models.CharField(max_length=60, blank=True, null=True, verbose_name="Twitter Handle")
	region = models.CharField(max_length=60, blank=True, null=True, verbose_name="Region")
	team_type = models.CharField(max_length=60, blank=False, null=False, verbose_name="Team Type", default="Independent")
	group = models.CharField(max_length=100, blank=True, null=True, verbose_name="Group Representing")
	clean_creds = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = u'Clean Team'

	def __unicode__(self):
		return u'Clean Team: %s' % self.name

	def save(self, *args, **kwargs):
		super(CleanTeam, self).save(*args, **kwargs)

class CleanTeamMember(models.Model):
	user = models.ForeignKey(User)
	clean_team = models.ForeignKey(CleanTeam)
	role = models.CharField(max_length=30, default="clean-ambassador")
	status = models.CharField(max_length=30, default="pending")

	class Meta:
		verbose_name_plural = u'Clean Team Member'

	def __unicode__(self):
		return u'%s is on %s' %(self.user.username, self.clean_team)

	def save(self, *args, **kwargs):
		super(CleanTeamMember, self).save(*args, **kwargs)

	def request_join_clean_team(self, user, ct):
		self.user = user
		self.clean_team = ct
		self.status = "pending"
		self.role = "clean-ambassador"
		self.save()

		self.user.profile.clean_team_member = CleanTeamMember.objects.latest('id')
		self.user.profile.save()

	def has_max_clean_ambassadors(self):
		num_ca = CleanTeamMember.objects.filter(clean_team_id=8).count()

		if num_ca >= 4:
			return True

		return False
		