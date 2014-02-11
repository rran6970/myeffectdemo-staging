from django.contrib import admin
from django.core.mail import EmailMessage
from django.template import Context, RequestContext
from django.template.loader import get_template

from mycleancity.actions import export_as_csv_action

from notifications.models import *

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'message', 'users_to_notify')
    search_fields = ['name']
    actions = [export_as_csv_action("CSV Export")]

class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notification', 'read', 'timestamp')
    search_fields = ['user', 'notification', 'read']
    actions = [export_as_csv_action("CSV Export")]

admin.site.register(Notification, NotificationAdmin)
admin.site.register(UserNotification, UserNotificationAdmin)