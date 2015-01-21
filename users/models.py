from django.db import models
from django.contrib.auth.models import User

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
Name:           CleanTeamLevel
Date created:   Jan 30, 2014
Description:    All of the levels each Change Team can go through
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
Name:           CleanTeamLevelTask
Date created:   Jan 30, 2014
Description:    All of the tasks required to be completed in a level
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
Name:           CleanTeamLevelProgress
Date created:   Jan 30, 2014
Description:    The tasks each Change Team has completed per level
"""
class ProfileProgress(models.Model):
    user = models.ForeignKey(User)
    profile_task = models.ForeignKey(ProfileTask)
    approval_requested = models.BooleanField(default=0)
    completed = models.BooleanField(default=0)

    class Meta:
        verbose_name_plural = u'Profile Progress'

    def __unicode__(self):
        return u'%s - %s' % (self.clean_team, self.level_task)

    def submit_for_approval(self):
        self.approval_requested = True
        self.completed = False
        self.save()

    def save(self, *args, **kwargs):
        super(ProfileProgress, self).save(*args, **kwargs)