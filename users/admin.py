from django.contrib import admin
from django.contrib.sites.models import Site

from mycleancity.actions import export_as_csv_action
from cleanteams.models import CleanTeamMember
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
class OrganizationLicenseAdmin(admin.ModelAdmin):
    list_display = ('edit_link', 'id', 'code', 'user', 'custom_user_name', 'user_email', 'organization', 'is_charity', 'from_date', 'to_date')
    raw_id_fields = ("user",)
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'code']
    actions = [export_as_csv_action("CSV Export")]

    def custom_user_name(self, obj):
        if obj.user:
            if obj.user.first_name and obj.user.last_name:
                return '%s %s' % (obj.user.first_name, obj.user.last_name)
        return ""
    custom_user_name.allow_tags = True
    custom_user_name.short_description = 'User Name'

    def organization(self, obj):
        name = ""
        if obj.user:
            if CleanTeamMember.objects.filter(user=obj.user, role="manager"):
                name = CleanTeamMember.objects.filter(user=obj.user, role="manager")[0].clean_team.name
        return name
    organization.allow_tags = True
    organization.short_description = 'Organization'

    def user_email(self, obj):
        if obj.user:
            if obj.user.email:
                return '%s' % obj.user.email
        return ""
    user_email.allow_tags = True
    user_email.short_description = 'Email'

    def edit_link(self,obj):
        #return u'<a href="/admin/%s/%s/%s">Edit</a>' % ( obj._meta.app_label, obj._meta.module_name, obj.id)
        return "Edit"
    edit_link.allow_tags = True
    edit_link.short_description = " "

admin.site.register(PrelaunchEmails, PrelaunchEmailsAdmin)
admin.site.register(ProfilePhase, ProfilePhaseAdmin)
admin.site.register(ProfileTask, ProfileTaskAdmin)
admin.site.register(ProfileProgress, ProfileProgressAdmin)
admin.site.register(OrganizationLicense, OrganizationLicenseAdmin)
#admin.site.register(Site)