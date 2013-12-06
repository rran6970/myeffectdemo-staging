from django.contrib import admin
from django.core.mail import EmailMessage
from django.template import Context, RequestContext
from django.template.loader import get_template

from cleanteams.models import *

class CleanTeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website')
    search_fields = ['name']

class CleanTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clean_team', 'status', 'role')
    search_fields = ['user', 'clean_team', 'status', 'role']

admin.site.register(CleanTeam, CleanTeamAdmin)
admin.site.register(CleanTeamMember, CleanTeamMemberAdmin)