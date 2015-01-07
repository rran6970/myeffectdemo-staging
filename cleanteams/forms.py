import datetime
import re

from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.files.images import get_image_dimensions

from cleanteams.models import CleanTeam, CleanTeamMember, CleanTeamInvite, LeaderReferral, CleanTeamPresentation

CLEAN_TEAM_TYPES = (('', 'Please select one...'),
	('independent', 'Independent'), 
	('representing', 'Representing a school or group'),
)

class RegisterCleanTeamForm(forms.ModelForm):
	name = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
	website = forms.URLField(required=False, max_length=128, min_length=2, widget=forms.TextInput())
	logo = forms.ImageField(required=False)
	about = forms.CharField(required=False, widget=forms.Textarea())
	twitter = forms.CharField(required=False, initial="@", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'@'}))
	region = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
	team_type = forms.ChoiceField(widget=forms.Select(), choices=CLEAN_TEAM_TYPES)
	group = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput())
	clean_team_id = forms.CharField(required=False, widget=forms.HiddenInput())
	role = forms.CharField(required=False, widget=forms.HiddenInput())
	contact_first_name = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput(attrs={'readonly':'readonly'}), label="First name")
	contact_last_name = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput(attrs={'readonly':'readonly'}), label="Last name")
	contact_phone = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput(attrs={'class':'phone-number'}), label="Phone number")
	contact_email = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput(attrs={'readonly':'readonly'}), label="Email address")
	
	# Combines the form with the corresponding model
	class Meta:
		model = CleanTeam
		exclude = ('clean_creds', 'level', 'contact_user')

	def clean(self):
		cleaned_data = super(RegisterCleanTeamForm, self).clean()
		name = cleaned_data.get('name')
		website = cleaned_data.get('website')
		logo = cleaned_data.get('logo')
		about = cleaned_data.get('about')
		twitter = cleaned_data.get('twitter')
		region = cleaned_data.get('region')
		team_type = cleaned_data.get('team_type')
		group = cleaned_data.get('group')
		contact_phone = cleaned_data.get('contact_phone')
		clean_team_id = cleaned_data.get('clean_team_id')

		contact_first_name = cleaned_data.get("contact_first_name")
		contact_last_name = cleaned_data.get("contact_last_name")
		contact_phone = cleaned_data.get("contact_phone")
		contact_email = cleaned_data.get("contact_email")

		if not name:
			raise forms.ValidationError("Please enter your Change Team's name")
		elif not region:
			raise forms.ValidationError("Please enter your region")
		elif not team_type:
			raise forms.ValidationError("Please select the type of team")
		elif not contact_phone:
			raise forms.ValidationError("Please enter a contact phone number")

		if logo:
			if logo._size > 2*1024*1024:
				raise forms.ValidationError("Image file must be smaller than 2MB")

			w, h = get_image_dimensions(logo)

			if w != 124:
				raise forms.ValidationError("The image is supposed to be 124px X 124px")
			if h != 124:
				raise forms.ValidationError("The image is supposed to be 124px X 124px")

		if CleanTeam.objects.filter(name=name) and not clean_team_id:
			raise forms.ValidationError(u'%s already exists' % name)

		return cleaned_data

class EditCleanTeamForm(forms.ModelForm):
	name = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
	website = forms.URLField(required=False, max_length=128, min_length=2, widget=forms.TextInput())
	logo = forms.ImageField(required=False)
	about = forms.CharField(required=False, widget=forms.Textarea())
	twitter = forms.CharField(required=False, initial="@", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'@'}))
	region = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
	team_type = forms.ChoiceField(widget=forms.Select(), choices=CLEAN_TEAM_TYPES)
	group = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput())
	clean_team_id = forms.CharField(required=False, widget=forms.HiddenInput())
	
	# Combines the form with the corresponding model
	class Meta:
		model = CleanTeam
		exclude = ('clean_creds', 'level', 'contact_user', 'contact_phone')

	def clean(self):
		cleaned_data = super(EditCleanTeamForm, self).clean()
		name = cleaned_data.get('name')
		website = cleaned_data.get('website')
		logo = cleaned_data.get('logo')
		about = cleaned_data.get('about')
		twitter = cleaned_data.get('twitter')
		region = cleaned_data.get('region')
		team_type = cleaned_data.get('team_type')
		group = cleaned_data.get('group')
		clean_team_id = cleaned_data.get('clean_team_id')

		if not name:
			raise forms.ValidationError("Please enter your Change Team's name")
		elif not region:
			raise forms.ValidationError("Please enter your region")
		elif not team_type:
			raise forms.ValidationError("Please select the type of team")

		if logo:
			if logo._size > 2*1024*1024:
				raise forms.ValidationError("Image file must be smaller than 2MB")

			w, h = get_image_dimensions(logo)

			if w != 124:
				raise forms.ValidationError("The image is supposed to be 124px X 124px")
			if h != 124:
				raise forms.ValidationError("The image is supposed to be 124px X 124px")

		if CleanTeam.objects.filter(name=name) and not clean_team_id:
			raise forms.ValidationError(u'%s already exists' % name)

		return cleaned_data

