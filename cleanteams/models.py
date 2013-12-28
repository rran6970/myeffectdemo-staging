from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count

from time import time

from notifications.models import Notification, UserNotification

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

"""
Name:           CleanTeamMember
Date created:   Nov 25, 2013
Description:    Users can be part of Clean Teams
"""
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
	
	def approveCleanAmbassador(self):
		self.status = "approved"
		self.save()

		# Send notifications
		notification = Notification.objects.get(notification_type="ca_joined")
		# The names that will go in the notification message template
		name_strings = [self.clean_team.name]
		link_strings = [str(self.clean_team.id)]
	
		user_notification = UserNotification()
		user_notification.create_notification("ca_joined", self.user, name_strings, link_strings)

	def removedCleanAmbassador(self):
		self.status = "removed"
		self.save()

	def requestBecomeCleanAmbassador(self, user, form):
		selected_team = form.cleaned_data['team']

		self.user = user
		self.clean_team = selected_team
		self.status = "pending"
		self.role = "clean-ambassador"
		self.save()

		self.user.profile.clean_team_member = CleanTeamMember.objects.latest('id')
		self.user.profile.save()

		# Send notifications
		notification = Notification.objects.get(notification_type="ca_request")
		# The names that will go in the notification message template
		full_name = u'%s %s' %(self.user.first_name, self.user.last_name)
		name_strings = [full_name, self.clean_team.name]

		users_to_notify_str = notification.users_to_notify
		users_to_notify = users_to_notify_str.split(', ')

		# Notify all of the Users that have the roles within users_to_notify
		for role in users_to_notify:
			clean_team_members = CleanTeamMember.objects.filter(role=role, clean_team=self.clean_team, status="approved")

			for member in clean_team_members:
				user_notification = UserNotification()
				user_notification.create_notification("ca_request", member.user, name_strings)

	def becomeCleanChampion(self, user, form):
		selected_team = form.cleaned_data['team']

		self.user = user
		self.clean_team = selected_team
		self.status = "approved"
		self.role = "clean-champion"
		self.save()

		self.user.profile.clean_team_member = CleanTeamMember.objects.latest('id')
		self.user.profile.save()

		# Send notifications
		notification = Notification.objects.get(notification_type="cc_joined")
		# The names that will go in the notification message template
		full_name = u'%s %s' %(self.user.first_name, self.user.last_name)
		name_strings = [full_name, self.clean_team.name]

		users_to_notify_str = notification.users_to_notify
		users_to_notify = users_to_notify_str.split(', ')

		# Notify all of the Users that have the roles within users_to_notify
		for role in users_to_notify:
			clean_team_members = CleanTeamMember.objects.filter(role=role, clean_team=self.clean_team, status="approved")

			for member in clean_team_members:
				user_notification = UserNotification()
				user_notification.create_notification("cc_joined", member.user, name_strings)

	def has_max_clean_ambassadors(self):
		num_ca = CleanTeamMember.objects.filter(clean_team_id=8).count()

		if num_ca >= 4:
			return True

		return False

"""
Name:           CleanTeamPost
Date created:   Dec 25, 2013
Description:    The posts on a Clean Team's profile
"""
class CleanTeamPost(models.Model):
	clean_team = models.ForeignKey(CleanTeam)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	message = models.TextField(blank=True, null=True, default="")

	class Meta:
		verbose_name_plural = u'Clean Team Post'

	def __unicode__(self):
		return u'%s post on %s' % (self.clean_team, str(self.timestamp))

	def newPost(self, user, form, clean_team):
		self.user = user
		self.clean_team = clean_team
		self.message = form.cleaned_data['message']

		self.save()

		# Send notifications
		notification = Notification.objects.get(notification_type="message_posted")
		# The names that will go in the notification message template
		name_strings = [self.clean_team.name]
		link_strings = [str(self.clean_team.id)]

		users_to_notify_str = notification.users_to_notify
		users_to_notify = users_to_notify_str.split(', ')

		# Notify all of the Users that have the roles within users_to_notify
		for role in users_to_notify:
			clean_team_members = CleanTeamMember.objects.filter(role=role, clean_team=self.clean_team, status="approved")

			for member in clean_team_members:
				user_notification = UserNotification()
				user_notification.create_notification("message_posted", member.user, name_strings, link_strings)


	def save(self, *args, **kwargs):
		super(CleanTeamPost, self).save(*args, **kwargs)