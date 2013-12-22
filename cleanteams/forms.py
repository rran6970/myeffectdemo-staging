import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from cleanteams.models import CleanTeam

class RegisterCleanTeamForm(forms.ModelForm):
	name = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
	website = forms.URLField(required=True, initial="http://", max_length=128, min_length=2, widget=forms.TextInput())
	logo = forms.ImageField(required=False)
	about = forms.CharField(required=False, widget=forms.Textarea())
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
		clean_team_id = cleaned_data.get('clean_team_id')

		if not name:
			raise forms.ValidationError("Please enter your Clean Team's name")
		elif not website:
			raise forms.ValidationError("Please enter your website")
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