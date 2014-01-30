from django.contrib import admin
from django.core.mail import EmailMessage
from django.template import Context, RequestContext
from django.template.loader import get_template

from cleanteams.models import *

class CleanTeamLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'badge')
    search_fields = ['name']

class CleanTeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website', 'clean_creds', 'level')
    search_fields = ['name', 'level']

class CleanTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clean_team', 'status', 'role')
    search_fields = ['user', 'clean_team', 'status', 'role']

class CleanChampionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clean_team', 'status')
    search_fields = ['user', 'clean_team', 'status', 'role']

class CleanTeamPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'clean_team', 'user', 'timestamp')
    search_fields = ['user', 'clean_team', 'user']

class CleanTeamInviteAdmin(admin.ModelAdmin):
    list_display = ('id', 'clean_team', 'user', 'email', 'role', 'timestamp')
    search_fields = ['user', 'clean_team', 'user']

class CleanTeamLevelTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'clean_team_level', 'description')
    search_fields = ['user', 'clean_team_level', 'description']

class CleanTeamLevelProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'clean_team', 'level_task', 'completed')
    search_fields = ['clean_team', 'level_task', 'completed']

admin.site.register(CleanTeamLevel, CleanTeamLevelAdmin)
admin.site.register(CleanTeam, CleanTeamAdmin)
admin.site.register(CleanTeamMember, CleanTeamMemberAdmin)
admin.site.register(CleanTeamPost, CleanTeamPostAdmin)
admin.site.register(CleanChampion, CleanChampionAdmin)
admin.site.register(CleanTeamInvite, CleanTeamInviteAdmin)
admin.site.register(CleanTeamLevelTask, CleanTeamLevelTaskAdmin)
admin.site.register(CleanTeamLevelProgress, CleanTeamLevelProgressAdmin)