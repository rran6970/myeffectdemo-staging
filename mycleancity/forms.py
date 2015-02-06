import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms.extras.widgets import SelectDateWidget

from captcha.fields import ReCaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput())
    email = forms.EmailField(widget=forms.TextInput())
    subject = forms.CharField(widget=forms.TextInput())
    message = forms.CharField(widget=forms.Textarea())
    receive_newsletters = forms.BooleanField(required=False)
    captcha = ReCaptchaField()
    # testing 123 testing testing
    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get("name")
        email = cleaned_data.get("email")
        subject = cleaned_data.get("subject")
        message = cleaned_data.get("message")
        receive_newsletters = cleaned_data.get('receive_newsletters')
        captcha = cleaned_data.get('captcha')

        if not name and email and subject and message:
            raise forms.ValidationError("Please enter all of the fields")
        elif not name:
            raise forms.ValidationError("Please let us know what to call you!")
        elif not email:
            raise forms.ValidationError("Please enter a valid email address")
        elif not subject:
            raise forms.ValidationError("Please enter a valid subject")
        elif not message:
            raise forms.ValidationError("Please enter a message")
        elif not captcha:
            raise forms.ValidationError("Please enter the CAPTCHA field correctly")

        return cleaned_data

class ContactForLicenceForm(forms.Form):
    name = forms.CharField(label='Your Name *', max_length=50, widget=forms.TextInput())
    email = forms.EmailField(label='Email *', widget=forms.TextInput())
    organization = forms.CharField(label='Organization *', widget=forms.TextInput())
    position = forms.CharField(label='Position', required=False, widget=forms.TextInput())
    number_of_users = forms.CharField(label='Number of users', required=False, widget=forms.TextInput())
    message = forms.CharField(label='Message', widget=forms.Textarea())
    captcha = ReCaptchaField()

    def clean(self):
        cleaned_data = super(ContactForLicenceForm, self).clean()
        name = cleaned_data.get("name")
        email = cleaned_data.get("email")
        organization = cleaned_data.get("organization")
        position = cleaned_data.get("position")
        number_of_users = cleaned_data.get("number_of_users")
        message = cleaned_data.get("message")
        captcha = cleaned_data.get('captcha')

        if not name:
            raise forms.ValidationError("Please let us know what to call you!")
        elif not email:
            raise forms.ValidationError("Please enter a valid email address")
        elif not organization:
            raise forms.ValidationError("Please enter a organization name")
        elif not message:
            raise forms.ValidationError("Please enter a message")
        elif not captcha:
            raise forms.ValidationError("Please enter the CAPTCHA field correctly")

        return cleaned_data