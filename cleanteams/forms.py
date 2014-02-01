import datetime
import re

from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.files.images import get_image_dimensions

from cleanteams.models import CleanTeam, CleanTeamInvite

CLEAN_TEAM_TYPES = (('', 'Please select one...'),
	('independent', 'Independent'), 
	('representing', 'Representing a school or group'),
)

class RegisterCleanTeamForm(forms.ModelForm):
	name = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
	website = forms.URLField(required=False, initial="", max_length=128, min_length=2, widget=forms.TextInput())
	logo = forms.ImageField(required=False)
	about = forms.CharField(required=False, widget=forms.Textarea())
	twitter = forms.CharField(required=False, initial="@", max_length = 128, min_length=1, widget=forms.TextInput())
	region = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
	team_type = forms.ChoiceField(widget=forms.Select(), choices=CLEAN_TEAM_TYPES)
	group = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput())
	clean_team_id = forms.CharField(required=False, widget=forms.HiddenInput())

	# Combines the form with the corresponding model
	class Meta:
		model = CleanTeam
		exclude = ('clean_creds', 'level')

	def clean(self):
		cleaned_data = super(RegisterCleanTeamForm, self).clean()
		name = cleaned_data.get('name')
		website = cleaned_data.get('website')
		logo = cleaned_data.get('logo')
		about = cleaned_data.get('about')
		twitter = cleaned_data.get('twitter')
		region = cleaned_data.get('region')
		team_type = cleaned_data.get('team_type')
		group = cleaned_data.get('group')
		clean_team_id = cleaned_data.get('clean_team_id')

		if not name:
			raise forms.ValidationError("Please enter your Clean Team's name")
		elif not region:
			raise forms.ValidationError("Please enter your region")
		elif not team_type:
			raise forms.ValidationError("Please select the type of team")

		if logo:
			if logo._size > 2*1024*1024:
				raise forms.ValidationError("Image file must be smaller than 2MB")

			w, h = get_image_dimensions(logo)

			if w != 124:
				raise forms.ValidationError("The image is supposed to be 124px X 124px")
			if h != 124:
				raise forms.ValidationError("The image is supposed to be 124px X 124px")

		if CleanTeam.objects.filter(name=name) and not clean_team_id:
			raise forms.ValidationError(u'%s already exists' % name)

		return cleaned_data

class RequestJoinTeamsForm(forms.Form):
	team = forms.ModelChoiceField(required=True, queryset=CleanTeam.objects.all())

class JoinTeamCleanChampionForm(forms.Form):
	team = forms.ModelChoiceField(required=True, queryset=CleanTeam.objects.all())

CREATE_OR_JOIN_CHOICES = (
	('create-new-team', 'Create a new team'), 
	('join-existing-team', 'Join an existing team'),
)

class CreateTeamOrJoinForm(forms.Form):
	selections = forms.ChoiceField(widget=forms.RadioSelect, choices=CREATE_OR_JOIN_CHOICES)
	invite = forms.CharField(required=False, widget=forms.HiddenInput())


RESPONSE_CHOICES = (
	('accepted', 'Accept'), 
	('declined', 'Decline'),
)
class InviteResponseForm(forms.Form):
	selections = forms.ChoiceField(widget=forms.RadioSelect, choices=RESPONSE_CHOICES)
	token = forms.CharField(required=True, widget=forms.HiddenInput())

ROLE_CHOICES = (
	('clean-ambassador', 'Clean Ambassador'), 
	('clean-champion', 'Clean Champion'),
)

class InviteForm(forms.Form):
	email = forms.CharField(required=True, max_length=128, widget=forms.TextInput())
	role = forms.ChoiceField(widget=forms.Select(), choices=ROLE_CHOICES)
	clean_team_id = forms.CharField(required=False, widget=forms.HiddenInput())

	# Combines the form with the corresponding model
	class Meta:
		model = CleanTeamInvite
		exclude = ('clean_team', 'user', 'role', 'status')

	def clean(self):
		cleaned_data = super(InviteForm, self).clean()
		email = cleaned_data.get('email')
		role = cleaned_data.get('role')
		clean_team_id = cleaned_data.get('clean_team_id')

		if not email:
			raise forms.ValidationError("Please enter an email")

		try:
			u = User.objects.get(email=email)

			if role == 'clean-ambassador':
				if u.profile.is_clean_ambassador() or u.profile.is_clean_ambassador("pending"):
					raise forms.ValidationError("%s is already a Clean Ambassador for %s" % (email, u.profile.clean_team_member.clean_team.name))

			if role == 'clean-champion':
				if u.profile.is_clean_champion(clean_team_id):
					raise forms.ValidationError("%s is already a Clean Clean Champion for your team" % (email))	
		except User.DoesNotExist, e:
			print e

		e = CleanTeamInvite.objects.filter(email=email, role=role, clean_team_id=clean_team_id).count()

		if e > 0:
			raise forms.ValidationError("Already invited for that role")

		return cleaned_data

class PostMessageForm(forms.Form):
	message = forms.CharField(required=False, widget=forms.Textarea())

	# Combines the form with the corresponding model
	class Meta:
		model = CleanTeam
		exclude = ('clean_creds')

	def clean(self):
		cleaned_data = super(PostMessageForm, self).clean()
		message = cleaned_data.get('message')

		if not message:
			raise forms.ValidationError("Please enter a message")

		return cleaned_data