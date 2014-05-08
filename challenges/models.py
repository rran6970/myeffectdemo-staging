import datetime
import json
import math
import operator
import qrcode
import random
import string

from cStringIO import StringIO

from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save

from django.utils.timezone import utc

from cleanteams.models import CleanTeam, CleanTeamMember, CleanChampion, CleanTeamLevelTask

from mycleancity.actions import *
from notifications.models import Notification, UserNotification

from itertools import chain

"""
Name:           ChallengeQRCode
Date created:   March 10, 2014
Description:    A QR Code of each Challenge.
"""
class ChallengeQRCode(models.Model):
	data = models.CharField(max_length=200, blank=True, null=True, default="")
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
		verbose_name_plural = u'Challenge QR Codes'

	def __unicode__(self):
		return u'Challenge QR Code: %s' % self.data

	def qr_code(self):
		return '%s' % self.qr_image.url

	qr_code.allow_tags = True

def challengeqrcode_pre_save(sender, instance, **kwargs):    
	if not instance.pk:
		instance._QRCODE = True
	else:
		if hasattr(instance, '_QRCODE'):
			instance._QRCODE = False
		else:
			instance._QRCODE = True

def challengeqrcode_post_save(sender, instance, **kwargs):
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
		file_name = 'ChallengeQR_%s.jpg' % (instance.id)
		file_object = File(image_buffer, file_name)
		content_file = ContentFile(file_object.read())

		key = 'qr_code/%s' % (file_name)
		uploadFile = UploadFileToS3()
		path = uploadFile.upload(key, content_file)

		instance.qr_image.save(path, content_file, save=True)
	 
models.signals.pre_save.connect(challengeqrcode_pre_save, sender=ChallengeQRCode)
models.signals.post_save.connect(challengeqrcode_post_save, sender=ChallengeQRCode)

"""
Name:           ChallengeType
Date created:   Mar 10, 2014
Description:    The type of Challenge.
"""
class ChallengeType(models.Model):
	name = models.CharField(max_length=60, blank=False, verbose_name="Name")	
	description = models.TextField(blank=False, default="")
	challenge_type = models.CharField(max_length=60, blank=False, verbose_name="Challenge Type", default="")	

	class Meta:
		verbose_name_plural = u'Challenge Types'

	def __unicode__(self):
		return u'%s' % self.name

	def save(self, *args, **kwargs):
		super(ChallengeType, self).save(*args, **kwargs)

