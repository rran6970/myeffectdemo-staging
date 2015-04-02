import re
from django import forms
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from cleanteams.models import CleanTeam, CleanTeamMember, CleanTeamInvite, LeaderReferral, CleanTeamPresentation, OrgProfile, Community
from users.models import OrganizationLicense

CREATE_TEAM_CHOICES = (('change_team', 'Create A Change Team'),
    ('representing', 'Representing An Organization'),
)

ORG_TYPES = (('school', 'School'),
    ('nonprofit_charity', 'Nonprofit/Charity'),
    ('business', 'Business'),
    ('municipality', 'Municipality'),
)

ORG_CATEGORIES = (('General', 'General'),
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

class RegisterCleanTeamForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
    website = forms.URLField(required=False, initial="", max_length=128, min_length=2, widget=forms.TextInput())
    logo = forms.ImageField(required=False)
    about = forms.CharField(required=False, widget=forms.Textarea())
    twitter = forms.CharField(required=False, initial="@", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'@'}))
    facebook = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput())
    instagram = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput())
    region = forms.CharField(required=True, max_length=128, min_length=3, widget=forms.TextInput())
    group = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput())
    clean_team_id = forms.CharField(required=False, widget=forms.HiddenInput())
    role = forms.CharField(required=False, widget=forms.HiddenInput())
    contact_first_name = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput(attrs={'readonly':'readonly'}), label="First name")
    contact_last_name = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput(attrs={'readonly':'readonly'}), label="Last name")
    contact_phone = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput(attrs={'class':'phone-number'}), label="Phone number")
    contact_email = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput(attrs={'readonly':'readonly'}), label="Email address")
    number_of_users = forms.IntegerField(required=False)
    org_type = forms.ChoiceField(widget=forms.Select(), choices=ORG_TYPES)
    registered_number = forms.CharField(required=False, widget=forms.TextInput(), max_length=30 )
    category = forms.ChoiceField(widget=forms.Select(), choices=ORG_CATEGORIES)

    # Combines the form with the corresponding model
    class Meta:
        model = CleanTeam
        exclude = ('clean_creds', 'level', 'contact_user')

    def clean(self):
        cleaned_data = super(RegisterCleanTeamForm, self).clean()
        name = cleaned_data.get('name')
        # website = cleaned_data.get('website')
        logo = cleaned_data.get('logo')
        # about = cleaned_data.get('about')
        # twitter = cleaned_data.get('twitter')
        # facebook = cleaned_data.get('twitter')
        # instagram = cleaned_data.get('instagram')
        region = cleaned_data.get('region')
        group = cleaned_data.get('group')
        # contact_phone = cleaned_data.get('contact_phone')
        #clean_team_id = cleaned_data.get('clean_team_id')

        # contact_first_name = cleaned_data.get("contact_first_name")
        # contact_last_name = cleaned_data.get("contact_last_name")
        contact_phone = cleaned_data.get("contact_phone")
        # contact_email = cleaned_data.get("contact_email")

        if not name:
            raise forms.ValidationError("Please enter your Change Team's name")
        elif not region:
            raise forms.ValidationError("Please enter your region")
        elif not group:
            raise forms.ValidationError("Please the group your team associated with")
        elif not contact_phone:
            raise forms.ValidationError("Please enter a contact phone number")

        if logo:
            if logo._size > 2*1024*1024:
                raise forms.ValidationError("Image file must be smaller than 2MB")

            w, h = get_image_dimensions(logo)

            # if w != 124:
            #    raise forms.ValidationError("The image is supposed to be 124px X 124px")
            # if h != 124:
            #    raise forms.ValidationError("The image is supposed to be 124px X 124px")

        if CleanTeam.objects.filter(name=name):
            raise forms.ValidationError(u'%s already exists' % name)
        return cleaned_data

class RegisterCommunityForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(), max_length=120 )
    is_private = forms.BooleanField(required=False)
    website = forms.URLField(required=False, initial="", max_length=128, min_length=2, widget=forms.TextInput())
    logo = forms.ImageField(required=False)
    about = forms.CharField(required=False, widget=forms.Textarea())
    twitter = forms.CharField(required=False, initial="@", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'@'}))
    facebook = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput())
    instagram = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput())
    contact_phone = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput(attrs={'class':'phone-number'}), label="Phone number")
    region = forms.CharField(required=True, max_length=128, min_length=3, widget=forms.TextInput())
    category = forms.ChoiceField(widget=forms.Select(), choices=ORG_CATEGORIES)

    class Meta:
        model = Community
        exclude = ('owner_user', 'contact_user', 'clean_creds')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RegisterCommunityForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegisterCommunityForm, self).clean()
        name = cleaned_data.get('name')

        if Community.objects.filter(name=name):
            raise forms.ValidationError(u'There is already a community named \'%s\'.' % name)

        try:
            existing_community = Community.objects.get(owner_user=self.request.user)
        except:
            existing_community = None

        if existing_community:
            raise forms.ValidationError(u'You are already the owner of an existing community called \'%s\'.' % existing_community.name)

        return cleaned_data

class RegisterOrganizationForm(forms.ModelForm):
    create_team = forms.ChoiceField(widget=forms.RadioSelect, choices=CREATE_TEAM_CHOICES)
    org_type = forms.ChoiceField(widget=forms.Select(), choices=ORG_TYPES)
    registered_number = forms.CharField(required=False, widget=forms.TextInput(), max_length=30 )
    category = forms.ChoiceField(widget=forms.Select(), choices=ORG_CATEGORIES)
    number_of_users = forms.IntegerField(required=False)
    access_code = forms.CharField(required=False, widget=forms.TextInput(), max_length=30 )
    current_user = forms.CharField(required=False, widget=forms.HiddenInput(), max_length=50 )
    org_license = forms.CharField(required=False, widget=forms.HiddenInput(), max_length=10 )

    class Meta:
        model = OrgProfile
        exclude = ('user')

    def clean(self):
        cleaned_data = super(RegisterOrganizationForm, self).clean()
        create_team = cleaned_data.get('create_team')
        org_type = cleaned_data.get('org_type')
        registered_number = cleaned_data.get('registered_number')
        category = cleaned_data.get("category")
        number_of_users = cleaned_data.get("number_of_users")
        access_code = cleaned_data.get("access_code")
        current_user = cleaned_data.get("current_user")
        org_license = cleaned_data.get("org_license")
        if not create_team:
            raise forms.ValidationError("Please Select a Change Team Type")

        if create_team == 'representing':
            if org_type == 'nonprofit_charity':
                if not registered_number:
                    raise forms.ValidationError("Please enter your Registered Number")
            else:
                if not number_of_users:
                    raise forms.ValidationError("Please enter Expected Number Of Users")
                if number_of_users < 1:
                    raise forms.ValidationError("Please enter a valid Expected Number Of Users")
                if not org_license:
                    if not access_code:
                        raise forms.ValidationError("Please enter a valid Access Code")
                    if not OrganizationLicense.objects.filter(code=access_code).exists():
                        raise forms.ValidationError("Please enter a valid Access Code")
                    else:
                        ol = OrganizationLicense.objects.filter(code=access_code)[0]
                        if ol.user and ol.user.id != current_user:
                            raise forms.ValidationError("Please enter a valid Access Code3")
        return cleaned_data

class EditCleanTeamForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
    website = forms.URLField(required=False, initial="", max_length=128, min_length=2, widget=forms.TextInput())
    logo = forms.ImageField(required=False)
    about = forms.CharField(required=False, widget=forms.Textarea())
    twitter = forms.CharField(required=False, initial="@", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'@'}))
    facebook = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput())
    instagram = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput())
    region = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
    group = forms.CharField(required=False, max_length=128, min_length=2, widget=forms.TextInput())
    clean_team_id = forms.CharField(required=False, widget=forms.HiddenInput())
    community = forms.CharField(required=False, max_length=128, min_length=1, widget=forms.TextInput())

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
        facebook = cleaned_data.get('facebook')
        instagram = cleaned_data.get('instagram')
        region = cleaned_data.get('region')
        group = cleaned_data.get('group')
        clean_team_id = cleaned_data.get('clean_team_id')
        community = cleaned_data.get('community')
        if community == "":
            community = None

        if (not community is None) and (not Community.objects.filter(name=community)):
            raise forms.ValidationError("That community does not exist")

        if not name:
            raise forms.ValidationError("Please enter your Change Team's name")
        elif not region:
            raise forms.ValidationError("Please enter your region")

        if logo:
            if logo._size > 2*1024*1024:
                raise forms.ValidationError("Image file must be smaller than 2MB")

        if CleanTeam.objects.filter(name=name) and not clean_team_id:
            raise forms.ValidationError(u'%s already exists' % name)

        return cleaned_data

class EditCommunityForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=128, min_length=2, widget=forms.TextInput())
    website = forms.URLField(required=False, initial="", max_length=128, min_length=2, widget=forms.TextInput())
    logo = forms.ImageField(required=False)
    about = forms.CharField(required=False, widget=forms.Textarea())
    twitter = forms.CharField(required=False, initial="@", max_length = 128, min_length=1, widget=forms.TextInput(attrs={'placeholder':'@'}))
    facebook = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput())
    instagram = forms.CharField(required=False, initial="", max_length = 128, min_length=1, widget=forms.TextInput())
    community_id = forms.CharField(required=False, widget=forms.HiddenInput())
    region = forms.CharField(required=True, max_length=128, min_length=3, widget=forms.TextInput())
    category = forms.ChoiceField(widget=forms.Select(), choices=ORG_CATEGORIES)

    # Combines the form with the corresponding model
    class Meta:
        model = Community
        exclude = ('clean_creds', 'level', 'contact_user', 'contact_phone', 'is_private', 'owner_user')

    def clean(self):
        cleaned_data = super(EditCommunityForm, self).clean()
        name = cleaned_data.get('name')
        website = cleaned_data.get('website')
        logo = cleaned_data.get('logo')
        about = cleaned_data.get('about')
        twitter = cleaned_data.get('twitter')
        facebook = cleaned_data.get('facebook')
        instagram = cleaned_data.get('instagram')
        community_id = cleaned_data.get('community_id')

        if not name:
            raise forms.ValidationError("Please enter your Community's name")

        if logo:
            if logo._size > 2*1024*1024:
                raise forms.ValidationError("Image file must be smaller than 2MB")

        #  If there is an existing community with this name, and we are changing the community name, then error
        if Community.objects.filter(name=name).count() and Community.objects.filter(name=name, id=community_id).count() == 0:
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

ROLE_CHOICES = (('leader', 'Leader',), ('manager', 'Manager',))
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
    ('agent', 'Friend(Agent)'),
    ('leader', 'Leader'),
    ('organization', 'Organization')
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
            if clean_team_id:
                try:
                    u = User.objects.get(email=invite_email)

                    if role == 'leader':
                        if u.profile.is_clean_ambassador() or u.profile.is_clean_ambassador("pending"):
                            raise forms.ValidationError("%s is already a Clean Ambassador for %s" % (invite_email, u.profile.clean_team_member.clean_team.name))

                    if role == 'agent':
                        if u.profile.is_clean_champion(clean_team_id):
                            raise forms.ValidationError("%s is already a Clean Clean Champion for your team" % (invite_email))
                except User.DoesNotExist, e:
                    print e

                error = CleanTeamInvite.objects.filter(email=invite_email, role=role, clean_team_id=clean_team_id).count()

                if error > 0:
                    raise forms.ValidationError("%s is already invited for that role" %(invite_email))
            else:
                if CleanTeamInvite.objects.filter(email=invite_email):
                    raise forms.ValidationError("%s is already invited" %(invite_email))
                try:
                    u = User.objects.get(email=invite_email)
                    if u:
                        raise forms.ValidationError("%s is already invited" %(invite_email))
                except User.DoesNotExist, e:
                    print e
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
        exclude = ('clean_team', 'user', 'timestamp', 'status', 'token')

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
        if LeaderReferral.objects.filter(email=email):
            raise forms.ValidationError("This email is already referred")

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
