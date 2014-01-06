import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from cleanteams.models import CleanTeam, CleanTeamInvite

CLEAN_TEAM_TYPES = (('', 'Please select one...'),
	('independent', 'Independent'), 
	('representing', 'Representing a school or group'),
)

class RegisterCleanTeamForm(forms.ModelForm):
	name = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
	website = forms.URLField(required=False, initial="http://", max_length=128, min_length=2, widget=forms.TextInput())
	logo = forms.ImageField(required=False)
	about = forms.CharField(required=False, widget=forms.Textarea())
	twitter = forms.CharField(required=False, initial="@", max_length = 128, min_length=2, widget=forms.TextInput())
	region = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
	team_type = forms.ChoiceField(widget=forms.Select(), choices=CLEAN_TEAM_TYPES)
	group = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput())
	clean_team_id = forms.CharField(required=False, widget=forms.HiddenInput())

	# Combines the form with the corresponding model
	class Meta:
		model = CleanTeam
		exclude = ('clean_creds')

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
		# elif not logo:
		# 	raise forms.ValidationError("Please upload your logo")

		if CleanTeam.objects.filter(name=name) and not clean_team_id:
			raise forms.ValidationError(u'%s already exists' % name)

		return cleaned_data


CHOICES = (
	('create-new-team', 'Create a new team'), 
	('join-existing-team', 'Join an existing team'),
)

class CreateTeamOrJoinForm(forms.Form):
	selections = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class RequestJoinTeamsForm(forms.Form):
	team = forms.ModelChoiceField(required=True, queryset=CleanTeam.objects.all())

class JoinTeamCleanChampionForm(forms.Form):
	team = forms.ModelChoiceField(required=True, queryset=CleanTeam.objects.all())


ROLE_CHOICES = (
	('clean-ambassador', 'Clean Ambassador'), 
	('clean-champion', 'Clean Champion'),
)

class InviteForm(forms.Form):
	email = forms.CharField(required=True, max_length=128, widget=forms.TextInput())
	role = forms.ChoiceField(widget=forms.Select(), choices=ROLE_CHOICES)

	# Combines the form with the corresponding model
	class Meta:
		model = CleanTeamInvite
		exclude = ('clean_team', 'user', 'role', 'status')

	def clean(self):
		cleaned_data = super(InviteForm, self).clean()
		email = cleaned_data.get('email')

		if not email:
			raise forms.ValidationError("Please enter an email")

		emails = CleanTeamInvite.objects.filter(email=email).count()

		if emails > 0:
			raise forms.ValidationError("Already invited")
		
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