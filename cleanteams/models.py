import random
import string
import json

from django.contrib.auth.models import User
from django.db import models
from itertools import chain
from mycleancity.actions import *
from notifications.models import Notification, UserNotification


"""
Name:           Community
Date created:   March 10, 2015
Description:    A table that stores community objects (of which users and teams can belong to)
"""
class Community(models.Model):
    name = models.CharField(max_length=120, null=False, unique=True, default="", verbose_name='Name of Community')
    is_private = models.BooleanField(default=0, null=False)

    class Meta:
        verbose_name_plural = u'Community object'

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        super(Community, self).save(*args, **kwargs)

"""
Name:           OrgProfile
Date created:   Jan 29, 2014
Description:    profile for clean teams that Representing a organization
"""
class OrgProfile(models.Model):
    org_type = models.CharField(max_length=30, null=False, default="other")
    registered_number = models.CharField(max_length=30, blank=True, null=True )
    category = models.CharField(max_length=60, blank=False, null=False, verbose_name="Team Category", default="General")
    number_of_users = models.IntegerField(blank=True, null=True)
    user = models.OneToOneField(User, null=True)

    class Meta:
        verbose_name_plural = u'Organization Profile'

    def __unicode__(self):
        return u'%s' % self.org_type

    def save(self, *args, **kwargs):
        super(OrgProfile, self).save(*args, **kwargs)

"""
Name:           CleanTeamLevel
Date created:   Jan 30, 2014
Description:    All of the levels each Change Team can go through
"""
class CleanTeamLevel(models.Model):
    name = models.CharField(max_length=30, null=False, default="Seedling")
    badge = models.CharField(max_length=100, null=False, default="images/badge-level-1-75x63.png")
    tree_level = models.CharField(max_length=100, null=False, default="images/clean-team-tree-stage-1.png")
    next_level = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        verbose_name_plural = u'Change Team Level'

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        super(CleanTeamLevel, self).save(*args, **kwargs)

