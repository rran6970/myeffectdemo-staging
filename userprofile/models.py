from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
 
from PyQRNative import *

from cStringIO import StringIO

from boto.s3.connection import S3Connection
from boto.s3.key import Key

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

	class Meta:
		verbose_name_plural = u'User Profiles'

	def __unicode__(self):
		return u'UserProfile: %s' % self.user.username

	def is_clean_ambassador(self, status="approved"):
		try:
			ctm = CleanTeamMember.objects.get(user=self.user)

			return True if ctm.role=="clean-ambassador" and ctm.status==status else False
		except Exception, e:
			print e
			return False

	def is_clean_champion(self, clean_team):
		try:
			clean_champion = CleanChampion.objects.get(user=self.user, clean_team=clean_team)

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

	def has_clean_team(self):
		if not self.clean_team_member:
			return False

		try:
			ctm = CleanTeamMember.objects.get(user=self.user)

			if ctm.status == "removed":
				return False
			if ctm.status == "pending":
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

	def add_clean_creds(self, amount):
		self.clean_creds += amount
		self.save()

	def save(self, *args, **kwargs):
		super(UserProfile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance) 
       settings, created = UserSettings.objects.get_or_create(user=instance)
       profile.settings = UserSettings.objects.latest('id')
       profile.save()

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
Name:           QRCodeSignups
Date created:   Jan 9, 2013
Description:    Used to keep track of all of the signups through the QR Code URL
"""
class UrlQRCode(models.Model):
	url = models.URLField()
	qr_image = models.ImageField(
		upload_to=get_upload_file_name,
		height_field="qr_image_height",
		width_field="qr_image_width",
		null=True,
		blank=True,
		editable=False
	)
	qr_image_height = models.PositiveIntegerField(null=True, blank=True, editable=False)
	qr_image_width = models.PositiveIntegerField(null=True, blank=True, editable=False)

	def qr_code(self):
		return '%s' % self.qr_image.url
    
	qr_code.allow_tags = True

# from userprofile.models import *; qr = UrlQRCode(url='http://www.google.ca/'); qr.save()

def urlqrcode_pre_save(sender, instance, **kwargs):    
	if not instance.pk:
		instance._QRCODE = True
	else:
		if hasattr(instance, '_QRCODE'):
			instance._QRCODE = False
		else:
			instance._QRCODE = True

def urlqrcode_post_save(sender, instance, **kwargs):
	if instance._QRCODE:
		instance._QRCODE = False

		if instance.qr_image:
			instance.qr_image.delete()
		
		qr = QRCode(4, QRErrorCorrectLevel.L)
		qr.addData(instance.url)
		qr.make()
		image = qr.makeImage()

		# Save image to string buffer
		image_buffer = StringIO()
		image.save(image_buffer, format='JPEG')
		image_buffer.seek(0)

		# # Here we use django file storage system to save the image.
		file_name = 'UrlQR_%s.jpg' % instance.id
		file_object = File(image_buffer, file_name)
		content_file = ContentFile(file_object.read())

		content_file.open()

		conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
		bucket = conn.get_bucket(settings.AWS_BUCKET)
		k = Key(bucket)
		k.key = 'qr_code/%s' % (file_name)
		k.set_contents_from_string(content_file.read())
		# user.profile.picture = k.key
		instance.qr_image.save(k.key, content_file, save=True)
	 
models.signals.pre_save.connect(urlqrcode_pre_save, sender=UrlQRCode)
models.signals.post_save.connect(urlqrcode_post_save, sender=UrlQRCode)

post_save.connect(create_user_profile, sender=User) 
User.profile = property(lambda u: u.get_profile())