from django.contrib import admin
from cleanteams.models import *
from mycleancity.actions import export_as_csv_action


class CleanTeamLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'badge')
    search_fields = ['name']
    actions = [export_as_csv_action("CSV Export")]


class CleanTeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website', 'clean_creds', 'level', 'admin')
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
    list_display = ('id', 'clean_team_level', 'description', 'link', 'approval_required')
    search_fields = ['user', 'clean_team_level', 'description', 'approval_required']
    actions = [export_as_csv_action("CSV Export")]


class CleanTeamLevelProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'clean_team', 'level_task', 'approval_requested', 'completed')
    search_fields = ['clean_team', 'level_task', 'approval_requested', 'completed']
    actions = ['complete_tasks', export_as_csv_action("CSV Export")]    

    def complete_tasks(self, request, queryset):
        for row in queryset:
            row.clean_team.complete_level_task(row.level_task)


class LeaderReferralAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'organization', 'title', 'clean_team', 'user')
    search_fields = ['user', 'email', 'organization']
    actions = [export_as_csv_action("CSV Export")]


class CleanTeamFollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clean_team')
    search_fields = ['user', 'clean_team']
    actions = [export_as_csv_action("CSV Export")]


class CleanTeamPresentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'presentation', 'clean_team', 'user')
    search_fields = ['user', 'title']
    actions = [export_as_csv_action("CSV Export")]

class TeamAntiSpamAdmin(admin.ModelAdmin):
    list_display = ('id', 'clean_team', 'blocked', 'group_name', 'email', 'address')
    search_fields = ['clean_team', 'group_name']
    actions = [export_as_csv_action("CSV Export")]

admin.site.register(CleanTeamLevel, CleanTeamLevelAdmin)
admin.site.register(CleanTeam, CleanTeamAdmin)
admin.site.register(CleanTeamMember, CleanTeamMemberAdmin)
admin.site.register(CleanTeamPost, CleanTeamPostAdmin)
admin.site.register(CleanChampion, CleanChampionAdmin)
admin.site.register(CleanTeamInvite, CleanTeamInviteAdmin)
admin.site.register(CleanTeamLevelTask, CleanTeamLevelTaskAdmin)
admin.site.register(CleanTeamLevelProgress, CleanTeamLevelProgressAdmin)
admin.site.register(CleanTeamPresentation, CleanTeamPresentationAdmin)
admin.site.register(LeaderReferral, LeaderReferralAdmin)
admin.site.register(TeamAntiSpam, TeamAntiSpamAdmin)