"""
Name:           CleanTeam
Date created:   Nov 25, 2013
Description:    Users can be part of Change Teams
"""
class CleanTeam(models.Model):

    name = models.CharField(max_length=60, blank=True, verbose_name='Change Team Name')
    website = models.URLField(verbose_name = u'Website', blank=True, null=True, default="")
    logo = models.ImageField(upload_to=get_upload_file_name, blank=True, null=True, default="", verbose_name='Logo')
    about = models.TextField(blank=True, null=True, default="")
    twitter = models.CharField(max_length=60, blank=True, null=True, verbose_name="Twitter Handle")
    facebook = models.CharField(max_length=60, blank=True, null=True, verbose_name="Facebook")
    instagram = models.CharField(max_length=60, blank=True, null=True, verbose_name="Instagram Link")
    region = models.CharField(max_length=60, blank=True, null=True, verbose_name="Region")
    group = models.CharField(max_length=100, blank=True, null=True, verbose_name="Group Representing")
    clean_creds = models.IntegerField(default=0)
    level = models.ForeignKey(CleanTeamLevel, blank=True, null=True)
    admin = models.BooleanField(default=False)
    org_profile = models.OneToOneField(OrgProfile, blank=True, null=True)

    contact_user = models.ForeignKey(User)
    contact_phone = models.CharField(max_length=15, blank=False, verbose_name="Contact Phone Number")

    class Meta:
        verbose_name_plural = u'Change Team'

    def __unicode__(self):
        return u'Change Team: %s' % self.name

    def get_pixels_for_leading_teams(self, clean_creds):
        height = 0

        if clean_creds <= 250:
            difference = 75
            max = 250

            divisor = max/difference
            height = clean_creds/divisor
            height -= 30
        elif clean_creds <= 1000:
            difference = 67
            max = 1000

            divisor = max/difference

            height = clean_creds/divisor
            height += difference
            height -= 30
        elif clean_creds <= 3000:
            difference = 67
            max = 3000

            divisor = max/difference

            height = clean_creds/divisor
            height += (difference + 75)
            height -= 15
        elif clean_creds <= 5000:
            difference = 67
            max = 5000

            divisor = max/difference

            height = clean_creds/divisor
            height += (difference + 140)
            height -= 35
        elif clean_creds <= 10000:
            difference = 67
            max = 10000

            divisor = max/difference;

            height = clean_creds/divisor;
            height += (difference + 208);
            height -= 40
        elif clean_creds <= 15000:
            difference = 67
            max = 15000

            divisor = max/difference

            height = clean_creds/divisor
            height += (difference + 285)
            height -= 13
        elif clean_creds > 15000:
            height = 419
            height -= 5

        return height

    def get_leading_teams(self):
        clean_teams = CleanTeam.objects.filter(clean_creds__gt=self.clean_creds)[:3]
        clean_teams_list = []

        for clean_team in clean_teams:
            pixels = self.get_pixels_for_leading_teams(clean_team.clean_creds)
            clean_team_array = [clean_team, pixels]
            clean_teams_list.append(clean_team_array)

        return clean_teams_list

    def add_team_clean_creds(self, amount, notification=True):
        self.clean_creds += amount
        self.save()


        if notification:

            try:
                # Send notifications
                notification = Notification.objects.get(notification_type="clean_team_add_clean_creds")
                # The names that will go in the notification message template
                name_strings = [self.name, amount]
                link_strings = [str(self.id)]

                users_to_notify_str = notification.users_to_notify
                users_to_notify = users_to_notify_str.split(', ')

                # Notify all of the Users that have the roles within users_to_notify
                for role in users_to_notify:
                    clean_team_members = CleanTeamMember.objects.filter(role=role, clean_team=self, status="approved")

                    for member in clean_team_members:
                        user_notification = UserNotification()
                        user_notification.create_notification("clean_team_add_clean_creds", member.user, name_strings, link_strings)
            except Exception, e:
                print e

    # Checks if all of the tasks within the Change Teams level is complete.
    # If so, they are leveled up.
    def check_if_level_up(self):
        level_tasks = CleanTeamLevelTask.objects.filter(clean_team_level=self.level)
        tasks_complete = CleanTeamLevelProgress.objects.filter(clean_team=self, level_task__in=level_tasks, completed=True).count()
        # total_tasks = CleanTeamLevelTask.objects.filter(clean_team_level=self.level).count()
        return tasks_complete

    def level_up(self, notification=True):
        # If they don't have a badge, ie. new team, make them a Seedling
        if self.level is None:
            level = CleanTeamLevel.objects.get(name="Seedling")
        else:
            level = CleanTeamLevel.objects.get(name="Seedling")


        self.level = level

        # Add rewards for certain badges


        self.save()

        level_tasks = CleanTeamLevelTask.objects.filter(clean_team_level=self.level)

        # Create the new tasks the Change Team must complete
        for task in level_tasks:
            level_progress = CleanTeamLevelProgress(clean_team=self, level_task=task)
            level_progress.save()

        if notification:
            try:
                # Send notifications
                notification = Notification.objects.get(notification_type="level_up")
                # The names that will go in the notification message template
                name_strings = [self.name, self.level.name]
                link_strings = [str(self.id)]

                users_to_notify_str = notification.users_to_notify
                users_to_notify = users_to_notify_str.split(', ')

                # Notify all of the Users that have the roles within users_to_notify
                for role in users_to_notify:
                    clean_team_members = CleanTeamMember.objects.filter(role=role, clean_team=self, status="approved")

                    for member in clean_team_members:
                        user_notification = UserNotification()
                        user_notification.create_notification("level_up", member.user, name_strings, link_strings)
            except Exception, e:
                print e

    def complete_level_task(self, task):
        level_progress, created = CleanTeamLevelProgress.objects.get_or_create(clean_team=self, level_task=task)

        # Check if the task is already requesting an approval
        if level_progress.approval_requested:
            level_progress.approval_requested = False
            level_progress.completed = True
        elif task.approval_required:
            level_progress.submit_for_approval()
        else:
            level_progress.completed = True

        level_progress.save()

        self.check_if_level_up()

    def uncomplete_level_task(self, task):
        level_progress, created = CleanTeamLevelProgress.objects.get_or_create(clean_team=self, level_task=task)

        if level_progress.level_task.approval_required:
            level_progress.approval_requested = True
        else:
            level_progress.approval_requested = False

        level_progress.completed = False
        level_progress.save()

    def count_invites_sent(self, role=""):
        if role:
            return CleanTeamInvite.objects.filter(clean_team=self, role=role).count()
        else:
            return CleanTeamInvite.objects.filter(clean_team=self).count()

    def count_approved_members(self, role=""):
        if role == "leader":
            return CleanTeamMember.objects.filter(clean_team=self, role=role, status="approved").count()
        elif role == "agent":
            return CleanChampion.objects.filter(clean_team=self, status="approved").count()
        else:
            ca = CleanTeamMember.objects.filter(clean_team=self, role="leader", status="approved").count()
            cc = CleanChampion.objects.filter(clean_team=self, status="approved").count()

            return ca + cc

    def update_main_contact(self, form):
        try:
            clean_ambassador = form['clean_ambassadors']
            clean_ambassador_user = User.objects.get(id=clean_ambassador)

            self.contact_user = clean_ambassador_user
            self.contact_phone = form['contact_phone']
            self.save()
        except Exception, e:
            print e

    def save(self, *args, **kwargs):
        super(CleanTeam, self).save(*args, **kwargs)

