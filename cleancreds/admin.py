from django.contrib import admin
from cleancreds.models import *
from users.models import *

class CleanCredsMilestonesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'cleancreds_needed')
    search_fields = ['title']

class CleanCredsAchievementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'milestone')
    search_fields = ['user__id', 'user__first_name', 'user__last_name', 'milestone']    

admin.site.register(CleanCredsMilestones, CleanCredsMilestonesAdmin)
admin.site.register(CleanCredsAchievements, CleanCredsAchievementsAdmin)