import random
import string

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from django.db import models
from django.db.models import Count
from django.template import Context
from django.template.loader import get_template

from itertools import chain

from time import time

from notifications.models import Notification, UserNotification

def get_upload_file_name(instance, filename):
	return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)

"""
Name:           CleanTeamLevel
Date created:   Jan 30, 2014
Description:    All of the levels each Clean Team can go through
"""
class CleanTeamLevel(models.Model):
	name = models.CharField(max_length=30, null=False, default="Seedling")
	badge = models.CharField(max_length=100, null=False, default="images/badge-level-1-75x63.png")	
	next_level = models.ForeignKey('self', null=True, blank=True)

	class Meta:
		verbose_name_plural = u'Clean Team Level'

	def __unicode__(self):
		return u'%s' % self.name

	def save(self, *args, **kwargs):
		super(CleanTeamLevel, self).save(*args, **kwargs)

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
	level = models.ForeignKey(CleanTeamLevel, blank=True, null=True)

	class Meta:
		verbose_name_plural = u'Clean Team'

	def __unicode__(self):
		return u'Clean Team: %s' % self.name

	def add_team_clean_creds(self, amount):
		self.clean_creds += amount
		self.save()

	def level_up(self):
		# If they don't have a badge, ie. new team, make them a Seedling
		if self.level is None:
			print "it's None"
			level = CleanTeamLevel.objects.get(name="Seedling")

			self.level = level
			self.save()

			level_tasks = CleanTeamLevelTask.objects.filter(clean_team_level=level)
			
			for task in level_tasks:
				level_progress = CleanTeamLevelProgress(clean_team=self, level_task=task)

				if level_progress.level_task.name == "signup":
					level_progress.completed = True
				elif level_progress.level_task.name == "sign_code_conduct":
					level_progress.completed = True
				elif level_progress.level_task.name == "ct_name":
					level_progress.completed = True

				level_progress.save()

		else:
			if self.level.next_level.name == "Sapling":
				print "it's Seedling"

	def save(self, *args, **kwargs):
		super(CleanTeam, self).save(*args, **kwargs)
		self.level_up()

"""
Name:           CleanChampion
Date created:   Dec 30, 2013
Description:    Users can be part of Clean Teams as Clean Champions
"""
class CleanChampion(models.Model):
	user = models.ForeignKey(User)
	clean_team = models.ForeignKey(CleanTeam)
	status = models.CharField(max_length=30, default="approved")

	class Meta:
		verbose_name_plural = u'Clean Champions'

	def __unicode__(self):
		return u'%s is supporting %s' %(self.user.email, self.clean_team.name)

	def save(self, *args, **kwargs):
		super(CleanChampion, self).save(*args, **kwargs)

	def becomeCleanChampion(self, user, selected_team):
		self.user = user
		self.clean_team = selected_team
		self.status = "approved"
		self.save()

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

		self.clean_team.add_team_clean_creds(10)	

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
		return u'%s is on %s' %(self.user.email, self.clean_team.name)

	def save(self, *args, **kwargs):
		super(CleanTeamMember, self).save(*args, **kwargs)


	# By pass the requestBecomeCleanAmbassador and approveCleanAmbassador
	def becomeCleanAmbassador(self, user, selected_team, notification=True):
		self.user = user
		self.clean_team = selected_team
		self.status = "approved"
		self.save()

		self.user.profile.clean_team_member = CleanTeamMember.objects.latest('id')
		self.user.profile.save()

		if notification:
			# Send notifications
			notification = Notification.objects.get(notification_type="ca_approved")
			# The names that will go in the notification message template
			name_strings = [self.clean_team.name]
			link_strings = [str(self.clean_team.id)]
		
			user_notification = UserNotification()
			user_notification.create_notification("ca_approved", self.user, name_strings, link_strings)

		self.clean_team.add_team_clean_creds(10)	

	def approveCleanAmbassador(self, notification=True):
		self.status = "approved"
		self.save()

		CleanChampion.objects.filter(user=self.user, clean_team=self.clean_team).delete()

		if notification:
			# Send notifications
			notification = Notification.objects.get(notification_type="ca_approved")
			# The names that will go in the notification message template
			name_strings = [self.clean_team.name]
			link_strings = [str(self.clean_team.id)]
		
			user_notification = UserNotification()
			user_notification.create_notification("ca_approved", self.user, name_strings, link_strings)

		self.clean_team.add_team_clean_creds(10)

	def removedCleanAmbassador(self):
		self.status = "removed"
		self.save()

	def requestBecomeCleanAmbassador(self, user, selected_team, notification=True):
		self.user = user
		self.clean_team = selected_team
		self.status = "pending"
		self.role = "clean-ambassador"
		self.save()

		self.user.profile.clean_team_member = CleanTeamMember.objects.latest('id')
		self.user.profile.save()

		if notification:
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

			members_list = list(clean_team_members)

			if role == "clean-champion":
				clean_champions = CleanChampion.objects.filter(clean_team=self.clean_team, status="approved")	

				members_list = list(chain(clean_team_members, clean_champions))

			for member in members_list:
				user_notification = UserNotification()
				user_notification.create_notification("message_posted", member.user, name_strings, link_strings)

	def save(self, *args, **kwargs):
		super(CleanTeamPost, self).save(*args, **kwargs)

