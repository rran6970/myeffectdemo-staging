from django.contrib import admin
from userprofile.models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'organization', 'dob', 'city', 'postal_code', 'country')
    search_fields = ['user__id', 'user__first_name', 'user__last_name']

admin.site.register(UserProfile, UserProfileAdmin)