"""
Name:           CleanChampion
Date created:   Dec 30, 2013
Description:    Users can be part of Change Teams as Clean Champions
"""
class CleanChampion(models.Model):

    user = models.ForeignKey(User)
    clean_team = models.ForeignKey(CleanTeam)
    status = models.CharField(max_length=30, default="approved")

    class Meta:
        verbose_name_plural = u'Clean Champions'

    def __unicode__(self):
        return u'%s is supporting %s' %(self.user.email, self.clean_team.name)

    def save(self, *args, **kwargs):
        super(CleanChampion, self).save(*args, **kwargs)

    def becomeCleanChampion(self, user, selected_team, notification=True):
        self.user = user
        self.clean_team = selected_team
        self.status = "approved"
        self.save()

        if notification:
            try:
                # Send notifications
                notification = Notification.objects.get(notification_type="cc_joined")
                # The names that will go in the notification message template
                full_name = u'%s %s' %(self.user.first_name, self.user.last_name)
                name_strings = [full_name, self.clean_team.name]

                users_to_notify_str = notification.users_to_notify
                users_to_notify = users_to_notify_str.split(', ')

                # Notify all of the Users that have the roles within users_to_notify
                for role in users_to_notify:
                    clean_team_members = CleanTeamMember.objects.filter(role=role, clean_team=self.clean_team, status="approved")

                    for member in clean_team_members:
                        user_notification = UserNotification()
                        user_notification.create_notification("cc_joined", member.user, name_strings)
            except Exception, e:
                print e

        if self.clean_team.level.name == "Sprout":
            # count_ccs = CleanChampion.objects.filter(clean_team=self.clean_team).count()
            self.clean_team.level.name == "Seedling"
            # if count_ccs > 2:
            # task = CleanTeamLevelTask.objects.get(name="3_ccs")
            # self.clean_team.complete_level_task(task)
        elif self.clean_team.level.name == "Sapling":
            self.clean_team.level.name == "Seedling"
            # count_ccs = CleanChampion.objects.filter(clean_team=self.clean_team).count()
            # if count_ccs > 9:
            # task = CleanTeamLevelTask.objects.get(name="10_ccs")
            #  self.clean_team.complete_level_task(task)
        elif self.clean_team.level.name == "Tree":
            self.clean_team.level.name == "Seedling"
            # count_ccs = CleanChampion.objects.filter(clean_team=self.clean_team).count()
            # if count_ccs > 19:
            #   task = CleanTeamLevelTask.objects.get(name="20_ccs")
            #   self.clean_team.complete_level_task(task)
        self.clean_team.add_team_clean_creds(5)
        self.user.profile.add_clean_creds(20)

    def becomeCleanChampionNew(self, user, userid, selected_team):
        self.user_id = userid
        self.clean_team_id = selected_team
        self.status = "approved"
        self.save()

        # Send notifications
        notification = Notification.objects.get(notification_type="cc_joined")
        # The names that will go in the notification message template
        full_name = u'%s %s' %(self.user.first_name, self.user.last_name)
        name_strings = [full_name, self.clean_team.name]

        users_to_notify_str = notification.users_to_notify
        users_to_notify = users_to_notify_str.split(', ')

        # Notify all of the Users that have the roles within users_to_notify
        for role in users_to_notify:
            # print self.clean_team_id
            clean_team_members = CleanTeamMember.objects.filter(role=role, clean_team=self.clean_team, status="approved")

            for member in clean_team_members:
                user_notification = UserNotification()
                user_notification.create_notification("cc_joined", member.user, name_strings)

        self.clean_team.add_team_clean_creds(5)
        self.user.profile.add_clean_creds(20)

