from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from cleanteams.views import *
from userorganization.views import *
from users.views import *

urlpatterns = patterns('',
	url(r'^login/?', LoginPageView.as_view()),
	url(r'^auth/?', 'users.views.auth_view'),
	url(r'^logout/?', 'users.views.logout'),	
	url(r'^register_success/?', 'users.views.register_success'),
	url(r'^leaderboard/?$', LeaderboardView.as_view()),
    url(r'^register/?$', RegisterView.as_view()),
    url(r'^register-organization/?$', RegisterOrganizationView.as_view()),
    url(r'^profile/(?P<uid>\d+)/?$', ProfilePublicView.as_view()),
    url(r'^profile/?$', ProfileView.as_view()),    
    url(r'^organization-profile/?$', OrganizationProfileView.as_view()),
    # url(r'^organization/(?P<uid>\d+)/?$', OrganizationProfilePublicView.as_view()),

    url(r'^/?$', PrelaunchView.as_view()),
)