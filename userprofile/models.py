from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
 
import qrcode

from cStringIO import StringIO

from mycleancity.actions import *
from cleanteams.models import CleanTeamMember, CleanChampion
from notifications.models import Notification, UserNotification
from userorganization.models import UserOrganization

"""
Name:           UserSettings
Date created:   Feb 15, 2014
Description:    All of the settings for each UserProfile.
"""
class UserSettings(models.Model):
	user = models.OneToOneField(User, null=True)
	communication_language = models.CharField(max_length=10, blank=False, null=False, default="English", verbose_name='Communication Language')
	email_privacy = models.BooleanField(default=0)

	class Meta:
		verbose_name_plural = u'User Settings'

	def __unicode__(self):
		return u'User Setting: %s' % self.user.username

	def save(self, *args, **kwargs):
		super(UserSettings, self).save(*args, **kwargs)

"""
Name:           QRCodeSignups
Date created:   Jan 9, 2013
Description:    Used to keep track of all of the signups through the QR Code URL
"""
class QRCodeSignups(models.Model):
	user = models.OneToOneField(User)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	class Meta:
		verbose_name_plural = u'QR Code Signups'

	def __unicode__(self):
		return u'QR Code Signups : %s' % self.user.username

	def save(self, *args, **kwargs):
		super(QRCodeSignups, self).save(*args, **kwargs)

"""
Name:           UserQRCode
Date created:   Jan 9, 2014
Description:    A QR Code of each user
"""
class UserQRCode(models.Model):
	user = models.OneToOneField(User)
	data = models.CharField(max_length=60, blank=True, null=True, default="")
	qr_image = models.ImageField(
		upload_to=get_upload_file_name,
		height_field="qr_image_height",
		width_field="qr_image_width",
		null=True,
		blank=True
	)
	qr_image_height = models.PositiveIntegerField(null=True, blank=True, editable=False)
	qr_image_width = models.PositiveIntegerField(null=True, blank=True, editable=False)

	class Meta:
		verbose_name_plural = u'User QR Codes'

	def __unicode__(self):
		return u'User QR Code: %s' % self.user.username

	def qr_code(self):
		return '%s' % self.qr_image.url

	qr_code.allow_tags = True

# from userprofile.models import *; user = User.objects.get(id=196); qr = UserQRCode(data='http://hakstudio.com/', user=user); qr.save()

def userqrcode_pre_save(sender, instance, **kwargs):    
	if not instance.pk:
		instance._QRCODE = True
	else:
		if hasattr(instance, '_QRCODE'):
			instance._QRCODE = False
		else:
			instance._QRCODE = True

def userqrcode_post_save(sender, instance, **kwargs):
	if instance._QRCODE:
		instance._QRCODE = False

		if instance.qr_image:
			instance.qr_image.delete()
		
		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=12,
			border=2,
		)
		qr.add_data(instance.data)
		qr.make()
		image = qr.make_image()

		# Save image to string buffer
		image_buffer = StringIO()
		image.save(image_buffer, kind='JPEG')
		image_buffer.seek(0)

		# Here we use django file storage system to save the image.
		file_name = 'UserQR_%s_%s.jpg' % (instance.user.id, instance.id)
		file_object = File(image_buffer, file_name)
		content_file = ContentFile(file_object.read())

		key = 'qr_code/%s' % (file_name)
		uploadFile = UploadFileToS3()
		path = uploadFile.upload(key, content_file)

		instance.qr_image.save(path, content_file, save=True)
	 
models.signals.pre_save.connect(userqrcode_pre_save, sender=UserQRCode)
models.signals.post_save.connect(userqrcode_post_save, sender=UserQRCode)

