from django.contrib import admin
from challenges.models import *

from mycleancity.actions import export_as_csv_action

from users.models import *

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clean_team', 'title', 'timestamp', 'event_date', 'event_time')
    search_fields = ['title', 'user__id', 'user__first_name', 'user__last_name', 'user__organization']
    actions = [export_as_csv_action("CSV Export")]

class ChallengeCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'challenge')
    search_fields = ['challenge__id', 'challenge__title', 'category__name'] 
    actions = [export_as_csv_action("CSV Export")]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'clean_cred_value')
    search_fields = ['name', 'challenge__title']
    actions = [export_as_csv_action("CSV Export")]

class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'challenge', 'user', 'timestamp', 'time_in', 'time_out', 'total_hours')
    search_fields = ['user__id', 'user__first_name', 'user__last_name', 'challenge']
    actions = [export_as_csv_action("CSV Export")]

class CleanGridAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value')
    search_fields = ['name']
    actions = [export_as_csv_action("CSV Export")]

class ChallengeQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_number', 'question', 'type')
    search_fields = ['question', 'type']
    actions = [export_as_csv_action("CSV Export")]

class ChallengeQuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ['name']
    actions = [export_as_csv_action("CSV Export")]

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'score', 'clean_grid')
    search_fields = ['question', 'question_number']
    actions = [export_as_csv_action("CSV Export")]

class UserQuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'answer', 'clean_team')
    search_fields = ['user', 'answer', 'clean_team']
    actions = [export_as_csv_action("CSV Export")]

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(ChallengeCategory, ChallengeCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserChallenge, UserChallengeAdmin)
admin.site.register(CleanGrid, CleanGridAdmin)
admin.site.register(ChallengeQuestion, ChallengeQuestionAdmin)
admin.site.register(ChallengeQuestionType, ChallengeQuestionTypeAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(UserQuestionAnswer, UserQuestionAnswerAdmin)