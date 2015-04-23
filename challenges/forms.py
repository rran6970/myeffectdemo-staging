import datetime
import re

from django.core.validators import RegexValidator
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms.extras.widgets import SelectDateWidget
from parsley.decorators import parsleyfy
from challenges.models import *

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

WEEKDAYS = (('-1', '------Select------'),
    ('0', 'Monday'),
    ('1', 'Tuesday'),
    ('2', 'Wednesday'),
    ('3', 'Thursday'),
    ('4', 'Friday'),
    ('5', 'Saturday'),
    ('6', 'Sunday'),
)

EVENTTYPES = (('ongoing', 'Ongoing Event'),
    ('onetime', 'One Time Event'),
    ('weekly', 'Weekly Event'),
)

class UserVoucherForm(forms.Form):
    voucher = forms.CharField(required=True, max_length=60, min_length=2, label="Voucher Code", widget=forms.TextInput())
    user_id = forms.CharField(required=True, max_length=60, widget=forms.HiddenInput())

    class Meta:
        model = UserVoucher
        exclude = ('user')

    def clean(self):
        cleaned_data = super(UserVoucherForm, self).clean()
        voucher_code = cleaned_data.get("voucher")
        user_id = cleaned_data.get("user_id")

        voucher = None

        try:
            voucher = Voucher.objects.get(voucher=voucher_code)
        except Exception, e:
            raise forms.ValidationError(u"Invalid voucher code")

        user = User.objects.get(id=user_id)

        if voucher.has_already_claimed(user):
            raise forms.ValidationError(u"Sorry but you've already claimed that voucher code")

        if voucher.claims_made >= voucher.claims_allowed:
            raise forms.ValidationError(u"Voucher code has already been claimed the maximum number of times")

        return cleaned_data

class NewChallengeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(NewChallengeForm, self).__init__(*args, **kwargs)
        skilltags = SkillTag.objects.all()
        tag_list = []
        for tag in skilltags:
            tag_list.append((tag.id, tag.skill_name))
        skilltags_choices = tuple(tag_list)

        self.fields['title'] = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
        self.fields['event_start_date'] = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'datepicker', 'autocomplete':'off'}), label="Program Start Date")
        self.fields['event_start_time'] = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'timepicker', 'autocomplete':'off'}), label="Program End Date")
        self.fields['event_end_date'] = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'datepicker', 'autocomplete':'off'}))
        self.fields['event_end_time'] = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'timepicker', 'autocomplete':'off'}))
        self.fields['event_type'] = forms.ChoiceField(required=False, widget=forms.Select(), choices=EVENTTYPES, label="Event Type")
        self.fields['day_of_week'] = forms.ChoiceField(required=False, widget=forms.Select(), choices=WEEKDAYS)
        self.fields['address1'] = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(), label="Address")
        self.fields['address2'] = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(), label="Suite (optional)")
        self.fields['city'] = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
        self.fields['province'] = forms.ChoiceField(required=False, widget=forms.Select(), choices=PROVINCES)
        #self.fields['postal_code'] = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
        self.fields['country'] = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
        self.fields['description'] = forms.CharField(required=False, min_length = 2, widget=forms.Textarea())
        self.fields['tags'] = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple(), choices=skilltags_choices, label="Skill Tags")
        self.fields['link'] = forms.CharField(required=False, min_length=2, label="External link")
        self.fields['limit'] = forms.IntegerField(required=False, label="Maximum Participants")

        self.fields['host_is_clean_team'] = forms.BooleanField(required=False)
        self.fields['organization'] = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput(), label="Host Organization")
        self.fields['contact_first_name'] = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput(), label="First name")
        self.fields['contact_last_name'] = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput(), label="Last name")
        self.fields['contact_phone'] = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput(attrs={'class': 'phone-number'}), label="Phone number", validators=[RegexValidator(regex='[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,4}', message='Contact Phone Number format incorrect', code='invalid_phone')])
        self.fields['contact_email'] = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput(), label="Email address")

        self.fields['national_challenge'] = forms.BooleanField(label="This is a National Action", required=False)
        self.fields['virtual_challenge'] = forms.BooleanField(label="This is a Virtual  Action", required=False)
        self.fields['clean_team_only'] = forms.BooleanField(label="This is only for Change Teams", required=False)
        self.fields['is_private'] = forms.BooleanField(label="This is a private challenge", required=False)
        self.fields['type'] = forms.ModelChoiceField(required=False, queryset=ChallengeType.objects.all(), label="Change Creds Rate")
        self.fields['challenge_id'] = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(NewChallengeForm, self).clean()
        title = cleaned_data.get("title")
        event_start_date = cleaned_data.get("event_start_date")
        event_start_time = cleaned_data.get("event_start_time")
        event_end_date = cleaned_data.get("event_end_date")
        event_end_time = cleaned_data.get("event_end_time")
        event_type = cleaned_data.get("event_type")
        day_of_week = cleaned_data.get("day_of_week")
        address1 = cleaned_data.get("address1")
        address2 = cleaned_data.get("address2")
        city = cleaned_data.get("city")
        province = cleaned_data.get("province")
        country = cleaned_data.get("country")
        #postal_code = cleaned_data.get("postal_code")
        tags = cleaned_data.get("tags")
        description = cleaned_data.get("description")
        link = cleaned_data.get("link")
        organization = cleaned_data.get("organization")
        contact_first_name = cleaned_data.get("contact_first_name")
        contact_last_name = cleaned_data.get("contact_last_name")
        contact_phone = cleaned_data.get("contact_phone")
        contact_email = cleaned_data.get("contact_email")
        national_challenge = cleaned_data.get("national_challenge")
        virtual_challenge = cleaned_data.get("virtual_challenge")
        clean_team_only = cleaned_data.get("clean_team_only")
        is_private = cleaned_data.get("is_private")
        type = cleaned_data.get("type")
        challenge_id = cleaned_data.get("challenge_id")

        if not organization:
            raise forms.ValidationError("Please enter a host organization")
        elif not contact_first_name:
            raise forms.ValidationError("Please enter a contact first name")
        elif not contact_last_name:
            raise forms.ValidationError("Please enter a contact last name")
        elif not contact_phone:
            raise forms.ValidationError("Please enter a contact phone number")
        elif not contact_email:
            raise forms.ValidationError("Please enter a contact email")
        elif not title:
            raise forms.ValidationError("Please enter a title")
        elif not event_start_date:
            raise forms.ValidationError("Please enter a starting event date")
        elif not event_start_time:
            raise forms.ValidationError("Please enter a starting event time")
        elif not event_end_date:
            raise forms.ValidationError("Please enter an ending event date")
        elif not event_end_time:
            raise forms.ValidationError("Please enter an ending event time")
        elif not description:
            raise forms.ValidationError("Please enter a description")
        elif not national_challenge and not virtual_challenge:
            if not country:
                raise forms.ValidationError("Please enter a country")
            elif not address1:
                raise forms.ValidationError("Please enter an address")
            elif not city:
                raise forms.ValidationError("Please enter a city")
            elif not province:
                raise forms.ValidationError("Please select a province")
            #elif not postal_code:
                #raise forms.ValidationError("Please enter a postal code")

        return cleaned_data

