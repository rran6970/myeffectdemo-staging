import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms.extras.widgets import SelectDateWidget
from challenges.models import Challenge, UserChallenge, Category

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
	title = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	category = forms.ModelChoiceField(required=True, queryset=Category.objects.all())
	event_date = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'datepicker'}))
	event_time = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'timepicker'}))
	address1 = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	address2 = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
	city = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	province = forms.ChoiceField(widget=forms.Select(), choices=PROVINCES)
	postal_code = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
	country = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
	description = forms.CharField(required=False, min_length = 2, widget=forms.Textarea())

	class Meta:
		model = Challenge
		exclude = ('user', 'clean_team')

	def clean(self):
		cleaned_data = super(NewChallengeForm, self).clean()
		title = cleaned_data.get("title")
		category = cleaned_data.get("category")
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
		elif not category:
			raise forms.ValidationError("Please select a category")
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