from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save

from cleanteams.models import CleanTeamMember, CleanChampion
from notifications.models import Notification, UserNotification
from userorganization.models import UserOrganization

def get_upload_file_name(instance, filename):
	return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)

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

	def save(self, *args, **kwargs):
		super(UserProfile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

"""
Name:           QRCodeSignups
Date created:   Sept 9, 2013
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
 
post_save.connect(create_user_profile, sender=User) 
User.profile = property(lambda u: u.get_profile())