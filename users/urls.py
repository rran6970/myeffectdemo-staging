from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from users.views import *

urlpatterns = patterns('',
	# User Auth URLs
	url(r'^login/?', 'users.views.login'),
	url(r'^auth/?', 'users.views.auth_view'),
	url(r'^logout/?', 'users.views.logout'),
	url(r'^loggedin/?', 'users.views.loggedin'),
	url(r'^invalid/?', 'users.views.invalid_login'),
	# url(r'^register/?', 'users.views.register_user'),
	url(r'^register_success/?', 'users.views.register_success'),

   	# url(r'^login/?$', LoginView.as_view(), name='login'),
    url(r'^register/?$', RegisterView.as_view(), name='register'),
    url(r'^profile/?$', ProfileView.as_view(), name='profile'),

    url(r'^/?$', PrelaunchView.as_view(), name='prelaunch'),
)