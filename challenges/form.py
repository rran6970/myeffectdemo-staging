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