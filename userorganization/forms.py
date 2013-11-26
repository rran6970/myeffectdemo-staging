import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class RegisterOrganizationForm(forms.ModelForm):
	first_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	last_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	email = forms.CharField(required=True, max_length = 128, widget=forms.TextInput())
	password = forms.CharField(required=True, max_length = 32, widget = forms.PasswordInput())
	confirm_password = forms.CharField(required=True, max_length = 32, widget = forms.PasswordInput())
	organization = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	city = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	province = forms.ChoiceField(widget=forms.Select(), choices=PROVINCES)
	postal_code = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
	country = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
	website = forms.URLField(required=True, initial="http://", max_length = 128, min_length = 2, widget=forms.TextInput())
	logo = forms.ImageField(required=True)

	# Combines the form with the corresponding model
	class Meta:
		model = User
		exclude = ('username', 'last_login', 'date_joined')

	def clean(self):
		cleaned_data = super(RegisterOrganizationForm, self).clean()
		first_name = cleaned_data.get('first_name')
		last_name = cleaned_data.get('last_name')
		email = cleaned_data.get('email')
		organization = cleaned_data.get('organization')
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		city = cleaned_data.get('city')
		province = cleaned_data.get('province')
		website = cleaned_data.get('website')
		logo = cleaned_data.get('logo')

		if not first_name:
			raise forms.ValidationError("Please enter your first name")
		elif not last_name:
			raise forms.ValidationError("Please enter your last name")
		# elif not email:
		# 	raise forms.ValidationError("Please enter a valid email address")
		# elif not password:
		# 	raise forms.ValidationError("Please enter a password")
		elif not organization:
			raise forms.ValidationError("Please enter your organization")
		elif not confirm_password:
			raise forms.ValidationError("Please confirm your password")
		elif not city:
			raise forms.ValidationError("Please select your city")
		elif not province:
			raise forms.ValidationError("Please select your province")
		elif not website:
			raise forms.ValidationError("Please enter your website")
		elif not logo:
			raise forms.ValidationError("Please upload your logo")

		if password and confirm_password:
			if password != confirm_password:
				raise forms.ValidationError('Passwords did not match')

		if User.objects.filter(username = email):
			raise forms.ValidationError(u'%s is already registered' % email)

		if len(password) < 8:
			raise forms.ValidationError(u'Password must be at least 8 characters')

		return cleaned_data