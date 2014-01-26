from django.contrib import admin
from userprofile.models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'province', 'clean_team_member')
    search_fields = ['user__id', 'user__first_name', 'user__last_name', 'user__email']

class QRCodeSignupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'timestamp')
    search_fields = ['user__id']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(QRCodeSignups, QRCodeSignupsAdmin)