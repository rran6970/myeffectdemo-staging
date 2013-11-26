import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from cleanteams.models import CleanTeam

class RegisterCleanTeamForm(forms.ModelForm):
	name = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
	website = forms.URLField(required=True, initial="http://", max_length=128, min_length=2, widget=forms.TextInput())
	logo = forms.ImageField(required=True)

	# Combines the form with the corresponding model
	class Meta:
		model = CleanTeam
		exclude = ('clean_creds')

	def clean(self):
		cleaned_data = super(RegisterCleanTeamForm, self).clean()
		name = cleaned_data.get('name')
		website = cleaned_data.get('website')
		logo = cleaned_data.get('logo')

		if not name:
			raise forms.ValidationError("Please enter your Clean Team's name")
		elif not website:
			raise forms.ValidationError("Please enter your website")
		elif not logo:
			raise forms.ValidationError("Please upload your logo")

		if CleanTeam.objects.filter(name = name):
			raise forms.ValidationError(u'%s already exists' % name)

		return cleaned_data