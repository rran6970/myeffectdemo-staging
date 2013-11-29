from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from cleanteams.views import CleamTeamView, RegisterCleanTeamView

urlpatterns = patterns('',
	url(r'^register-clean-team/?$', RegisterCleanTeamView.as_view()),
	url(r'^(?P<ctid>\d+)/?$', CleamTeamView.as_view()),
)