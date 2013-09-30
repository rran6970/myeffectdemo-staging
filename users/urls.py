from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from users.views import *

urlpatterns = patterns('',
	url(r'^login/?', LoginPageView.as_view()),
	url(r'^auth/?', 'users.views.auth_view'),
	url(r'^logout/?', 'users.views.logout'),
	url(r'^loggedin/?', 'users.views.loggedin'),	
	url(r'^register_success/?', 'users.views.register_success'),
	url(r'^leaderboard/?$', LeaderboardView.as_view()),
    url(r'^register/?$', RegisterView.as_view()),
    url(r'^register-organization/?$', RegisterOrganizationView.as_view()),
    url(r'^profile/?$', ProfileView.as_view()),

    url(r'^/?$', PrelaunchView.as_view()),
)