import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms.extras.widgets import SelectDateWidget
from challenges.models import Challenge, UserChallenge

class NewChallengeForm(forms.ModelForm):
	event_date = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'datepicker'}))
	event_time = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'timepicker'}))

	class Meta:
		model = Challenge
		exclude = ('user')