# !/usr/bin/env python
# coding: utf8

import datetime
import re
import pytz

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.files.images import get_image_dimensions
from django.forms.extras.widgets import SelectDateWidget
from captcha.fields import ReCaptchaField

from users.models import PrelaunchEmails
from userprofile.models import UserProfile, UserSettings

class CustomPasswordResetForm(PasswordResetForm):
    """
        Overriding the Email Password Resert Forms Save to be able to send HTML email
    """
    def save(self, domain_override=None, email_template_name='registration/reset_email.html', use_https=False, token_generator=default_token_generator, request=None, email_subject_name='registration/reset_subject.txt', **kwargs):
        from django.core.mail import EmailMultiAlternatives
        from django.utils.html import strip_tags
        from django.template.loader import render_to_string
        from django.contrib.sites.models import get_current_site
        from django.utils.http import int_to_base36

        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override

            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            render = render_to_string(email_template_name, c)
            render_subject = render_to_string(email_subject_name, c)

            msg = EmailMultiAlternatives(render_subject, strip_tags(render), None, [user.email])
            msg.attach_alternative(render, "text/html")
            msg.send()

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

COUNTRY = (('', 'Please select one'), ('Canada', 'Canada'), ('United States', 'United States'))

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
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
    ('other', 'Other')
)

CATEGORIES = (("------------------","-----------------"), ("Student","Student"), ("Professional","Professional"), ("Educator","Educator"))
COMM_CHOICES = (('English', 'English',), ('Français', 'Français',))
YES_NO_CHOICES = ((True, 'Yes'), (False, 'No'),)

class PrelaunchEmailsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'First name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email address'}))
    postal_code = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'placeholder':'Postal code'}))
    school_type = forms.ChoiceField(widget=forms.Select(), choices=SCHOOLS)
    ambassador = forms.BooleanField(label="I'd like to participate as an ambassador", required=False)
    join = forms.BooleanField(label="I'd like to join the My Effect team", required=False)

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
    ROLE_CHOICES = (('agent', 'Agent',), ('leader', 'Leader',), ('manager', 'Manager',))
    HEAR_CHOICES = (('Twitter', 'Twitter'), ('Instagram', 'Instagram'), ('Facebook', 'Facebook'), ('Google', 'Google'), ('Volunteer Posting', 'Volunteer Posting'), ('School Flyer', 'School Flyer'), ('Teacher', 'Teacher'), ('Friend', 'Friend'), ('Clean Leader', 'Clean Leader'), ('Website', 'Website'), ('H&M', 'H&M'), ('Staples', 'Staples'))

    first_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput(), label="First name")
    last_name = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput(), label="Last name")
    email = forms.CharField(required=True, max_length = 128, widget=forms.TextInput(), label="Email")
    password = forms.CharField(required=True, max_length = 32, widget = forms.PasswordInput(), label="Password")
    confirm_password = forms.CharField(required=True, max_length = 32, widget = forms.PasswordInput(), label="Confirm password")
    city = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput(), label="City")
    province = forms.ChoiceField(widget=forms.Select(), choices=PROVINCES, label="Province/State")
    country = forms.ChoiceField(widget=forms.Select(), choices=COUNTRY, label="Country")
    # school_type = forms.ChoiceField(widget=forms.Select(), choices=SCHOOLS)
    # student_id = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(), label="Student P/Profession")
    school_name = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(), label="School Name/Company Name")
    # age = forms.ChoiceField(widget=forms.Select(), choices=AGE_CHOICES, label="Age range / Tranche d’âge")
    role = forms.ChoiceField(widget=forms.RadioSelect, choices=ROLE_CHOICES, label="Role")
    communication_language = forms.ChoiceField(widget=forms.RadioSelect, choices=COMM_CHOICES, label="Communication Language")
    receive_newsletters = forms.BooleanField(required=False)
    smartphone = forms.BooleanField(required=False)
    hear_about_us = forms.ChoiceField(widget=forms.Select(), choices=HEAR_CHOICES, label="How did you hear about us?")
    uea = forms.BooleanField(required=True)
    data_privacy = forms.BooleanField(required=False)
    token = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())
    captcha = ReCaptchaField()
    dob = forms.DateField(widget=SelectDateWidget(years=range(1950, datetime.date.today().year)), label="Date of birth", required=True)

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
        # age = cleaned_data.get('age')
        dob = cleaned_data.get('dob')
        uea = cleaned_data.get('uea')
        receive_newsletters = cleaned_data.get('receive_newsletters')
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
        elif not dob:
            raise forms.ValidationError("Please select your date of birth")

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
    website = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'www.yourwebsite.com'}))
    twitter = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'@'}))
    facebook = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'Facebook'}))
    instagram = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'Instagram'}))
    google_plus = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'Google+'}))
    linkedin = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'Linkedin'}))
    street_address = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
    city = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
    province = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
    country = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
    postal_code = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
    emergency_phone = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(attrs={'class':'phone-number'}), label="Emergency phone number")
    picture = forms.ImageField(required=False, label="Profile picture")
    dob = forms.DateField(widget=SelectDateWidget(years=range(1950, datetime.date.today().year)), label="Date of birth", required=True)
    category = forms.ChoiceField(required=False, widget=forms.Select, choices=CATEGORIES, label="I am a(n)")
    emergency_contact_fname = forms.CharField(required=False, max_length=128, widget=forms.TextInput())
    emergency_contact_fname = forms.CharField(required=False, max_length=128, widget=forms.TextInput())
    smartphone = forms.BooleanField(required=False, label="Check this box if you have regular access to a smartphone.")
    # Combines the form with the corresponding model
    class Meta:
        model = User
        exclude = ('username', 'last_login', 'date_joined', 'password')

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        street_address = cleaned_data.get("street_address")
        city = cleaned_data.get("city")
        province = cleaned_data.get("province")
        country = cleaned_data.get("country")
        postal_code = cleaned_data.get("postal_code")
        email = cleaned_data.get("email")
        about = cleaned_data.get("about")
        website = cleaned_data.get("website")
        twitter = cleaned_data.get("twitter")
        facebook = cleaned_data.get("facebook")
        instagram = cleaned_data.get("instagram")
        google_plus = cleaned_data.get("google_plus")
        linkedin = cleaned_data.get("linkedin")
        school_type = cleaned_data.get("school_type")
        emergency_phone = cleaned_data.get("emergency_phone")
        picture = cleaned_data.get("picture")
        dob = cleaned_data.get('dob')

        if not first_name:
            raise forms.ValidationError("Please enter your first name")
        elif not last_name:
            raise forms.ValidationError("Please enter your last name")
        elif not email:
            raise forms.ValidationError("Please enter a valid email address")
        elif not dob:
            raise forms.ValidationError("Please select your date of birth")
        return cleaned_data

class SettingsForm(forms.ModelForm):
    communication_language = forms.ChoiceField(widget=forms.RadioSelect, choices=COMM_CHOICES, label="Communication language")
    email_privacy = forms.ChoiceField(widget=forms.RadioSelect, choices=YES_NO_CHOICES, label="Make email private?")
    data_privacy = forms.ChoiceField(widget=forms.RadioSelect, choices=YES_NO_CHOICES, label="I consent to share my volunteer data with organizations I work with")
    receive_newsletters = forms.ChoiceField(widget=forms.RadioSelect, choices=YES_NO_CHOICES, label="Receive My Effect email communications")
    timezone = forms.ChoiceField(widget=forms.Select(), choices=SCHOOLS, label="Select your timezone (default is America/Toronto)")

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['timezone'].choices = [(tz, tz) for tz in pytz.all_timezones]

    # Combines the form with the corresponding model
    class Meta:
        model = UserSettings
        exclude = ('user')

    def clean(self):
        cleaned_data = super(SettingsForm, self).clean()

        return cleaned_data
