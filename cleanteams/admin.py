from django.contrib import admin
from django.core.mail import EmailMessage
from django.template import Context, RequestContext
from django.template.loader import get_template

from cleanteams.models import *

from mycleancity.actions import export_as_csv_action

class CleanTeamLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'badge')
    search_fields = ['name']
    actions = [export_as_csv_action("CSV Export")]

class CleanTeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website', 'clean_creds', 'level')
    search_fields = ['name', 'level']
    actions = [export_as_csv_action("CSV Export")]

class CleanTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clean_team', 'status', 'role')
    search_fields = ['user', 'clean_team', 'status', 'role']
    actions = [export_as_csv_action("CSV Export")]

class CleanChampionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clean_team', 'status')
    search_fields = ['user', 'clean_team', 'status', 'role']
    actions = [export_as_csv_action("CSV Export")]

class CleanTeamPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'clean_team', 'user', 'timestamp')
    search_fields = ['user', 'clean_team', 'user']
    actions = [export_as_csv_action("CSV Export")]

class CleanTeamInviteAdmin(admin.ModelAdmin):
    list_display = ('id', 'clean_team', 'user', 'email', 'role', 'timestamp')
    search_fields = ['user', 'clean_team', 'user']
    actions = [export_as_csv_action("CSV Export")]

class CleanTeamLevelTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'clean_team_level', 'description', 'link')
    search_fields = ['user', 'clean_team_level', 'description']
    actions = [export_as_csv_action("CSV Export")]

class CleanTeamLevelProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'clean_team', 'level_task', 'completed')
    search_fields = ['clean_team', 'level_task', 'completed']
    actions = ['complete_tasks', export_as_csv_action("CSV Export")]    

    def complete_tasks(self, request, queryset):
        for row in queryset:
            row.clean_team.complete_level_task(row.level_task)

class LeaderReferralAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'organization', 'title', 'clean_team', 'user')
    search_fields = ['user', 'email', 'organization']
    actions = [export_as_csv_action("CSV Export")]

admin.site.register(CleanTeamLevel, CleanTeamLevelAdmin)
admin.site.register(CleanTeam, CleanTeamAdmin)
admin.site.register(CleanTeamMember, CleanTeamMemberAdmin)
admin.site.register(CleanTeamPost, CleanTeamPostAdmin)
admin.site.register(CleanChampion, CleanChampionAdmin)
admin.site.register(CleanTeamInvite, CleanTeamInviteAdmin)
admin.site.register(CleanTeamLevelTask, CleanTeamLevelTaskAdmin)
admin.site.register(CleanTeamLevelProgress, CleanTeamLevelProgressAdmin)
admin.site.register(LeaderReferral, LeaderReferralAdmin)