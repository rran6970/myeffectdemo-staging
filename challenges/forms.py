import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms.extras.widgets import SelectDateWidget
from challenges.models import Challenge, UserChallenge, Category, ChallengeQuestion, QuestionAnswer

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
	event_date = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'datepicker', 'autocomplete':'off'}))
	event_time = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'timepicker', 'autocomplete':'off'}))
	address1 = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	address2 = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
	city = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
	province = forms.ChoiceField(widget=forms.Select(), choices=PROVINCES)
	postal_code = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
	country = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
	description = forms.CharField(required=False, min_length = 2, widget=forms.Textarea())
	host_organization = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(), label="Host Organization (if applicable)")
	challenge_id = forms.CharField(required=False, widget=forms.HiddenInput())

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
		host_organization = cleaned_data.get("host_organization")
		challenge_id = cleaned_data.get("challenge_id")

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

class ChallengeSurveyForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(ChallengeSurveyForm, self).__init__(*args, **kwargs)
		
		questions = ChallengeQuestion.objects.all().order_by('question_number')
		
		for question in questions:
			answers = QuestionAnswer.objects.filter(question=question).order_by('answer_number')
			answer_list = []

			for answer in answers:
				answer_list.append((answer.id, answer.answer))

			answer_tuple = tuple(answer_list)

			label = "%s. %s" %(question.question_number, question.question)	

			required = question.required

			if question.answer_type.name == "single":
				self.fields['question_%s' % question.question_number] = forms.ChoiceField(widget=forms.RadioSelect, required=required, label=label, choices=answer_tuple)
			elif question.answer_type.name == "multiple":
				self.fields['question_%s' % question.question_number] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=required, label=label, choices=answer_tuple)

			if question.question_number == 5:
				self.fields['question_%s' % question.question_number].widget.attrs['disabled'] = True













