from django.contrib import admin
from challenges.models import *
from users.models import *

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clean_team', 'title', 'timestamp', 'event_date', 'event_time')
    search_fields = ['title', 'user__id', 'user__first_name', 'user__last_name', 'user__organization']

class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'challenge', 'user', 'timestamp', 'time_in', 'time_out', 'total_hours', 'complete')
    search_fields = ['user__id', 'user__first_name', 'user__last_name', 'challenge']    

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(UserChallenge, UserChallengeAdmin)