"""
Name:           CleanTeamMember
Date created:   Nov 25, 2013
Description:    Users can be part of Change Teams
"""
class CleanTeamMember(models.Model):

    user = models.ForeignKey(User)
    clean_team = models.ForeignKey(CleanTeam)
    role = models.CharField(max_length=30, default="leader")
    status = models.CharField(max_length=30, default="pending")

    class Meta:
        verbose_name_plural = u'Change Team Member'

    def __unicode__(self):
        return u'%s is on %s' %(self.user.email, self.clean_team.name)

    def save(self, *args, **kwargs):
        super(CleanTeamMember, self).save(*args, **kwargs)

    # By pass the requestBecomeCleanAmbassador() and approveCleanAmbassador()
    def becomeCleanAmbassador(self, user, selected_team, notification=True):
        CleanChampion.objects.filter(user=user, clean_team=selected_team).delete()

        self.user = user
        self.clean_team = selected_team
        self.role = "leader"
        self.status = "approved"
        self.save()

        self.user.profile.clean_team_member = CleanTeamMember.objects.latest('id')
        self.user.profile.save()

        if notification:
            try:
                # Send notifications
                # notification = Notification.objects.get(notification_type="ca_approved")
                # The names that will go in the notification message template
                name_strings = [self.clean_team.name]
                link_strings = [str(self.clean_team.id)]

                user_notification = UserNotification()
                user_notification.create_notification("ca_approved", self.user, name_strings, link_strings)
            except Exception, e:
                print e

        self.user.profile.add_clean_creds(50)

    def approveCleanAmbassador(self, notification=True):
        self.status = "approved"
        self.save()
        try:
            CleanChampion.objects.filter(user=self.user, clean_team=self.clean_team).delete()
        except Exception, e:
                print e
                
        if notification:
            try:
                # Send notifications
                # notification = Notification.objects.get(notification_type="ca_approved")
                # The names that will go in the notification message template
                name_strings = [self.clean_team.name]
                link_strings = [str(self.clean_team.id)]

                user_notification = UserNotification()
                user_notification.create_notification("ca_approved", self.user, name_strings, link_strings)
            except Exception, e:
                print e

        self.user.profile.add_clean_creds(50)

    def removedCleanAmbassador(self):
        self.user.profile.clean_team_member = None
        self.user.profile.save()
        self.delete()

    def requestBecomeCleanAmbassador(self, user, selected_team, notification=True):
        self.user = user
        self.clean_team = selected_team
        self.status = "pending"
        self.role = "leader"
        self.save()

        self.user.profile.clean_team_member = CleanTeamMember.objects.latest('id')
        self.user.profile.save()

        try:
            if notification:
                # Send notifications
                # notification = Notification.objects.get(notification_type="ca_request")
                # The names that will go in the notification message template
                full_name = u'%s %s' %(self.user.first_name, self.user.last_name)
                name_strings = [full_name, self.clean_team.name]

                # users_to_notify_str = notification.users_to_notify
                users_to_notify_str = "leader"
                users_to_notify = users_to_notify_str.split(', ')

                # Notify all of the Users that have the roles within users_to_notify
                for role in users_to_notify:
                    clean_team_members = CleanTeamMember.objects.filter(role=role, clean_team=self.clean_team, status="approved")

                    for member in clean_team_members:
                        user_notification = UserNotification()
                        user_notification.create_notification("ca_request", member.user, name_strings)
        except Exception, e:
                print e

    def has_max_clean_ambassadors(self):
        num_ca = CleanTeamMember.objects.filter(clean_team_id=8).count()

        if num_ca >= 4:
            return True

        return False

