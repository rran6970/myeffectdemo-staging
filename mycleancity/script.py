from django.contrib.auth.models import User

from userprofile.models import *

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

# from mycleancity.script import *; add_settings_to_all_user_profiles()

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


# from mycleancity.script import *; add_qrcodes_to_all_user_profiles()