CATEGORIES = (('', '-------Select-------'),
        ('General', 'General'),
        ('Animals_Wildlife', 'Animals & Wildlife'),
        ('Arts_Culture', 'Arts & Culture'),
        ('Business_Entrepreneurship', 'Business & Entrepreneurship'),
        ('Children_Youth', 'Children & Youth'),
        ('Education_Research', 'Education & Research'),
        ('Environment', 'Environment'),
        ('Health_Wellness', 'Health & Wellness'),
        ('HumanRights_Advocacy', 'Human Rights & Advocacy'),
        ('InternationalRelief_Development', 'International Relief & Development'),
        ('SocialServices_Community', 'Social Services & Community'),
        ('Sports_Recreation', 'Sports & Recreation'),
    )

@parsleyfy
class NewActionSurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewActionSurveyForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'main-question', 'data-parsley-group':'1'}), required=True, choices=CATEGORIES)

        questions = ChallengeQuestion.objects.all().order_by('question_number')
        questions_order = 3

        for question in questions:
            required = question.required
            if required:
                questions_order = questions_order + 1
                #label = "%s. %s" %(questions_order, question.question)
                label = question.question
                inputclass = "main-question"
            else:
                label = question.question
                inputclass = "sub-question"
            answers = QuestionAnswer.objects.filter(question=question).order_by('answer_number')
            answer_list = []

            for answer in answers:
                answer_list.append((answer.id, answer.answer))

            answer_tuple = tuple(answer_list)

            if question.answer_type.name == "single":
                self.fields['question_%s' % question.question_number] = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':inputclass,'data-parsley-group':questions_order}), required=required, label=label, choices=answer_tuple)
            elif question.answer_type.name == "multiple":
                self.fields['question_%s' % question.question_number] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class':inputclass,'data-parsley-group':questions_order}), required=required, label=label, choices=answer_tuple)
            elif question.answer_type.name == "number":
                self.fields['question_num_%s' % question.question_number] = forms.IntegerField(widget=forms.TextInput(attrs={'class':inputclass,'data-parsley-group':questions_order }), required=required, label=label)
            elif question.answer_type.name == "text":
                self.fields['question_txt_%s' % question.question_number] = forms.CharField(widget=forms.TextInput(attrs={'class':inputclass,'data-parsley-group':questions_order }), required=required, label=label)

    def clean(self):
        cleaned_data = super(NewActionSurveyForm, self).clean()
        return cleaned_data

