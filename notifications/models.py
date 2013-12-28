import datetime

from django.db import models
from django.contrib.auth.models import User

"""
Name:           Notification
Date created:   Dec 25, 2013
Description:    The notifications Users can receive.
"""
class Notification(models.Model):
	name = models.CharField(max_length=60, blank=False, verbose_name="Title")	
	description = models.TextField(blank=False, default="")
	message = models.TextField(blank=False, default="")
	link = models.TextField(blank=True, default="")
	notification_type = models.CharField(max_length=60, blank=False, verbose_name="Notification Type", default="challenge_posted")	
	users_to_notify = models.TextField(blank=False, default="")

	class Meta:
		verbose_name_plural = u'Notifications'

	def __unicode__(self):
		return u'%s' % self.name

	def save(self, *args, **kwargs):
		super(Notification, self).save(*args, **kwargs)

"""
Name:           UserNotification
Date created:   Dec 25, 2013
Description:    The notifications each User has.
"""
class UserNotification(models.Model):
	user = models.ForeignKey(User)
	notification = models.ForeignKey(Notification)
	read = models.BooleanField(default=0)
	message = models.TextField(blank=False, default="")
	link = models.TextField(blank=True, default="")
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	class Meta:
		verbose_name_plural = u'User Notifications'

	def __unicode__(self):
		return u'Notification %s on %s' % (self.notification, self.user)

	def read_notification(self):
		self.read = True
		self.save()

	def create_notification(self, notification_type, user, *args, **kwargs):
		notification = Notification.objects.get(notification_type=notification_type)

		# This is what will be processed if it was hard coded.

		# array_of_strings = ['Team1', 'Team2', 'December 25th, 2015']
		# message = '{0} posted a challenge to {1} on {2}'
		# print(message.format(*array_of_strings))

		# print len(args)

		self.user = user
		self.notification = notification

		message_template = notification.message
		message = message_template.format(*args[0])
		self.message = message

		if len(args) > 1:
			link_template = notification.link
			link = link_template.format(*args[1])
		else:
			link = notification.link

		self.link = link
		self.save()

	def save(self, *args, **kwargs):
		super(UserNotification, self).save(*args, **kwargs)