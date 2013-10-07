import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms.extras.widgets import SelectDateWidget
from challenges.models import Challenge, UserChallenge

PROVINCES = (('', 'Please select one...'),
	('AB', 'AB'), 
	('BC', 'BC'), 
	('MB', 'MB'),
	('NB', 'NB'),
	('NF', 'NF'),
	('NW', 'NW'),
	('NS', 'NS'),
	('NU', 'NU'),
	('ON', 'ON'),
	('PEI', 'PEI'),
	('QB', 'QB'),
	('SA', 'SA'),
	('YU', 'YU'),
)

class NewChallengeForm(forms.ModelForm):
	event_date = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'datepicker'}))
	event_time = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'timepicker'}))
	province = forms.ChoiceField(choices=PROVINCES)

	class Meta:
		model = Challenge
		exclude = ('user')

	def clean(self):
		cleaned_data = super(NewChallengeForm, self).clean()
		title = cleaned_data.get("title")
		cleancred_value = cleaned_data.get("cleancred_value")
		event_date = cleaned_data.get("event_date")
		event_time = cleaned_data.get("event_time")
		address1 = cleaned_data.get("address1")
		address2 = cleaned_data.get("address2")
		city = cleaned_data.get("city")
		province = cleaned_data.get("province")
		country = cleaned_data.get("country")
		postal_code = cleaned_data.get("postal_code")
		description = cleaned_data.get("description")

		if not title:
			raise forms.ValidationError("Please enter a title")
		elif not cleancred_value:
			raise forms.ValidationError("Please enter a number for the Clean Cred value")
		elif not event_date:
			raise forms.ValidationError("Please enter an event date")
		elif not event_time:
			raise forms.ValidationError("Please enter an event time")
		elif not address1:
			raise forms.ValidationError("Please enter an address")
		elif not city:
			raise forms.ValidationError("Please enter a city")
		elif not province:
			raise forms.ValidationError("Please select a province")	
		elif not country:
			raise forms.ValidationError("Please enter a country")		
		elif not postal_code:
			raise forms.ValidationError("Please enter a postal code")	
		elif not description:
			raise forms.ValidationError("Please enter a description")		
		return cleaned_data