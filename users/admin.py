from django.contrib import admin
from users.models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'organization', 'dob', 'city', 'postal_code', 'country')
    search_fields = ['user__id', 'user__first_name', 'user__last_name']

class PrelaunchEmailsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'postal_code', 'school_type', 'ambassador', 'timestamp')
    search_fields = ['email', 'first_name', 'school_type']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PrelaunchEmails, PrelaunchEmailsAdmin)