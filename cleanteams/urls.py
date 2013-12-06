from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from cleanteams.views import *

urlpatterns = patterns('',
	url(r'^members/?$', CleanTeamMembersView.as_view()),
	url(r'^register-clean-team/?$', RegisterCleanTeamView.as_view()),
	url(r'^register-request-join/?$', RegisterRequestJoinView.as_view()),
	url(r'^register-clean-champion/?$', RegisterCleanChampionView.as_view()),
	url(r'^request-join/?$', 'cleanteams.views.request_join_clean_team'),
	url(r'^member-action/?$', 'cleanteams.views.clean_team_member_action'),
	url(r'^/?$', CreateOrRequest.as_view()),
	url(r'^(?P<ctid>\d+)/?$', CleanTeamView.as_view()),
)