from django.contrib import admin
from userprofile.models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'province', 'clean_team_member')
    search_fields = ['user__id', 'user__first_name', 'user__last_name', 'user__email']

admin.site.register(UserProfile, UserProfileAdmin)