"""
Name:           CleanTeamPost
Date created:   Dec 25, 2013
Description:    The posts on a Change Team's profile
"""
class CleanTeamPost(models.Model):

    clean_team = models.ForeignKey(CleanTeam)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    message = models.TextField(blank=True, null=True, default="")

    class Meta:
        verbose_name_plural = u'Change Team Post'

    def __unicode__(self):
        return u'%s post on %s' % (self.clean_team, str(self.timestamp))

    def newPost(self, user, message, clean_team, notification=True):
        self.user = user
        self.clean_team = clean_team
        self.message = message

        self.save()

        if notification:
            try:
                # Send notifications
                notification = Notification.objects.get(notification_type="message_posted")
                # The names that will go in the notification message template
                name_strings = [self.clean_team.name]
                link_strings = [str(self.clean_team.id)]

                users_to_notify_str = notification.users_to_notify
                users_to_notify = users_to_notify_str.split(', ')

                # Notify all of the Users that have the roles within users_to_notify
                for role in users_to_notify:
                    clean_team_members = CleanTeamMember.objects.filter(role=role, clean_team=self.clean_team, status="approved")

                    members_list = list(clean_team_members)

                    if role == "agent":
                        clean_champions = CleanChampion.objects.filter(clean_team=self.clean_team, status="approved")

                        members_list = list(chain(clean_team_members, clean_champions))

                    for member in members_list:
                        user_notification = UserNotification()
                        user_notification.create_notification("message_posted", member.user, name_strings, link_strings)
            except Exception, e:
                print e

        post_string = "<div class='post'>";

        if self.user.profile.picture:
            post_string += "<img class='profile-pic profile-pic-42x42' src='%s%s' alt='' />" % (settings.MEDIA_URL, self.user.profile.picture)
        else:
            post_string += "<img src='%simages/default-profile-pic-42x42.png' alt='' class='profile-pic profile-pic-42x42' />" % (settings.STATIC_URL)

        post_string += "<p class='user'><a href='/users/profile/%s'>%s</a></p>" % (self.user.id, self.user.profile.get_full_name())
        # post_string += "<p class='timestamp'>%s</p>" % date(self.timestamp, "F j, Y, g:i a")
        post_string += "<p class='timestamp'>Just now</p>"
        post_string += "<div class='clear'></div>"
        post_string += "<p class='message'>" + message + "</p></div>"
        post_string += "<div class='clear'></div>"

        return json.dumps(post_string, indent=4, separators=(',', ': '))

    def save(self, *args, **kwargs):
        super(CleanTeamPost, self).save(*args, **kwargs)

