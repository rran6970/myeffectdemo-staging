from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from challenges.views import *

urlpatterns = patterns('',
	url(r'^/?$', ChallengesFeedView.as_view()),
	url(r'^(?P<cid>\d+)/?$', ChallengeView.as_view()),
	url(r'^participants/(?P<cid>\d+)/?$', ChallengeParticipantsView.as_view()),
	url(r'^participate/?$', 'challenges.views.participate_in_challenge'),
	url(r'^new-challenge/?$', NewChallengeView.as_view()),
)