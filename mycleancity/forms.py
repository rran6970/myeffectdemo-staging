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