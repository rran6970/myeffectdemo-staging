import re

from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from users.models import PrelaunchEmails

"""
Form validators
"""

def username_is_unique(value):
	if User.objects.filter(username = value):
		raise forms.ValidationError(u'%s is already registered' % value)

def username_exists(value):
	if not User.objects.filter(username = value):
		raise forms.ValidationError(u'%s is not a valid user' % value)

def username_format_is_valid(value):
	if not value:
		raise forms.ValidationError(u'Invalid email address')
	if not re.match(r'\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b', value,
		re.IGNORECASE):
		raise forms.ValidationError(u'%s is not a valid email address' % value)

def password_length_sufficient(value):
	if len(value) < 8:
		raise forms.ValidationError(u'Password must be at least 8 characters')

def country_is_valid(country):
	_countries = pycountry.countries
	countries = []
	for _country in _countries:
		if getattr(_country, 'alpha2', False):
			countries.append(_country.alpha2)
	if str(country) not in countries:
		raise forms.ValidationError('Invalid country')

SCHOOLS = (('high_school', 'High School'), ('post_secondary', 'Post Secondary'))
class PrelaunchEmailsForm(forms.ModelForm):
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'First name'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email address'}))
	postal_code = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'placeholder':'Postal code'}))
	school_type = forms.ChoiceField(choices=SCHOOLS)
	ambassador = forms.BooleanField(label="I'd like to participate as an ambassador", required=False)

	# Combines the form with the corresponding model
	class Meta:
		model = PrelaunchEmails

	def clean(self):
		cleaned_data = super(PrelaunchEmailsForm, self).clean()
		first_name = cleaned_data.get("first_name")
		email = cleaned_data.get("email")
		postal_code = cleaned_data.get("postal_code")

		if not first_name and email and postal_code:
			raise forms.ValidationError("Please enter all of the fields")
		elif not first_name:
			raise forms.ValidationError("Please let us know what to call you!")
		elif not email:
			raise forms.ValidationError("Please enter a valid email address")
		elif not postal_code:
			raise forms.ValidationError("Please enter a valid postal code")

		return cleaned_data

class RegisterUserForm(forms.ModelForm):
	email = forms.CharField(max_length = 128, validators = [
		username_format_is_valid, username_is_unique], widget=forms.TextInput(attrs={'class':'required'}))
	password = forms.CharField(max_length = 32, widget = forms.PasswordInput(attrs={'class':'required'}),
		validators = [password_length_sufficient])
	confirm_password = forms.CharField(max_length = 32,
		widget = forms.PasswordInput(attrs={'class':'required'}))
	first_name = forms.CharField(max_length = 128, min_length = 2, widget=forms.TextInput(attrs={'class':'autofocus required'}))
	last_name = forms.CharField(max_length = 128, min_length = 2, widget=forms.TextInput(attrs={'class':'required'}))

	# Combines the form with the corresponding model
	class Meta:
		model = User

	def clean(self):
		cleaned_data = self.cleaned_data
		passwd1 = cleaned_data.get('password')
		passwd2 = cleaned_data.get('confirm_password')

		if passwd1 and passwd2:
			if passwd1 != passwd2:
				raise forms.ValidationError('Passwords did not match')

		# for key in cleaned_data:
		# 	if key in cleaned_data:
		# 		key = key.title()
		# 	else:
		# 		raise forms.ValidationError('First name is required')

		if 'first_name' in cleaned_data:
			self.cleaned_data['first_name'] = cleaned_data['first_name'].title()
		else:
			raise forms.ValidationError('First name is required')

		if 'last_name' in cleaned_data:
			self.cleaned_data['last_name'] = cleaned_data['last_name'].title()
		else:
			raise forms.ValidationError('Last name is required')

		if 'email' in cleaned_data:
			self.cleaned_data['email'] = cleaned_data['email'].title()
		else:
			raise forms.ValidationError('Email is required')

		if 'password' in cleaned_data:
			self.cleaned_data['password'] = cleaned_data['password'].title()
		else:
			raise forms.ValidationError('Password is required')

		if 'confirm_password' in cleaned_data:
			self.cleaned_data['confirm_password'] = cleaned_data['confirm_password'].title()
		else:
			raise forms.ValidationError('Confirm password is required')

		return cleaned_data

class LoginUserForm(forms.Form):
	email = forms.CharField(max_length = 128, validators = [
		username_format_is_valid, username_exists], widget=forms.TextInput(attrs={'class':'required', 'placeholder':'Email Address'}))
	password = forms.CharField(max_length = 32, widget = forms.PasswordInput(attrs={'class':'required', 'placeholder':'********'}))

	def clean(self):
		cleaned_data = self.cleaned_data

		if 'email' in cleaned_data and 'password' in cleaned_data:
			user = authenticate(username = cleaned_data['email'],
				password = cleaned_data['password'])
			if user is None or not user.is_active:
				raise forms.ValidationError('Email address and password are not valid. If you are not currenly a member please sign up at "Become a Member".')
		else:
			raise forms.ValidationError('Please provide an email address and password.')
		return cleaned_data