"""
Name:           CleanTeamInvite
Date created:   Jan 5, 2014
Description:    The invites that each member can receive
"""
class CleanTeamInvite(models.Model):
	email = models.EmailField(max_length=70, blank=True)
	clean_team = models.ForeignKey(CleanTeam)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	role = models.CharField(max_length=30, default="clean-ambassador")
	status = models.CharField(max_length=30, default="pending")
	token = models.CharField(max_length=20, blank=True)

	class Meta:
		verbose_name_plural = u'Clean Team Invite'

	def __unicode__(self):
		return u'%s post on %s' % (self.clean_team, str(self.timestamp))

	# Checks if User is already registered before accpeting the invite
	# Returns False if not accepted
	def acceptInvite(self, notification=True):
		emails = User.objects.filter(email=self.email).count()

		if emails > 0:
			self.status = "accepted"
			self.save()

			# Send notifications
			notification = Notification.objects.get(notification_type="ca_joined")
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
					user_notification.create_notification("ca_joined", member.user, name_strings)

			# self.clean_team.add_team_clean_creds(5)	

			return True

		return False

	def inviteUsers(self, user, role, email, uri, notification=True):
		char_set = string.ascii_lowercase + string.digits
		token = ''.join(random.sample(char_set*20,20))
		full_uri = u'%s/%s' % (uri, token)

		self.clean_team = user.profile.clean_team_member.clean_team
		self.user = user
		self.email = str(email)
		self.role = role
		self.status = 'pending'
		self.token = token
		self.save()

		# If the User is already registered, send them a notification
		try:
			u = User.objects.get(email=str(email))
		except Exception, e:
			u = None

		if notification:
			if u:
				# Send notifications
				notification_type = "cc_invite"
				if role == "clean-ambassador":
					notification_type = "ca_invite"
					
				notification = Notification.objects.get(notification_type=notification_type)
				# The names that will go in the notification message template
				full_name = u'%s %s' %(self.user.first_name, self.user.last_name)
				name_strings = [full_name, self.clean_team.name]
				link_strings = [str(self.token)]

				user_notification = UserNotification()
				user_notification.create_notification(notification_type, u, name_strings, link_strings)

		if role == "clean-ambassador":
			role = "Clean Ambassador"
		elif role == "clean-champion":
			role = "Clean Champion"

		# Send invite email to email address
		template = get_template('emails/email_invite_join.html')
		content = Context({ 'user': user, 'email': email, 'role': role, 'full_uri': full_uri })
		content = template.render(content)

		subject, from_email, to = 'My Clean City - Invite to join', 'info@mycleancity.org', email

		mail = EmailMessage(subject, content, from_email, [to])
		mail.content_subtype = "html"
		mail.send()

	def save(self, *args, **kwargs):
		super(CleanTeamInvite, self).save(*args, **kwargs)

"""
Name:           CleanTeamLevelTask
Date created:   Jan 30, 2014
Description:    All of the tasks required to be completed in a level
"""
class CleanTeamLevelTask(models.Model):
	clean_team_level = models.ForeignKey(CleanTeamLevel)
	name = models.CharField(max_length=60, blank=False, default="", verbose_name='Clean Team Level Task Name')
	description = models.TextField(blank=True, null=True, default="")

	class Meta:
		verbose_name_plural = u'Clean Team Level Task'

	def __unicode__(self):
		return u'%s' % self.clean_team_level

	def save(self, *args, **kwargs):
		super(CleanTeamLevelTask, self).save(*args, **kwargs)

"""
Name:           CleanTeamLevelProgress
Date created:   Jan 30, 2014
Description:    The tasks each Clean Team has completed per level
"""
class CleanTeamLevelProgress(models.Model):
	clean_team = models.ForeignKey(CleanTeam)
	level_task = models.ForeignKey(CleanTeamLevelTask)
	completed = models.BooleanField(default=0)

	class Meta:
		verbose_name_plural = u'Clean Team Level Progress'

	def __unicode__(self):
		return u'%s - %s' % (self.clean_team, self.level_task)

	def save(self, *args, **kwargs):
		super(CleanTeamLevelProgress, self).save(*args, **kwargs)