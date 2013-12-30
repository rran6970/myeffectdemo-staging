from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save

from cleanteams.models import CleanTeamMember
from notifications.models import Notification, UserNotification
from userorganization.models import UserOrganization

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
	school_type = models.CharField(max_length = 30, blank=True, default="High School")
	clean_team_member = models.ForeignKey(CleanTeamMember, null=True)

	class Meta:
		verbose_name_plural = u'User Profiles'

	def __unicode__(self):
		return u'UserProfile: %s' % self.user.username

	def is_clean_ambassador(self):
		ctm = CleanTeamMember.objects.get(user=self.user)

		return True if ctm.role=="clean-ambassador" and ctm.status=="approved" else False

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
		user_notifications = UserNotification.objects.filter(user=self.user).order_by('-timestamp')[:5]
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
 
post_save.connect(create_user_profile, sender=User) 
User.profile = property(lambda u: u.get_profile())