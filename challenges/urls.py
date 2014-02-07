from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from challenges.views import *

urlpatterns = patterns('',
	url(r'^/?$', ChallengesFeedView.as_view()),
	url(r'^fr/?', TemplateView.as_view(template_name="mycleancity/french/challenge_centre_fr.html")),

	url(r'^(?P<cid>\d+)/?$', ChallengeView.as_view()),
	url(r'^edit/(?P<cid>\d+)/?$', EditChallengeView.as_view()),
	url(r'^new-challenge/?$', NewChallengeView.as_view()),
	url(r'^participants/(?P<cid>\d+)/?$', ChallengeParticipantsView.as_view()),
	url(r'^my-challenges/?$', MyChallengesView.as_view()),
	# url(r'^confirm-participants/?$', 'challenges.views.confirm_participants'),
	url(r'^check-in-check-out/?$', 'challenges.views.check_in_check_out'),
	url(r'^participate/?$', 'challenges.views.participate_in_challenge'),
)