from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from cleanteams.views import *

urlpatterns = patterns('',
	url(r'^invite/?$', InviteView.as_view()),
	url(r'^invite-org/?$', InviteOrganizationView.as_view()),
	url(r'^invite/unsubscribe/(?P<token>\w+)/?$', 'cleanteams.views.unsubscribe'),
	url(r'^invite/(?P<token>\w+)/?$', 'cleanteams.views.invite_check'),
	url(r'^invite-org/(?P<token>\w+)/?$', 'cleanteams.views.referral_check'),
	url(r'^resend-invite/?$', 'cleanteams.views.resend_invite'),
	url(r'^invite-response/(?P<token>\w+)/?$', InviteResponseView.as_view()),
	# url(r'^invite/(?P<token>\w+)/?$', 'cleanteams.views.accept_invite'),
	url(r'^post-message-ajax/?$', 'cleanteams.views.post_message_ajax'),
	url(r'^post-message/?$', PostMessageView.as_view()),
	url(r'^members/?$', CleanTeamMembersView.as_view()),
	url(r'^level-progress/?$', LevelProgressView.as_view()),
	url(r'^edit/?$', EditCleanTeamView.as_view()),
	url(r'^main-contact/?$', CleanTeamMainContactView.as_view()),
	url(r'^register-clean-team/?$', RegisterCleanTeamView.as_view()),
	url(r'^register-request-join/?$', RegisterRequestJoinView.as_view()),
	url(r'^register-catalyst/?$', RegisterCleanChampionView.as_view()),
	url(r'^leader-referral/?$', LeaderReferralView.as_view()),
	url(r'^send-presentation/?$', CleanTeamPresentationView.as_view()),
	url(r'^cc-join/?$', 'cleanteams.views.be_clean_champion'),
	url(r'^ca-request-join/?$', 'cleanteams.views.request_join_clean_team'),
	url(r'^member-action/?$', 'cleanteams.views.clean_team_member_action'),
	url(r'^create-or-request/?$', CreateOrRequest.as_view()),
	url(r'^/?$', ViewAllCleanTeams.as_view()),
	url(r'^(?P<ctid>\d+)/?$', CleanTeamView.as_view()),
)