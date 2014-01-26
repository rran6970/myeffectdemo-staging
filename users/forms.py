import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.files.images import get_image_dimensions
from django.forms.extras.widgets import SelectDateWidget

from captcha.fields import CaptchaField

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
	ROLE_CHOICES = (('individual', 'Individual',), ('clean-ambassador', 'Clean Ambassador',), ('clean-champion', 'Clean Champion',))
	AGE_CHOICES = (('13-16', '13-16',), ('17-21', '17-21',), ('22-25', '22-25',))

	first_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	last_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	email = forms.CharField(required=True, max_length = 128, widget=forms.TextInput())
	password = forms.CharField(required=True, max_length = 32, widget = forms.PasswordInput())
	confirm_password = forms.CharField(required=True, max_length = 32, widget = forms.PasswordInput())
	city = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	province = forms.ChoiceField(widget=forms.Select(), choices=PROVINCES)
	# school_type = forms.ChoiceField(widget=forms.Select(), choices=SCHOOLS)
	age = forms.ChoiceField(widget=forms.Select(), choices=AGE_CHOICES, label="Age range")
	role = forms.ChoiceField(widget=forms.RadioSelect, choices=ROLE_CHOICES)
	smartphone = forms.BooleanField(required=False)
	uea = forms.BooleanField(required=True)
	token = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())
	captcha = CaptchaField()
	
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
		# school_type = cleaned_data.get('school_type')
		role = cleaned_data.get('role')
		age = cleaned_data.get('age')
		uea = cleaned_data.get('uea')
		captcha = cleaned_data.get('captcha')
		token = cleaned_data.get('token')

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
		# elif not school_type:
		# 	raise forms.ValidationError("Please select your school type")
		elif not uea:
			raise forms.ValidationError("Please accept the Terms & Conditions")
		elif not captcha:
			raise forms.ValidationError("Please enter the CAPTCHA field correctly")
		elif not age:
			raise forms.ValidationError("Please select your age range")

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
	twitter = forms.CharField(required=False, initial="@", max_length = 128, min_length=1, widget=forms.TextInput())
	# dob = forms.DateField(required=True, initial=datetime.date.today, label="Date of Birth (YYYY-MM-DD)", widget=forms.TextInput(attrs={'class':'datepicker'}))
	school_type = forms.ChoiceField(widget=forms.Select(), choices=SCHOOLS)
	picture = forms.ImageField(required=True, label="Profile Picture")
	
	# Combines the form with the corresponding model
	class Meta:
		model = User
		exclude = ('username', 'last_login', 'date_joined', 'password')

	def clean(self):
		cleaned_data = super(ProfileForm, self).clean()
		first_name = cleaned_data.get("first_name")
		last_name = cleaned_data.get("last_name")
		email = cleaned_data.get("email")
		about = cleaned_data.get("about")
		twitter = cleaned_data.get("twitter")
		school_type = cleaned_data.get("school_type")
		picture = cleaned_data.get("picture")

		if not first_name:
			raise forms.ValidationError("Please enter your first name")
		elif not last_name:
			raise forms.ValidationError("Please enter your last name")
		elif not email:
			raise forms.ValidationError("Please enter a valid email address")
		elif not school_type:
			raise forms.ValidationError("Please select your school type")

		if picture:
			if picture._size > 2*1024*1024:
				raise forms.ValidationError("Image file must be smaller than 2MB")

			w, h = get_image_dimensions(picture)

			if w != 124:
				raise forms.ValidationError("The image is supposed to be 124px X 124px")
			if h != 124:
				raise forms.ValidationError("The image is supposed to be 124px X 124px")

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