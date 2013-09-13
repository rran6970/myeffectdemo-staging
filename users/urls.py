from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from users.views import *

urlpatterns = patterns('',
    # url(r'^/?$', PrelaunchView.as_view(), name='prelaunch'),
    url(r'^login/?$', LoginView.as_view(), name='login'),
    url(r'^register/?$', RegisterView.as_view(), name='register'),
)