YEAR_IN_SCHOOL_CHOICES = (
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
)
class EditCleanTeamMainContact(forms.Form):
	contact_first_name = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(attrs={'readonly':'readonly'}), label="First name")
	contact_last_name = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(attrs={'readonly':'readonly'}), label="Last name")
	contact_phone = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(attrs={'class':'phone-number'}), label="Phone number")
	contact_email = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(attrs={'readonly':'readonly'}), label="Email address")
	clean_team_id = forms.CharField(required=False, widget=forms.HiddenInput())

	def __init__(self, clean_team=None, request=None, *args, **kwargs):
		super(EditCleanTeamMainContact, self).__init__(*args, **kwargs)
		
		# Prepopulate the Clean Ambassador drop down
		ctm_queryset = CleanTeamMember.objects.filter(clean_team=clean_team)
		self.fields["clean_ambassadors"] = forms.ChoiceField(label="Clean Ambassadors", widget=None, choices=[(o.user.id, str(o.user.profile.get_full_name())) for o in ctm_queryset])

	def clean(self):
		cleaned_data = super(EditCleanTeamMainContact, self).clean()
		
		contact_phone = cleaned_data.get("contact_phone")

		if not contact_phone:
			raise forms.ValidationError("Please enter a contact phone number")

		return cleaned_data

class RequestJoinTeamsForm(forms.Form):
	team = forms.ModelChoiceField(required=True, queryset=CleanTeam.objects.all())

class JoinTeamCleanChampionForm(forms.Form):
	team = forms.ModelChoiceField(required=True, queryset=CleanTeam.objects.all())

CREATE_OR_JOIN_CHOICES = (
	('create-new-team', 'Create a new team'), 
	('join-existing-team', 'Join an existing team'),
)

ROLE_CHOICES = (('ambassador', 'Ambassador',), ('manager', 'Manager',))
class CreateTeamOrJoinForm(forms.Form):
	selections = forms.ChoiceField(widget=forms.RadioSelect, choices=CREATE_OR_JOIN_CHOICES)
	role = forms.ChoiceField(widget=forms.RadioSelect, choices=ROLE_CHOICES, label="Role")
	invite = forms.CharField(required=False, widget=forms.HiddenInput())

RESPONSE_CHOICES = (
	('accepted', 'Accept'), 
	('declined', 'Decline'),
)
class InviteResponseForm(forms.Form):
	selections = forms.ChoiceField(widget=forms.RadioSelect, choices=RESPONSE_CHOICES)
	token = forms.CharField(required=True, widget=forms.HiddenInput())

ROLE_CHOICES = (
	('catalyst', 'Catalyst'),
	('ambassador', 'Ambassador'), 
)

class InviteForm(forms.Form):
	email = forms.CharField(required=True, widget=forms.Textarea)
	role = forms.ChoiceField(widget=forms.Select(), choices=ROLE_CHOICES)
	terms = forms.BooleanField(required=True)
	clean_team_id = forms.CharField(required=False, widget=forms.HiddenInput())

	# Combines the form with the corresponding model
	class Meta:
		model = CleanTeamInvite
		exclude = ('clean_team', 'user', 'role', 'status')

	def clean(self):
		cleaned_data = super(InviteForm, self).clean()
		email = cleaned_data.get('email')
		role = cleaned_data.get('role')
		terms = cleaned_data.get('terms')
		clean_team_id = cleaned_data.get('clean_team_id')

		if not email:
			raise forms.ValidationError("Please enter an email")
		if not terms:
			raise forms.ValidationError("Please accept the terms")

		emails = re.split(',', email)

		for invite_email in emails:
			invite_email = invite_email.strip()

			try:
				u = User.objects.get(email=invite_email)

				if role == 'ambassador':
					if u.profile.is_clean_ambassador() or u.profile.is_clean_ambassador("pending"):
						raise forms.ValidationError("%s is already a Clean Ambassador for %s" % (invite_email, u.profile.clean_team_member.clean_team.name))

				if role == 'catalyst':
					if u.profile.is_clean_champion(clean_team_id):
						raise forms.ValidationError("%s is already a Clean Clean Champion for your team" % (invite_email))	
			except User.DoesNotExist, e:
				print e

			error = CleanTeamInvite.objects.filter(email=invite_email, role=role, clean_team_id=clean_team_id).count()

			if error > 0:
				raise forms.ValidationError("%s is already invited for that role" %(invite_email))

		return cleaned_data

class PostMessageForm(forms.Form):
	message = forms.CharField(required=False, widget=forms.Textarea())

	# Combines the form with the corresponding model
	class Meta:
		model = CleanTeam
		exclude = ('clean_creds')

	def clean(self):
		cleaned_data = super(PostMessageForm, self).clean()
		message = cleaned_data.get('message')

		if not message:
			raise forms.ValidationError("Please enter a message")

		return cleaned_data

class LeaderReferralForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.TextInput())

	class Meta:
		model = LeaderReferral
		exclude = ('clean_team', 'user', 'timestamp')

	def clean(self):
		cleaned_data = super(LeaderReferralForm, self).clean()
		first_name = cleaned_data.get('first_name')
		last_name = cleaned_data.get('last_name')
		email = cleaned_data.get('email')
		organization = cleaned_data.get('organization')
		title = cleaned_data.get('title')

		if not first_name:
			raise forms.ValidationError("Please enter a first name")
		if not last_name:
			raise forms.ValidationError("Please enter a last name")
		if not email:
			raise forms.ValidationError("Please enter a valid email")
		if not organization:
			raise forms.ValidationError("Please enter a organization")
		if not title:
			raise forms.ValidationError("Please enter a title")

		return cleaned_data

class CleanTeamPresentationForm(forms.ModelForm):
	presentation = forms.FileField()

	class Meta:
		model = CleanTeamPresentation
		exclude = ('clean_team', 'user', 'timestamp')

	def clean(self):
		cleaned_data = super(CleanTeamPresentationForm, self).clean()
		title = cleaned_data.get('title')
		presentation = cleaned_data.get('presentation')
		
		if not title:
			raise forms.ValidationError("Please enter a title")
		if not presentation:
			raise forms.ValidationError("Please provide a presentation")

		return cleaned_data