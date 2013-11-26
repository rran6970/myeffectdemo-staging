from django.contrib import admin
from django.core.mail import EmailMessage
from django.template import Context, RequestContext
from django.template.loader import get_template

from cleanteams.models import *

class CleanTeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website')
    search_fields = ['name']

admin.site.register(CleanTeam, CleanTeamAdmin)