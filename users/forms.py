import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms.extras.widgets import SelectDateWidget
from users.models import PrelaunchEmails
from userprofile.models import UserProfile
from userorganization.models import UserOrganization

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

SCHOOLS = (('', 'Please select one...'),('Elementary Student', 'Elementary Student'), ('High School Student', 'High School Student'), ('Post Secondary Student', 'Post Secondary Student'))

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

class PrelaunchEmailsForm(forms.ModelForm):
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'First name'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email address'}))
	postal_code = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'placeholder':'Postal code'}))
	school_type = forms.ChoiceField(widget=forms.Select(), choices=SCHOOLS)
	ambassador = forms.BooleanField(label="I'd like to participate as an ambassador", required=False)

	# Combines the form with the corresponding model
	class Meta:
		model = PrelaunchEmails

	def clean(self):
		cleaned_data = super(PrelaunchEmailsForm, self).clean()
		first_name = cleaned_data.get("first_name")
		email = cleaned_data.get("email")
		postal_code = cleaned_data.get("postal_code")
		school_type = cleaned_data.get("school_type")

		if not first_name:
			raise forms.ValidationError("Please let us know what to call you!")
		elif not email:
			raise forms.error
		elif not postal_code:
			raise forms.ValidationError("Please enter a valid postal code")
		elif not school_type:
			raise forms.ValidationError("Please select your education")

		return cleaned_data

class RegisterUserForm(forms.ModelForm):
	CHOICES = (('individual', 'Individual',), ('clean-ambassador', 'Clean Ambassador',), ('clean-champion', 'Clean Champion',))

	first_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	last_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	email = forms.CharField(required=True, max_length = 128, widget=forms.TextInput())
	password = forms.CharField(required=True, max_length = 32, widget = forms.PasswordInput())
	confirm_password = forms.CharField(required=True, max_length = 32, widget = forms.PasswordInput())
	city = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	province = forms.ChoiceField(widget=forms.Select(), choices=PROVINCES)
	school_type = forms.ChoiceField(widget=forms.Select(), choices=SCHOOLS)
	role = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
	
	# Combines the form with the corresponding model
	class Meta:
		model = User
		exclude = ('username', 'last_login', 'date_joined')

	def clean(self):
		cleaned_data = super(RegisterUserForm, self).clean()
		first_name = cleaned_data.get('first_name')
		last_name = cleaned_data.get('last_name')
		email = cleaned_data.get('email')
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		city = cleaned_data.get('city')
		province = cleaned_data.get('province')
		school_type = cleaned_data.get('school_type')
		role = cleaned_data.get('role')

		if not first_name:
			raise forms.ValidationError("Please enter your first name")
		elif not last_name:
			raise forms.ValidationError("Please enter your last name")
		elif not email:
			raise forms.ValidationError("Please enter a valid email address")
		elif not password:
			raise forms.ValidationError("Please enter a password")
		elif not confirm_password:
			raise forms.ValidationError("Please confirm your password")
		elif not city:
			raise forms.ValidationError("Please select your city")
		elif not province:
			raise forms.ValidationError("Please select your province")
		elif not school_type:
			raise forms.ValidationError("Please select your school type")

		if password and confirm_password:
			if password != confirm_password:
				raise forms.ValidationError('Passwords did not match')

		if User.objects.filter(username = email):
			raise forms.ValidationError(u'%s is already registered' % email)

		if len(password) < 8:
			raise forms.ValidationError(u'Password must be at least 8 characters')

		return cleaned_data

class ProfileForm(forms.ModelForm):
	first_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	last_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	email = forms.CharField(required=True, max_length = 128, widget=forms.TextInput())
	about = forms.CharField(required=False, widget=forms.Textarea())
	# dob = forms.DateField(required=True, initial=datetime.date.today, label="Date of Birth (YYYY-MM-DD)", widget=forms.TextInput(attrs={'class':'datepicker'}))
	school_type = forms.ChoiceField(widget=forms.Select(), choices=SCHOOLS)
	
	# Combines the form with the corresponding model
	class Meta:
		model = User
		exclude = ('username', 'last_login', 'date_joined', 'password')

	def clean(self):
		cleaned_data = super(ProfileForm, self).clean()
		first_name = cleaned_data.get("first_name")
		last_name = cleaned_data.get("last_name")
		email = cleaned_data.get("email")
		school_type = cleaned_data.get("school_type")

		if not first_name:
			raise forms.ValidationError("Please enter your first name")
		elif not last_name:
			raise forms.ValidationError("Please enter your last name")
		elif not email:
			raise forms.ValidationError("Please enter a valid email address")
		elif not school_type:
			raise forms.ValidationError("Please select your school type")

		return cleaned_data

class OrganizationProfileForm(forms.ModelForm):
	first_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	last_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	organization = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	email = forms.CharField(required=True, max_length = 128, widget=forms.TextInput())
	
	city = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	province = forms.ChoiceField(widget=forms.Select(), choices=PROVINCES)
	postal_code = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
	country = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
	website = forms.URLField(required=True, initial="http://", max_length = 128, min_length = 2, widget=forms.TextInput())
	about = forms.CharField(required=False, widget=forms.Textarea())

	
	# Combines the form with the corresponding model
	class Meta:
		model = User
		exclude = ('username', 'last_login', 'date_joined', 'password')

	def clean(self):
		cleaned_data = super(OrganizationProfileForm, self).clean()
		first_name = cleaned_data.get('first_name')
		last_name = cleaned_data.get('last_name')
		email = cleaned_data.get('email')
		organization = cleaned_data.get('organization')
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		city = cleaned_data.get('city')
		province = cleaned_data.get('province')
		website = cleaned_data.get('website')

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
		elif not city:
			raise forms.ValidationError("Please select your city")
		elif not province:
			raise forms.ValidationError("Please select your province")
		elif not website:
			raise forms.ValidationError("Please enter your website")

		return cleaned_data	