"""
Name:           UserProfile
Date created:   Sept 8, 2013
Description:    Used as an extension to the User model.
"""
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	dob = models.DateField(auto_now_add=True, blank=True, null=True)
	about = models.TextField(blank=True, null=True, default="")
	twitter = models.CharField(max_length=60, blank=True, null=True, verbose_name="Twitter Handle")
	city = models.CharField(max_length=60, blank=True, null=True, verbose_name='City')
	province = models.CharField(max_length=10, blank=True, null=True, verbose_name='Province')
	postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Postal Code')
	country = models.CharField(max_length=60, blank=True, null=True, verbose_name='Country')
	clean_creds = models.IntegerField(default=0)
	school_type = models.CharField(max_length=30, blank=True, default="High School")
	age = models.CharField(max_length=30, blank=True, default="17-21")
	smartphone = models.BooleanField(default=0)
	clean_team_member = models.ForeignKey(CleanTeamMember, null=True)
	picture = models.ImageField(upload_to=get_upload_file_name, blank=True, null=True, default="", verbose_name='Profile Picture')
	hear_about_us = models.CharField(max_length=100, blank=True, null=True, verbose_name='How did you hear about us?')
	settings = models.OneToOneField(UserSettings, null=True)
	qr_code = models.OneToOneField(UserQRCode, null=True)

	class Meta:
		verbose_name_plural = u'User Profiles'

	def __unicode__(self):
		return u'UserProfile: %s' % self.user.username

	def is_clean_ambassador(self, status="approved"):
		try:
			return True if self.clean_team_member.role=="clean-ambassador" and self.clean_team_member.status==status else False
		except Exception, e:
			print e
			return False

	def is_clean_champion(self, clean_team=None):
		try:
			if clean_team:
				clean_champion = CleanChampion.objects.get(user=self.user, clean_team=clean_team)
			else:
				clean_champion = CleanChampion.objects.filter(user=self.user)[0]

			return True if clean_champion.status=="approved" else False
		except Exception, e:
			print e
			return False
		
	def is_organization(self):
		try:
			organization = UserOrganization.objects.get(user=self.user)
			return True
		except Exception, e:
			print e
			return False

	# TODO: Should check if they are part of a Clean Team as 
	# 		either a Clean Champion or Clean Ambassador
	def has_clean_team(self):
		if not self.clean_team_member:
			return False

		try:
			# ctm = CleanTeamMember.objects.get(user=self.user)

			if self.clean_team_member.status == "removed":
				return False
			if self.clean_team_member.status == "pending":
				return False

		except Exception, e:
			print e
			return False

		return True

	def get_notifications(self):
		user_notifications = UserNotification.objects.filter(user=self.user).order_by('-timestamp')[:10]
		return user_notifications

	def count_unread_notifications(self):
		count = UserNotification.objects.filter(user=self.user, read=False).count()
		return count

	def count_notifications(self):
		count = UserNotification.objects.filter(user=self.user).count()
		return count

	def add_clean_creds(self, amount, notification=True):
		self.clean_creds += amount
		self.save()

		if notification:
			try:
				# Send notifications
				notification = Notification.objects.get(notification_type="user_add_clean_creds")
				# The names that will go in the notification message template
				name_strings = [amount]
				link_strings = [str(self.user.id)]
			
				user_notification = UserNotification()
				user_notification.create_notification("user_add_clean_creds", self.user, name_strings, link_strings)
			except Exception, e:
				print e

	def add_clean_creds_to_individual_and_teams(self, amount, notification=True):
		# Add CleanCreds to individual
		self.add_clean_creds(amount, notification)

		# Clean Champion
		if self.is_clean_champion():
			clean_champions = CleanChampion.objects.filter(user=self.user)	
			
			for clean_champion in clean_champions:
				if clean_champion.status == "approved":
					clean_champion.clean_team.add_team_clean_creds(amount, notification)

		# Clean Ambassador
		if self.is_clean_ambassador():
			self.user.profile.clean_team_member.clean_team.add_team_clean_creds(amount, notification)	

	def save(self, *args, **kwargs):
		super(UserProfile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance) 
       settings, created = UserSettings.objects.get_or_create(user=instance)
       qr_code, created = UserQRCode.objects.get_or_create(user=instance, data='%s' % (profile.user.id))

       profile.settings = UserSettings.objects.latest('id')
       profile.qr_code = UserQRCode.objects.latest('id')

       profile.save()

post_save.connect(create_user_profile, sender=User) 
User.profile = property(lambda u: u.get_profile())