"""
Name:           Challenge
Date created:   Sept 8, 2013
Description:    The challenge that each user will be allowed to created.
"""
class Challenge(models.Model):
	title = models.CharField(max_length=60, blank=False, verbose_name="Title")
	event_start_date = models.DateField(blank=True, null=True)
	event_start_time = models.TimeField(blank=True, null=True)
	event_end_date = models.DateField(blank=True, null=True)
	event_end_time = models.TimeField(blank=True, null=True)
	address1 = models.CharField(max_length=60, blank=False, verbose_name="Address")
	address2 = models.CharField(max_length=60, blank=True, verbose_name="Suite")
	city = models.CharField(max_length=60, blank=True, verbose_name='City')
	province = models.CharField(max_length=60, blank=True, verbose_name='Province')
	postal_code = models.CharField(max_length=10, blank=True, verbose_name='Postal Code')
	country = models.CharField(max_length=60, blank=True, verbose_name='Country')
	description = models.TextField(blank=False, default="")
	user = models.ForeignKey(User)
	clean_team = models.ForeignKey(CleanTeam, blank=True, null=True, default=-1)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	last_updated_by = models.ForeignKey(User, related_name='user_last_updated_by')
	clean_creds_per_hour = models.IntegerField(default=0)
	national_challenge = models.BooleanField(default=False)
	type = models.ForeignKey(ChallengeType, blank=True, null=True, default=1)
	qr_code = models.OneToOneField(ChallengeQRCode, null=True, blank=True)
	token = models.CharField(max_length=20, blank=True)
	promote_top = models.BooleanField(default=False)
	url = models.CharField(max_length=60, blank=True, null=True, unique=True, verbose_name="URL")

	clean_team_only = models.BooleanField(default=False)

	organization = models.CharField(max_length=60, blank=False, verbose_name="Organization Name")
	contact_first_name = models.CharField(max_length=60, blank=False, verbose_name="Contact First Name")
	contact_last_name = models.CharField(max_length=60, blank=False, verbose_name="Contact Last Name")
	contact_phone = models.CharField(max_length=15, blank=False, verbose_name="Contact Phone Number")
	contact_email = models.CharField(max_length=60, blank=False, verbose_name="Contact Email")

	class Meta:
		verbose_name_plural = u'Challenges'

	def __unicode__(self):
		return u'Challenge: %s' % self.title

	def new_challenge(self, user, form):
		self.user = user
		self.last_updated_by = user
		self.title = form['title']
		self.event_start_date = form['event_start_date']
		self.event_start_time = form['event_start_time']
		self.event_end_date = form['event_end_date']
		self.event_end_time = form['event_end_time']
		self.address1 = form['address1']
		self.address2 = form['address2']
		self.city = form['city']
		self.postal_code = form['postal_code']
		self.province = form['province']
		self.country = form['country']
		self.description = form['description']
		self.national_challenge = form['national_challenge']
		self.clean_team_only = form['clean_team_only']
		
		self.organization = form['organization']
		self.contact_first_name = form['contact_first_name']
		self.contact_last_name = form['contact_last_name']
		self.contact_phone = form['contact_phone']
		self.contact_email = form['contact_email']

		if form['type']:
			self.type = form['type']
		
		char_set = string.ascii_lowercase + string.digits
		self.token = ''.join(random.sample(char_set*20,20))
		self.clean_team = user.profile.clean_team_member.clean_team
		self.save()

		survey = UserChallengeSurvey()
		survey.create_survey(self, form)		

		# Send notifications
		notification = Notification.objects.get(notification_type="challenge_posted")
		# The names that will go in the notification message template
		name_strings = [self.clean_team.name, self.title]
		link_strings = [str(self.id)]

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
				user_notification.create_notification("challenge_posted", member.user, name_strings, link_strings)

		if self.clean_team.level.name == "Sprout":
			task = CleanTeamLevelTask.objects.get(name="1_challenge")
			self.clean_team.complete_level_task(task)

		elif self.clean_team.level.name == "Sapling":
			count_challenges = Challenge.objects.filter(clean_team=self.clean_team).count()

			if count_challenges > 4:
				task = CleanTeamLevelTask.objects.get(name="5_challenges")
				self.clean_team.complete_level_task(task)

	def get_challenge_total_clean_creds(self, total_hours):
		return int(self.clean_creds_per_hour * total_hours)

	def one_time_check_in_with_token(self, user, token):
		now = datetime.datetime.utcnow().replace(tzinfo=utc)
		total_clean_creds = self.clean_creds_per_hour

		if self.clean_team_only:
			try:
				participant = user.profile.clean_team_member.clean_team
				clean_team_challenge, created = CleanTeamChallenge.objects.get_or_create(clean_team=participant, challenge=self, time_in__isnull=True)
					
				clean_team_challenge.time_in = now
				clean_team_challenge.time_out = now
				clean_team_challenge.total_hours = 0
				clean_team_challenge.total_clean_creds = total_clean_creds
				clean_team_challenge.save()

				# TODO: Add CleanCreds to CAs and CCs
				
				# Clean Team posting challenge	
				self.clean_team.add_team_clean_creds(total_clean_creds)
			except Exception, e:
				print e
		else:
			try:
				userchallenge, created = UserChallenge.objects.get_or_create(user=user, challenge=self, time_in__isnull=True)
					
				userchallenge.time_in = now
				userchallenge.time_out = now
				userchallenge.total_hours = 0
				userchallenge.total_clean_creds = total_clean_creds
				userchallenge.save()

				user.profile.add_clean_creds_to_individual_and_teams(total_clean_creds)
				
				# Clean Team posting challenge	
				self.clean_team.add_team_clean_creds(total_clean_creds)
			except Exception, e:
				print e
	
	def check_in_check_out(self, participant_id, manual_clean_creds=0, manual_hours=0):
		try:
			if self.type.challenge_type == "hourly":

				if self.clean_team_only:
					participant_challenge = CleanTeamChallenge.objects.get(clean_team_id=participant_id, challenge=self)
				else:
					participant_challenge = UserChallenge.objects.get(user_id=participant_id, challenge=self)

				if not participant_challenge.time_in:
					now = datetime.datetime.utcnow().replace(tzinfo=utc)

					participant_challenge.time_in = now
					participant_challenge.save()
				else:
					# Get current time and time out time
					now = str(datetime.datetime.utcnow().replace(tzinfo=utc))
					participant_challenge.time_out = now

					now_str = datetime.datetime.strptime(str(now)[:19], "%Y-%m-%d %H:%M:%S")
					time_in_str = datetime.datetime.strptime(str(participant_challenge.time_in)[:19], "%Y-%m-%d %H:%M:%S")

					diff = now_str - time_in_str
					total_hours = (diff.days * 24) + (diff.seconds // 3600)

					total_clean_creds = self.get_challenge_total_clean_creds(total_hours)

					participant_challenge.total_hours = total_hours
					participant_challenge.total_clean_creds = total_clean_creds
					participant_challenge.save()

					# Add CleanCreds
					if hasattr(participant_challenge, 'user'):
						user = participant_challenge.user
						user.profile.add_clean_creds_to_individual_and_teams(total_clean_creds)

					# Clean Team posting challenge		
					self.clean_team.add_team_clean_creds(total_clean_creds)

					return "%s Hours<br/>%s <span class='green bold'>Clean</span><span class='blue bold'>Creds</span>" % (str(total_hours), str(total_clean_creds))
			
			elif self.type.challenge_type == "manual":

				if self.clean_team_only:
					participant_challenge = CleanTeamChallenge.objects.get(clean_team_id=participant_id, challenge=self)
				else:
					participant_challenge = UserChallenge.objects.get(user_id=participant_id, challenge=self)

				now = datetime.datetime.utcnow().replace(tzinfo=utc)
				# total_clean_creds = self.clean_creds_per_hour

				participant_challenge.time_in = now
				participant_challenge.time_out = now
				participant_challenge.total_hours = manual_hours
				participant_challenge.total_clean_creds = manual_clean_creds
				participant_challenge.save()

				# Add CleanCreds
				if hasattr(participant_challenge, 'user'):
					user = participant_challenge.user
					user.profile.add_clean_creds_to_individual_and_teams(manual_clean_creds)
				
				# Clean Team posting challenge	
				self.clean_team.add_team_clean_creds(manual_clean_creds)

				return "Confirmed"
			
			else:

				if self.clean_team_only:
					participant_challenge, created = CleanTeamChallenge.objects.get_or_create(clean_team_id=participant_id, challenge=self, time_in__isnull=True)
				else:
					participant_challenge, created = UserChallenge.objects.get_or_create(user_id=participant_id, challenge=self, time_in__isnull=True)

				now = datetime.datetime.utcnow().replace(tzinfo=utc)
				total_clean_creds = self.clean_creds_per_hour

				participant_challenge.time_in = now
				participant_challenge.time_out = now
				participant_challenge.total_hours = 0
				participant_challenge.total_clean_creds = total_clean_creds
				participant_challenge.save()

				# Add CleanCreds
				if hasattr(participant_challenge, 'user'):
					user = participant_challenge.user
					user.profile.add_clean_creds_to_individual_and_teams(total_clean_creds)
				
				# Clean Team posting challenge	
				self.clean_team.add_team_clean_creds(total_clean_creds)

				return "Confirmed"

		except Exception, e:
			print e

	# Have to remove staples_store parameter only there for the Staples CleanAct
	def participate_in_challenge(self, user, staples_store=None):
		try:
			if self.clean_team_only:
				if user.profile.is_clean_ambassador():
					clean_team = user.profile.clean_team_member.clean_team

					# Staples CleanAct stuff
					if self.url == "staples-cleanact":
						staples_challenge = StaplesChallenge.objects.filter(staples_store=staples_store)

						if staples_challenge.count() == 0:
							staples_challenge = StaplesChallenge()
							staples_challenge.challenge = self
							staples_challenge.clean_team = clean_team
							staples_challenge.staples_store = staples_store
							staples_challenge.save()
						else:
							return False

					clean_team_challenge = CleanTeamChallenge.objects.filter(clean_team=clean_team, challenge=self)

					if clean_team_challenge.count() == 0:
						clean_team_challenge = CleanTeamChallenge(clean_team=clean_team)
						clean_team_challenge.challenge = self
						clean_team_challenge.save()
					else:
						return False			
			else:
				user_challenge = UserChallenge.objects.filter(user=user, challenge=self)

				if user_challenge.count() == 0:
					user_challenge = UserChallenge(user=user)
					user_challenge.challenge = self
					user_challenge.save()
				else:
					return False

			if user.profile.is_clean_ambassador():
				if user.profile.clean_team_member.clean_team.level.name == "Tree":
					count_user_challenges = UserChallenge.objects.filter(user=user, challenge__national_challenge=True).count()
					count_clean_team_challenges = CleanTeamChallenge.objects.filter(clean_team=clean_team, challenge__national_challenge=True).count()

					total_challenges = count_user_challenges + count_clean_team_challenges

					if total_challenges > 1:
						task = CleanTeamLevelTask.objects.get(name="2_national_challenges_signup")
						self.clean_team.complete_level_task(task)

		except Exception, e:
			raise e
		
		return True
	
	def get_participating_challenge(self, user):
		if self.clean_team_only:
			if user.is_active:
				if user.profile.is_clean_ambassador():
					try:
						clean_team_challenge = CleanTeamChallenge.objects.get(clean_team=user.profile.clean_team_member.clean_team, challenge=self)
						return clean_team_challenge
					except Exception, e:
						print e
						return False
		else:
			try:
				user_challenge = UserChallenge.objects.get(user=user, challenge=self)
				return user_challenge
			except Exception, e:
				print e
				return False

	def get_participants(self):
		if self.clean_team_only:
			participants = CleanTeamChallenge.objects.raw("SELECT id, clean_team_id FROM challenges_cleanteamchallenge WHERE challenge_id = %s GROUP BY clean_team_id, challenge_id" % (self.id))
		else:
			participants = UserChallenge.objects.raw("SELECT id, user_id FROM challenges_userchallenge WHERE challenge_id = %s GROUP BY user_id, challenge_id" % (self.id))

		return participants

	def get_participants_to_check_in(self):
		if self.clean_team_only:
			participants = CleanTeamChallenge.objects.raw("SELECT id, clean_team_id, challenge_id, max(time_in) AS time_in FROM challenges_cleanteamchallenge WHERE challenge_id = %s GROUP BY clean_team_id, challenge_id" % (self.id))

			return participants
		else:
			participants = UserChallenge.objects.raw("SELECT id, user_id, challenge_id, max(time_in) AS time_in FROM challenges_userchallenge WHERE challenge_id = %s GROUP BY user_id, challenge_id" % (self.id))

			return participants

	@staticmethod
	def search_challenges(query, national_challenges=False, clean_team_only=False, limit=False):
		today = datetime.datetime.now()

		predicates = Q(event_end_date__gte=today)

		if national_challenges == "true" or national_challenges == "on":
			predicates.add(Q(national_challenge=True), predicates.connector)

		if clean_team_only == "true" or clean_team_only == "on":
			predicates.add(Q(clean_team_only=True), predicates.connector)

		predicates.add(Q(title__icontains=query) | Q(city__icontains=query), predicates.connector)

		if limit:
			challenges = Challenge.objects.filter(predicates).order_by('-promote_top')[:limit]
		else:
			challenges = Challenge.objects.filter(predicates).order_by('-promote_top')

		return challenges

	@staticmethod
	def search_results_to_json(challenges):
		challenge_dict = {}

		count = 0
		for c in challenges:
			pk = c.id
			type = c.type.id
			clean_team = c.clean_team.id

			clean_team = CleanTeam.objects.get(id=clean_team)
			list_start = "<li><a href='/challenges/%s/'>" % (pk)
			list_end = "</a></li>"

			if clean_team.logo:
				logo = "<img class='profile-pic profile-pic-42x42' src='%s%s' alt='' />" % (settings.MEDIA_URL, clean_team.logo)
			else:
				logo = "<img src='%simages/default-team-pic-124x124.png' alt='' class='profile-pic profile-pic-42x42' />" % (settings.STATIC_URL)

			limit = 22

			if len(c.title) > limit:
				challenge_title = "%s..." % limiter(c.title, limit)
			else:
				challenge_title = c.title

			city = c.city if c.city else ""
			province = c.province if c.province else ""

			if type == 2:
				clean_creds_per_hour = "<br/><strong>%s</strong>&nbsp;<span class='green bold'>Clean</span><span class='blue bold'>Creds</span>" % (c.clean_creds_per_hour) if c.clean_creds_per_hour else ""
			else:
				clean_creds_per_hour = "<br/><strong>%s</strong>&nbsp;<span class='green bold'>Clean</span><span class='blue bold'>Creds</span>/hr" % (c.clean_creds_per_hour) if c.clean_creds_per_hour else ""

			title = "%s<div>%s<br/>%s&nbsp;%s%s</div>" % (logo, challenge_title, city, province, clean_creds_per_hour)
			
			if c.national_challenge:
				title += "<img class='badge-icon' src='/static/images/badge-nc-62x45.png' alt='National Challenge'>"

			li = "%s%s%s" % (list_start, title, list_end)

			challenge_dict[count] = li
			count += 1


		return json.dumps(challenge_dict, indent=4, separators=(',', ': '))

	def save(self, *args, **kwargs):
		super(Challenge, self).save(*args, **kwargs)

def create_challenge(sender, instance, created, **kwargs):  
	if created:
		if instance.type.challenge_type == "one-time":
			site_url = current_site_url()
			
			qr_code, created = ChallengeQRCode.objects.get_or_create(data='%schallenges/one-time-check-in/%s/%s' % (site_url, instance.id, instance.token))
		
			instance.qr_code = qr_code

			instance.save()

post_save.connect(create_challenge, sender=Challenge) 

"""
Name:           UserChallenge
Date created:   Sept 8, 2013
Description:    Will be used to keep track of all of the Users partcipating 
				within a challenge.
"""
class UserChallenge(models.Model):
	challenge = models.ForeignKey(Challenge)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	time_in	= models.DateTimeField(blank=True, null=True)
	time_out = models.DateTimeField(blank=True, null=True)
	total_hours = models.IntegerField(default=0)
	total_clean_creds = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = u'Challenges user participated in'

	def save(self, *args, **kwargs):
		super(UserChallenge, self).save(*args, **kwargs)

"""
Name:           CleanTeamChallenge
Date created:   May 2, 2014
Description:    Will be used to keep track of all of the Clean Teams partcipating 
				within a challenge.
"""
class CleanTeamChallenge(models.Model):
	challenge = models.ForeignKey(Challenge)
	clean_team = models.ForeignKey(CleanTeam)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	time_in	= models.DateTimeField(blank=True, null=True)
	time_out = models.DateTimeField(blank=True, null=True)
	total_hours = models.IntegerField(default=0)
	total_clean_creds = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = u'Challenges clean teams participated in'

	def save(self, *args, **kwargs):
		super(CleanTeamChallenge, self).save(*args, **kwargs)

"""
Name:           StaplesStores
Date created:   May 4, 2014
Description:    
"""
class StaplesStores(models.Model):
	store_no = models.IntegerField(default=0, unique=True)
	district = models.IntegerField(default=0)
	store_name = models.CharField(max_length=60, blank=False, verbose_name="Store Name")
	address = models.CharField(max_length=60, blank=False, verbose_name="Store Address")
	city = models.CharField(max_length=60, blank=False, verbose_name="City")
	province = models.CharField(max_length=60, blank=False, verbose_name="Province")
	postal_code = models.CharField(max_length=60, blank=False, verbose_name="Postal Code")
	telephone = models.CharField(max_length=60, blank=False, verbose_name="Telephone")
	fax = models.CharField(max_length=60, blank=False, verbose_name="Fax")
	gm = models.CharField(max_length=60, blank=False, verbose_name="General Manager")

	def __unicode__(self):
		return u'Staples: %s at %s' % (self.store_no, self.store_name)

	class Meta:
		verbose_name_plural = u'Staples Stores'

	def save(self, *args, **kwargs):
		super(StaplesStores, self).save(*args, **kwargs)

"""
Name:           StaplesChallenge
Date created:   May 4, 2014
Description:    
"""
class StaplesChallenge(models.Model):
	challenge = models.ForeignKey(Challenge, null=True, blank=True)
	clean_team = models.ForeignKey(CleanTeam, null=True, blank=True)
	staples_store = models.ForeignKey(StaplesStores, null=True, blank=True)

	def __unicode__(self):
		return u'%s selected %s' % (self.clean_team, self.staples_store)

	class Meta:
		verbose_name_plural = u'Staples Challenge Entries'

	@staticmethod
	def get_participating_store(clean_team):
		staples_challenge = StaplesChallenge.objects.get(clean_team=clean_team)

		return staples_challenge

	def save(self, *args, **kwargs):
		super(StaplesChallenge, self).save(*args, **kwargs)

"""
Name:           UserVoucher
Date created:   Mar 29, 2014
Description:    
"""
class UserVoucher(models.Model):
	voucher = models.CharField(max_length=60, blank=False, unique=True, verbose_name="Voucher")	
	user = models.ForeignKey(User, null=True, blank=True)
	challenge = models.ForeignKey(Challenge, null=True, blank=True)
	clean_creds = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = u'Voucher Codes'

	def claim_voucher(self, user):
		if self.voucher:	
			self.user = user

			if self.challenge:
				self.challenge.one_time_check_in_with_token(user, self.challenge.token)
			elif self.clean_creds:
				user.profile.add_clean_creds_to_individual_and_teams(self.clean_creds)

			self.save()

		return False

	def save(self, *args, **kwargs):
		super(UserVoucher, self).save(*args, **kwargs)

"""
Name:           CleanGrid
Date created:   Feb 3, 2014
Description:    The Clean Grid system for answer value calculation.
"""
class CleanGrid(models.Model):
	name = models.CharField(max_length=60, blank=False, default="None", verbose_name='Clean Grid Name')
	value = models.DecimalField(max_digits=10, decimal_places=6)

	class Meta:
		verbose_name_plural = u'Challenge question CleanGrid'

	def __unicode__(self):
		return u'CleanGrid: %s' %(self.name)

	def save(self, *args, **kwargs):
		super(CleanGrid, self).save(*args, **kwargs)

"""
Name:           ChallengeQuestionType
Date created:   Feb 3, 2014
Description:    The questions types.
"""
class ChallengeQuestionType(models.Model):
	name = models.CharField(max_length=60, blank=False, default="None", unique=True, verbose_name='Question Type Name')
	description = models.TextField(blank=False, default="")

	class Meta:
		verbose_name_plural = u'Challenge question type'

	def __unicode__(self):
		return u'Question Type: %s' %(self.name)

	def save(self, *args, **kwargs):
		super(ChallengeQuestionType, self).save(*args, **kwargs)

"""
Name:           AnswerType
Date created:   Feb 3, 2014
Description:    The asnwer types.
"""
class AnswerType(models.Model):
	name = models.CharField(max_length=60, blank=False, default="None", unique=True, verbose_name='Answer Type Name')
	description = models.TextField(blank=False, default="")

	class Meta:
		verbose_name_plural = u'Challenge answer type'

	def __unicode__(self):
		return u'Answer Type: %s' %(self.name)

	def save(self, *args, **kwargs):
		super(AnswerType, self).save(*args, **kwargs)

"""
Name:           ChallengeQuestion
Date created:   Feb 3, 2014
Description:    The questions that need to be answered to determine the
				CleanCred per hour value.
"""
class ChallengeQuestion(models.Model):
	question_number = models.IntegerField(default=0)	
	question = models.TextField(blank=False, default="None", verbose_name='Question')
	type = models.ForeignKey(ChallengeQuestionType, blank=True, default=1)
	answer_type = models.ForeignKey(AnswerType, blank=True, default=1)
	required = models.BooleanField(default=True)

	class Meta:
		verbose_name_plural = u'Challenge questions'

	def __unicode__(self):
		return u'Question: %s. %s' %(self.question_number, self.question)

	def save(self, *args, **kwargs):
		super(ChallengeQuestion, self).save(*args, **kwargs)

"""
Name:           QuestionAnswer
Date created:   Feb 3, 2014
Description:    The answer to each question and the value of each answer.
"""
class QuestionAnswer(models.Model):
	question = models.ForeignKey(ChallengeQuestion)
	answer_number = models.CharField(max_length=1, blank=False, null=False, default="A", verbose_name="Answer Number")
	answer = models.CharField(max_length=60, blank=False, default="None", verbose_name='Answer')
	score = models.IntegerField(blank=True, null=True, default=None)
	clean_grid = models.ForeignKey(CleanGrid, null=True, blank=True, default=None)

	class Meta:
		verbose_name_plural = u'Challenge question answer'

	def get_answer_score(self):
		if self.score is not None:
			return self.score
		else:
			return int(math.ceil(self.clean_grid.value))

	def __unicode__(self):
		return u'Question Answer: %s: %s' %(self.question, self.answer)

	def save(self, *args, **kwargs):
		super(QuestionAnswer, self).save(*args, **kwargs)

"""
Name:           UserChallengeSurvey
Date created:   Feb 17 2014
Description:    The survey each User creates for the Challenge.
"""
class UserChallengeSurvey(models.Model): 
	user = models.ForeignKey(User)
	clean_team = models.ForeignKey(CleanTeam)
	challenge = models.ForeignKey(Challenge)
	total_score = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = u'User Challenge Surveys'

	def create_survey(self, challenge, form):
		self.user = challenge.user
		self.clean_team = challenge.clean_team
		self.challenge = challenge
		self.save()

		total_score = 0

		for question, answers in form.items():			
			if question.startswith("question_"):
				if isinstance(answers, list):
					for answer in answers:
						try:	
							if answer != "":
								answer = int(answer)
								ans = QuestionAnswer.objects.get(id=answer)

								total_score += ans.get_answer_score()

								user_answer = UserChallengeSurveyAnswers(survey=self, answer=ans)
								user_answer.save()
						except Exception, e:
							print e
							return False
				else:
					try:
						if answers != "":
							answers = int(answers)
							ans = QuestionAnswer.objects.get(id=answers)

							total_score += ans.get_answer_score()

							user_answer = UserChallengeSurveyAnswers(survey=self, answer=ans)
							user_answer.save()
					except Exception, e:
						print e
						return False

		self.total_score = total_score
		self.save()

		challenge.clean_creds_per_hour = total_score
		challenge.save()

		return True

	def __unicode__(self):
		return u'User Challenge Survey: %s:' %(self.user)

	def save(self, *args, **kwargs):
		super(UserChallengeSurvey, self).save(*args, **kwargs)

"""
Name:           UserChallengeSurveyAnswers
Date created:   Feb 17 2014
Description:    The survey answer that each User gives for the Challenge.
"""
class UserChallengeSurveyAnswers(models.Model): 
	survey = models.ForeignKey(UserChallengeSurvey)
	answer = models.ForeignKey(QuestionAnswer)

	class Meta:
		verbose_name_plural = u'User Challenge Survey Answers'

	def __unicode__(self):
		return u'User Challenge Survey Answer: %s' %(self.answer)

	def save(self, *args, **kwargs):
		super(UserChallengeSurveyAnswers, self).save(*args, **kwargs)