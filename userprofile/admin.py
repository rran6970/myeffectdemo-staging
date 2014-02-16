from django.contrib import admin

from mycleancity.actions import export_as_csv_action

from userprofile.models import *

class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'communication_language')
    search_fields = ['user__id', 'user__first_name', 'user__last_name', 'user__email']
    actions = [export_as_csv_action("CSV Export")]

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'province', 'clean_team_member')
    search_fields = ['user__id', 'user__first_name', 'user__last_name', 'user__email']
    actions = [export_as_csv_action("CSV Export")]

class QRCodeSignupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'timestamp')
    search_fields = ['user__id']
    actions = [export_as_csv_action("CSV Export")]

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserSettings, UserSettingsAdmin)
admin.site.register(QRCodeSignups, QRCodeSignupsAdmin)