from django.contrib import admin
from django.core.mail import EmailMessage
from django.template import Context, RequestContext
from django.template.loader import get_template

from notifications.models import *

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'message', 'users_to_notify')
    search_fields = ['name']

class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notification', 'read', 'timestamp')
    search_fields = ['user', 'notification', 'read']

admin.site.register(Notification, NotificationAdmin)
admin.site.register(UserNotification, UserNotificationAdmin)