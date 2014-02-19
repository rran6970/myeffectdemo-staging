from django.contrib import admin
from challenges.models import *

from mycleancity.actions import export_as_csv_action

from users.models import *

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clean_team', 'title', 'timestamp', 'event_date', 'event_time', 'clean_creds_per_hour')
    search_fields = ['title', 'user__id', 'user__first_name', 'user__last_name', 'user__organization']
    actions = [export_as_csv_action("CSV Export")]

class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'challenge', 'user', 'timestamp', 'time_in', 'time_out', 'total_hours', 'total_clean_creds')
    search_fields = ['user__id', 'user__first_name', 'user__last_name', 'challenge']
    actions = [export_as_csv_action("CSV Export")]

class CleanGridAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value')
    search_fields = ['name']
    actions = [export_as_csv_action("CSV Export")]

class ChallengeQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_number', 'question', 'type', 'answer_type')
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

class UserChallengeSurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'clean_team', 'challenge', 'total_score')
    search_fields = ['user', 'clean_team', 'challenge']
    actions = [export_as_csv_action("CSV Export")]

class UserChallengeSurveyAnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'answer')
    search_fields = ['user', 'survey', 'answer']
    actions = [export_as_csv_action("CSV Export")]

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(UserChallenge, UserChallengeAdmin)
admin.site.register(CleanGrid, CleanGridAdmin)
admin.site.register(ChallengeQuestion, ChallengeQuestionAdmin)
admin.site.register(ChallengeQuestionType, ChallengeQuestionTypeAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(UserChallengeSurvey, UserChallengeSurveyAdmin)
admin.site.register(UserChallengeSurveyAnswers, UserChallengeSurveyAnswersAdmin)