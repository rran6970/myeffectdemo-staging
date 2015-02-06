from django.db import models
from datetime import date
from django.contrib.auth.models import User
import string
import random

"""
Name:           PrelaunchEmails
Date created:   Sept 9, 2013
Description:    Used to keep track of all of the prelaunch emails
"""
class PrelaunchEmails(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length = 70, blank=False)
    postal_code = models.CharField(max_length = 7, blank=False)
    school_type = models.CharField(max_length = 30, blank=False, default="High School")
    ambassador = models.BooleanField()
    join = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = u'Prelaunch emails'

    def __unicode__(self):
        return u'Prelaunch : %s' % self.user.username

    def save(self, *args, **kwargs):
        super(PrelaunchEmails, self).save(*args, **kwargs)

"""
Name:           ProfilePhase
"""
class ProfilePhase(models.Model):
    name = models.CharField(max_length=30, null=False, default="One")
    drop_level = models.CharField(max_length=100, null=False, default="images/clean-team-tree-stage-1.png")
    next_level = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        verbose_name_plural = u'Profile Phase'

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        super(ProfilePhase, self).save(*args, **kwargs)

"""
Name:           ProfileTask
"""
class ProfileTask(models.Model):
    profile_phase = models.ForeignKey(ProfilePhase)
    name = models.CharField(max_length=60, blank=False, unique=True, default="", verbose_name='Task Name')
    description = models.TextField(blank=True, null=True, default="")
    link = models.URLField(blank=True, null=True)
    approval_required = models.BooleanField(default=0)

    class Meta:
        verbose_name_plural = u'Profile Task'

    def __unicode__(self):
        return u'%s: %s' % (self.name, self.description)

    def save(self, *args, **kwargs):
        super(ProfileTask, self).save(*args, **kwargs)

"""
Name:           ProfileProgress
"""
class ProfileProgress(models.Model):
    user = models.ForeignKey(User)
    phase = models.ForeignKey(ProfilePhase)
    profile_task = models.ForeignKey(ProfileTask)
    approval_requested = models.BooleanField(default=0)
    completed = models.BooleanField(default=0)

    class Meta:
        verbose_name_plural = u'Profile Progress'

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.profile_task)

    def submit_for_approval(self):
        self.approval_requested = True
        self.completed = False
        self.save()

    def save(self, *args, **kwargs):
        super(ProfileProgress, self).save(*args, **kwargs)

"""
Name:           OrganizationLicense
Date created:   Sept 9, 2013
Description:    Used to keep track of all of the prelaunch emails
"""
class OrganizationLicense(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True, unique=True)
    user = models.OneToOneField(User,blank=True, null=True)
    is_charity = models.BooleanField(null=False, default=False, verbose_name='Is Nonprofit/Charity')
    from_date = models.DateField(null=False)
    to_date = models.DateField(null=False)

    class Meta:
        verbose_name_plural = u'Organization License'

    def __unicode__(self):
        return u'License : %s' % self.code

    def new_charity_license(self, user):
        self.code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        self.user = user
        self.is_charity = True
        self.from_date = date.today()
        to_date = date.today()
        try:
            to_date = to_date.replace(year = to_date.year + 1)
        except ValueError:
            to_date = to_date + (date(to_date.year + 1, 1, 1) - date(to_date.year, 1, 1))
        self.to_date = to_date
        self.save()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        super(OrganizationLicense, self).save(*args, **kwargs)