"""
Name:           CleanTeamInvite
Date created:   Jan 5, 2014
Description:    The invites that each member can receive
"""
class CleanTeamInvite(models.Model):

    email = models.EmailField(max_length=70, blank=True)
    clean_team = models.ForeignKey(CleanTeam)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    role = models.CharField(max_length=30, default="agent")
    status = models.CharField(max_length=30, default="pending")
    token = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = u'Change Team Invite'

    def __unicode__(self):
        return u'%s post on %s' % (self.clean_team, str(self.timestamp))

    # Checks if User is already registered before accpeting the invite
    # Returns False if not accepted
    def acceptInvite(self, user, notification=True):
        if self.role == "agent":
            clean_champion = CleanChampion()
            clean_champion.becomeCleanChampion(user, self.clean_team)

        elif self.role == "leader":
            ctm = CleanTeamMember()
            ctm.becomeCleanAmbassador(user, self.clean_team)

        emails = User.objects.filter(email=self.email).count()

        if emails > 0:
            self.status = "accepted"
            self.save()
            self.user.profile.add_clean_creds(10)

            if notification:
                try:
                    # Send notifications
                    notification = Notification.objects.get(notification_type="ca_joined")
                    # The names that will go in the notification message template
                    full_name = u'%s %s' %(self.user.first_name, self.user.last_name)
                    name_strings = [full_name, self.clean_team.name]

                    users_to_notify_str = notification.users_to_notify
                    users_to_notify = users_to_notify_str.split(', ')

                    # Notify all of the Users that have the roles within users_to_notify
                    for role in users_to_notify:
                        clean_team_members = CleanTeamMember.objects.filter(role=role, clean_team=self.clean_team, status="approved")

                        for member in clean_team_members:
                            user_notification = UserNotification()
                            user_notification.create_notification("ca_joined", member.user, name_strings)

                    # self.clean_team.add_team_clean_creds(5)
                except Exception, e:
                    print e

            return True

        return False

    def inviteUser(self, user, role, email, uri, notification=True):
        char_set = string.ascii_lowercase + string.digits
        token = ''.join(random.sample(char_set*20,20))
        invite_full_uri = u'%s/%s' % (uri, token)
        unsubscribe_full_uri = u'%s/unsubscribe/' % (uri)

        self.clean_team = user.profile.clean_team_member.clean_team
        self.user = user
        self.email = str(email)
        self.role = role
        self.status = 'pending'
        self.token = token
        self.save()

        # If the User is already registered, send them a notification
        try:
            u = User.objects.get(email=str(email))
        except Exception, e:
            u = None

        if notification:
            try:
                if u:
                    # Send notifications
                    notification_type = "cc_invite"
                    if role == "leader":
                        notification_type = "ca_invite"

                    notification = Notification.objects.get(notification_type=notification_type)
                    # The names that will go in the notification message template
                    full_name = u'%s %s' %(self.user.first_name, self.user.last_name)
                    name_strings = [full_name, self.clean_team.name]
                    link_strings = [str(self.token)]

                    user_notification = UserNotification()
                    user_notification.create_notification(notification_type, u, name_strings, link_strings)
            except Exception, e:
                print e

        if self.clean_team.level.name == "Seedling":
            if self.clean_team.count_invites_sent() > 4:
                task = CleanTeamLevelTask.objects.get(name="invite_5_mcc")
                self.clean_team.complete_level_task(task)

        # from django.core.mail import send_mail
        # send_mail('test', 'test', 'zee@hakstudio.com', [email])

        # Send invite email to email address
        template = get_template('emails/email_invite_agent.html')
        if role == "leader":
            template = get_template('emails/email_invite_leader.html')
        content = Context({ 'user': user, 'email': email, 'role': role, 'invite_full_uri': invite_full_uri, 'unsubscribe_full_uri': unsubscribe_full_uri })

        subject, from_email, to = 'My Effect - Invite to join', settings.DEFAULT_FROM_EMAIL, email

        send_email = SendEmail()
        send_email.send(template, content, subject, from_email, to)

    def unsubscribe(self):
        self.status = "declined"
        self.save()

    def resendInvite(self, uri):
        invite_full_uri = u'%s/%s' % (uri, self.token)

        # from django.core.mail import send_mail
        # send_mail('test', 'test', 'zee@hakstudio.com', [email])

        # Send invite email to email address
        template = get_template('emails/email_invite_agent.html')
        if self.role == "leader":
            template = get_template('emails/email_invite_leader.html')
        content = Context({ 'user': self.user, 'email': self.email, 'role': self.role, 'invite_full_uri': invite_full_uri })

        subject, from_email, to = 'My Effect - Invite to join', settings.DEFAULT_FROM_EMAIL, self.email

        send_email = SendEmail()
        send_email.send(template, content, subject, from_email, to)

    def save(self, *args, **kwargs):
        super(CleanTeamInvite, self).save(*args, **kwargs)

