from django.contrib import admin
from userorganization.models import *

class UserOrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'organization', 'city', 'postal_code', 'country')
    search_fields = ['user__id', 'user__first_name', 'user__last_name']

admin.site.register(UserOrganization, UserOrganizationAdmin)