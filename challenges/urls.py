from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from challenges.views import *

urlpatterns = patterns('',
	url(r'^/?$', NewChallengeView.as_view()),
	url(r'^(?P<cid>\d+)?$', ChallengeView.as_view()),
	url(r'^new-challenge/?$', NewChallengeView.as_view()),
)