"""
Name:           CleanTeamLevelTask
Date created:   Jan 30, 2014
Description:    All of the tasks required to be completed in a level
"""
class CleanTeamLevelTask(models.Model):

    clean_team_level = models.ForeignKey(CleanTeamLevel)
    name = models.CharField(max_length=60, blank=False, unique=True, default="", verbose_name='Task Name')
    description = models.TextField(blank=True, null=True, default="")
    link = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=50, null=True)
    approval_required = models.BooleanField(default=0)

    class Meta:
        verbose_name_plural = u'Change Team Level Task'

    def __unicode__(self):
        return u'%s: %s' % (self.name, self.description)

    def save(self, *args, **kwargs):
        super(CleanTeamLevelTask, self).save(*args, **kwargs)

"""
Name:           CleanTeamLevelProgress
Date created:   Jan 30, 2014
Description:    The tasks each Change Team has completed per level
"""
class CleanTeamLevelProgress(models.Model):

    clean_team = models.ForeignKey(CleanTeam)
    level_task = models.ForeignKey(CleanTeamLevelTask)
    approval_requested = models.BooleanField(default=0)
    completed = models.BooleanField(default=0)

    class Meta:
        verbose_name_plural = u'Change Team Level Progress'

    def __unicode__(self):
        return u'%s - %s' % (self.clean_team, self.level_task)

    def submit_for_approval(self):
        self.approval_requested = True
        self.completed = False
        self.save()

    def save(self, *args, **kwargs):
        super(CleanTeamLevelProgress, self).save(*args, **kwargs)

"""
Name:           LeaderReferral
Date created:   Mar 4, 2014
Description:    When Change Teams refer leaders
"""
class LeaderReferral(models.Model):

    first_name = models.CharField(max_length=60, blank=False, default="")
    last_name = models.CharField(max_length=60, blank=False, default="")
    email = models.CharField(max_length=60, blank=False, default="")
    organization = models.CharField(max_length=60, blank=False, default="")
    title = models.CharField(max_length=60, blank=False, default="")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    clean_team = models.ForeignKey(CleanTeam, null=True)
    status = models.CharField(max_length=30, default="pending")
    token = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, null=True)


    class Meta:

        verbose_name_plural = u'Change Team Leader Referrals'

    def __unicode__(self):
        return u'%s %s from %s' % (self.first_name, self.last_name, self.organization)

    def new_referral(self, user, form, clean_team, uri):
        char_set = string.ascii_lowercase + string.digits
        token = ''.join(random.sample(char_set*20,20))
        invite_full_uri = u'%s' % (uri+token)
        unsubscribe_full_uri = u'%sunsubscribe/' % (uri)
        self.first_name = form.cleaned_data['first_name']
        self.last_name = form.cleaned_data['last_name']
        self.email = form.cleaned_data['email']
        self.organization = form.cleaned_data['organization']
        self.title = form.cleaned_data['title']
        self.status = 'pending'
        self.token = token

        self.user = user
        self.clean_team = clean_team

        self.save()

        if self.clean_team.level.name == "Seedling":
            task = CleanTeamLevelTask.objects.get(name="refer_teacher")
            self.clean_team.complete_level_task(task)

        template = get_template('emails/email_invite_org.html')
        content = Context({ 'user': user, 'email': self.email, 'first_name': self.first_name, 'last_name': self.last_name, 'invite_full_uri': invite_full_uri, 'unsubscribe_full_uri': unsubscribe_full_uri})

        subject, from_email, to = 'My Effect - Invite to join', settings.DEFAULT_FROM_EMAIL, self.email

        send_email = SendEmail()
        send_email.send(template, content, subject, from_email, to)

    def save(self, *args, **kwargs):
        super(LeaderReferral, self).save(*args, **kwargs)

