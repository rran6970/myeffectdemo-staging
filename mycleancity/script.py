import math
import string

from datetime import date

from django.contrib.auth.models import User

from challenges.models import *
from cleanteams.models import *
from mycleancity.actions import *
from userprofile.models import *

# To run this script:
# from mycleancity.script import *; add_settings_to_all_user_profiles()
def add_settings_to_all_user_profiles():
	users = User.objects.all()

	for user in users:
		try:
			user_profile = UserProfile.objects.get(user=user)
			settings, created = UserSettings.objects.get_or_create(user=user_profile.user)
			settings.save()

			if created:
				user_profile.settings = UserSettings.objects.latest('id')
				print "Created settings for %s" % user_profile.user.email
			else:
				user_profile.settings = settings
				print "Settings existed for %s, assigning to UserProfile" % user_profile.user.email

			user_profile.save()

		except Exception, e:
			user_profile = UserProfile()
			user_profile.user = user
			user_profile.save()

			print "No profile for %s: CREATED" % user_profile.user.email


# To run this script:
# from mycleancity.script import *; add_qrcodes_to_all_user_profiles()
def add_qrcodes_to_all_user_profiles():
	users = User.objects.all()

	for user in users:
		try:
			user_profile = UserProfile.objects.get(user=user)
			qr_code, created = UserQRCode.objects.get_or_create(user=user, data='%s' % (user_profile.user.id))

			if created:
				user_profile.qr_code = UserQRCode.objects.latest('id')
				print "Created QR Code for %s" % user_profile.user.email
			else:
				user_profile.qr_code = qr_code
				print "QR Code existed for %s, assigning to UserProfile" % user_profile.user.email

			user_profile.save()

		except Exception, e:
			print e
			user_profile = UserProfile()
			user_profile.user = user
			user_profile.save()

			print "No profile for %s: CREATED" % user_profile.user.email


# To run this script:
# from mycleancity.script import *; add_qrcodes_to_all_challenges()
def add_qrcodes_to_all_challenges():
	challenges = Challenge.objects.all()
	site_url = current_site_url()

	for challenge in challenges:
		try:
			qr_code, created = ChallengeQRCode.objects.get_or_create(data='%schallenges/one-time-check-in/%s/%s' % (site_url, challenge.id, challenge.token))

			if created:
				challenge.qr_code = ChallengeQRCode.objects.latest('id')
				print "Created QR Code for %s" % challenge.title

			challenge.save()

		except Exception, e:
			print e


# To run this script:
# from mycleancity.script import *; add_tokens_to_all_challenges()
def add_tokens_to_all_challenges():
	challenges = Challenge.objects.all()
	char_set = string.ascii_lowercase + string.digits

	for challenge in challenges:
		token = ''.join(random.sample(char_set*20,20))

		challenge.token = token
		challenge.save()
	

# CAUTION: VERY DANGEROUS SCRIPT
# To run this script:
# from mycleancity.script import *; add_clean_creds_to_earlybirds()
def add_clean_creds_to_earlybirds():
	users = User.objects.all()

	for user in users:
		print user.email
		user.profile.clean_creds = 0
		print "!!!CleanCreds reset!!!"
		early_bird_date = date(2014, 03, 19)

		if user.date_joined.date() <= early_bird_date:
			print "Joined before: %s" %(str(early_bird_date))
			user.profile.add_clean_creds(50)
			user.profile.save()
			print "Total CleanCreds: %s" %(str(user.profile.clean_creds))
		else:
			print "Joined on: %s" % (str(user.date_joined.date()))
			print "Total CleanCreds: %s" %(str(user.profile.clean_creds))
		print "--------------------------"


# CAUTION: VERY DANGEROUS SCRIPT
# To run this script:
# from mycleancity.script import *; add_clean_creds_to_clean_champions()
def add_clean_creds_to_clean_champions():
	users = User.objects.all()

	for user in users:
		print user.email
		clean_champions = CleanChampion.objects.filter(user=user)

		clean_creds = 0
		for clean_champion in clean_champions:
			clean_creds += 20
		
		print "Clean Champion in %s teams" % (str(clean_creds/20))
		print "Total CleanCreds to be added: %s" % (str(clean_creds))
		user.profile.add_clean_creds(clean_creds)
		user.profile.save()
		print "--------------------------"


# CAUTION: VERY DANGEROUS SCRIPT
# To run this script:
# from mycleancity.script import *; add_clean_creds_to_clean_ambassadors()
def add_clean_creds_to_clean_ambassadors():
	users = User.objects.all()

	for user in users:
		print user.email
		clean_ambassadors = CleanTeamMember.objects.filter(user=user)

		counter = 0
		for clean_ambassador in clean_ambassadors:
			if clean_ambassador.role == "clean-ambassador" and clean_ambassador.status == "approved":
				counter += 1

				print "Clean Ambassador in %s team" % (str(counter))
				print "Total CleanCreds added: %s" % (str(50))
				user.profile.add_clean_creds(50)
				user.profile.save()
				print "--------------------------"


# CAUTION: VERY DANGEROUS SCRIPT
# To run this script:
# from mycleancity.script import *; add_clean_creds_to_clean_teams()
def add_clean_creds_to_clean_teams():
	clean_teams = CleanTeam.objects.all()

	for clean_team in clean_teams:
		print clean_team.name
		clean_champions = CleanChampion.objects.filter(clean_team=clean_team)

		clean_creds = 0
		for clean_champion in clean_champions:
			clean_creds += 5

		print "Total Clean Champions: %s" %(str(clean_creds/5))
		print "Total CleanCreds: %s" %(str(clean_creds))
		clean_team.clean_creds = clean_creds
		clean_team.save()
		print "--------------------------"


# CAUTION: VERY DANGEROUS SCRIPT
# To run this script:
# from mycleancity.script import *; execute_all_clean_cred_adding_functions()
def execute_all_clean_cred_adding_functions():
	add_clean_creds_to_earlybirds()
	add_clean_creds_to_clean_champions()
	add_clean_creds_to_clean_ambassadors()
	add_clean_creds_to_clean_teams()