class EditChallengeForm(forms.ModelForm):
    title = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
    event_start_date = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'datepicker', 'autocomplete':'off'}))
    event_start_time = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'timepicker', 'autocomplete':'off'}))
    event_end_date = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'datepicker', 'autocomplete':'off'}))
    event_end_time = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'timepicker', 'autocomplete':'off'}))
    address1 = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
    address2 = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
    city = forms.CharField(required=True, max_length = 128, min_length = 2, widget=forms.TextInput())
    province = forms.ChoiceField(widget=forms.Select(), choices=PROVINCES)
    postal_code = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
    country = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput())
    description = forms.CharField(required=False, min_length = 2, widget=forms.Textarea())
    link = forms.URLField(required=False, min_length=2, label="External link")

    host_is_clean_team = forms.BooleanField(required=False)
    organization = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(), label="Host Organization")
    contact_first_name = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(), label="First name")
    contact_last_name = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(), label="Last name")
    contact_phone = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(attrs={'class':'phone-number'}), label="Phone number")
    contact_email = forms.CharField(required=False, max_length = 128, min_length = 2, widget=forms.TextInput(), label="Email address")

    national_challenge = forms.BooleanField(label="This is a National Challenge", required=False)
    type = forms.ModelChoiceField(required=False, queryset=ChallengeType.objects.all())
    challenge_id = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Challenge
        exclude = ('user', 'clean_team', 'clean_creds_per_hour', 'last_updated_by', 'qr_code', 'token')

    def clean(self):
        cleaned_data = super(EditChallengeForm, self).clean()
        title = cleaned_data.get("title")
        event_start_date = cleaned_data.get("event_start_date")
        event_start_time = cleaned_data.get("event_start_time")
        event_end_date = cleaned_data.get("event_end_date")
        event_end_time = cleaned_data.get("event_end_time")
        address1 = cleaned_data.get("address1")
        address2 = cleaned_data.get("address2")
        city = cleaned_data.get("city")
        province = cleaned_data.get("province")
        country = cleaned_data.get("country")
        postal_code = cleaned_data.get("postal_code")
        description = cleaned_data.get("description")
        link = cleaned_data.get("link")

        organization = cleaned_data.get("organization")
        contact_first_name = cleaned_data.get("contact_first_name")
        contact_last_name = cleaned_data.get("contact_last_name")
        contact_phone = cleaned_data.get("contact_phone")
        contact_email = cleaned_data.get("contact_email")

        national_challenge = cleaned_data.get("national_challenge")
        challenge_id = cleaned_data.get("challenge_id")

        if not organization:
            raise forms.ValidationError("Please enter a host organization")
        elif not contact_first_name:
            raise forms.ValidationError("Please enter a contact first name")
        elif not contact_last_name:
            raise forms.ValidationError("Please enter a contact last name")
        elif not contact_phone:
            raise forms.ValidationError("Please enter a contact phone number")
        elif not contact_email:
            raise forms.ValidationError("Please enter a contact email")
        elif not title:
            raise forms.ValidationError("Please enter a title")
        elif not event_start_date:
            raise forms.ValidationError("Please enter a starting event date")
        elif not event_start_time:
            raise forms.ValidationError("Please enter a starting event time")
        elif not event_end_date:
            raise forms.ValidationError("Please enter an ending event date")
        elif not event_end_time:
            raise forms.ValidationError("Please enter an ending event time")
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

class ChallengeUploadFileForm(forms.ModelForm):
    challenge_id = forms.CharField(required=True, widget=forms.HiddenInput())
    upload_file = forms.FileField(required=False)

    class Meta:
        model = ChallengeUploadFile
        exclude = ('challenge', 'file_name')

    def clean(self):
        cleaned_data = super(ChallengeUploadFileForm, self).clean()
        challenge_id = cleaned_data.get("challenge_id")
        upload_file = cleaned_data.get("upload_file")
        if not challenge_id:
            raise forms.ValidationError("Please enter a id")
        if not upload_file:
            raise forms.ValidationError("Please select a file to upload")
        # MAX_UPLOAD_SIZE 5MB - 5242880
        if upload_file._size > 5242880:
            raise forms.ValidationError('Please keep filesize under 5MB.')

        return cleaned_data

class ParticipantEmailForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=200, widget=forms.TextInput())
    message = forms.CharField(label='Message', widget=forms.Textarea())

    def clean(self):
        cleaned_data = super(ParticipantEmailForm, self).clean()
        subject = cleaned_data.get("subject")
        message = cleaned_data.get("message")

        if not subject:
            raise forms.ValidationError("Please enter a valid Subject")
        elif not message:
            raise forms.ValidationError("Please enter the message")

        return cleaned_data