"""
Name:           CleanTeamPresentation
Date created:   Mar 5, 2014
Description:    When Change Teams submits a presentation
"""
class CleanTeamPresentation(models.Model):

    title = models.CharField(max_length=60, blank=False, default="")
    presentation = models.FileField(upload_to=get_upload_file_name, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    clean_team = models.ForeignKey(CleanTeam, null=True)
    user = models.ForeignKey(User, null=True)

    class Meta:
        verbose_name_plural = u'Change Team Presentation'

    def __unicode__(self):
        return u'%s by %s' % (self.title, self.clean_team.name)

    def new_submission(self, user, form, clean_team):
        self.title = form.cleaned_data['title']
        presentation = form.cleaned_data['presentation']

        self.user = user
        self.clean_team = clean_team

        if presentation:
            key = 'presentations/ct_presentation_%s_%s' % (str(self.clean_team.id), presentation)
            uploadFile = UploadFileToS3()
            self.presentation = uploadFile.upload(key, presentation)

        self.save()

        if self.clean_team.level.name == "Seedling":
            task = CleanTeamLevelTask.objects.get(name="mcc_presentation")
            self.clean_team.complete_level_task(task)

    def save(self, *args, **kwargs):
        super(CleanTeamPresentation, self).save(*args, **kwargs)


class CleanTeamFollow(models.Model):

    clean_team = models.ForeignKey(CleanTeam, null=True)
    user = models.ForeignKey(User, null=True)

    class Meta:
        verbose_name_plural = u'Change Team Followers'

    def __unicode__(self):
        return u'%s is following %s' % (self.user.email, self.clean_team.name)

    def save(self, *args, **kwargs):
        super(CleanTeamFollow, self).save(*args, **kwargs)

    def become_clean_follower(self, user, selected_team):
        self.user = user
        self.clean_team = selected_team
        self.save()

"""
Name:           TeamCommunityMembership
Date created:   March 12, 2015
Description:    An association that describes that a team is associated with a specific community
"""
class TeamCommunityMembership(models.Model):
    clean_team = models.ForeignKey(CleanTeam, null=False)
    community = models.ForeignKey(Community, null=False)

    class Meta:
        verbose_name_plural = u'Community Team Membership'

    def __unicode__(self):
        return u'%s' % self.id

    def save(self, *args, **kwargs):
        super(TeamCommunityMembership, self).save(*args, **kwargs)

"""
Name:           UserCommunityMembership
Date created:   March 12, 2015
Description:    An association that describes that a user is associated with a specific community
"""
class UserCommunityMembership(models.Model):
    user = models.ForeignKey(User, null=False)
    community = models.ForeignKey(Community, null=False)

    class Meta:
        verbose_name_plural = u'Community User Membership'

    def __unicode__(self):
        return u'%s' % self.id

    def save(self, *args, **kwargs):
        super(UserCommunityMembership, self).save(*args, **kwargs)
