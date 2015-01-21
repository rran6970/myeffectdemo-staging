from django.contrib import admin
from django.contrib.sites.models import Site

from mycleancity.actions import export_as_csv_action

from users.models import *

class PrelaunchEmailsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'postal_code', 'school_type', 'ambassador', 'timestamp')
    search_fields = ['email', 'first_name', 'school_type']
    actions = [export_as_csv_action("CSV Export")]

class ProfilePhaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'drop_level')
    search_fields = ['name']
    actions = [export_as_csv_action("CSV Export")]

class ProfileTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile_phase', 'description', 'link', 'approval_required')
    search_fields = ['user', 'profile_phase', 'description', 'approval_required']
    actions = [export_as_csv_action("CSV Export")]

class ProfileProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_task', 'approval_requested', 'completed')
    search_fields = ['user', 'profile_task', 'approval_requested', 'completed']
    actions = ['complete_tasks', export_as_csv_action("CSV Export")]

    def complete_tasks(self, request, queryset):
        for row in queryset:
            row.user.complete_level_task(row.level_task)
    
admin.site.register(PrelaunchEmails, PrelaunchEmailsAdmin)
admin.site.register(ProfilePhase, ProfilePhaseAdmin)
admin.site.register(ProfileTask, ProfileTaskAdmin)
admin.site.register(ProfileProgress, ProfileProgressAdmin)
admin.site.register(Site)