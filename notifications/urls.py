from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from notifications.views import *

urlpatterns = patterns('',
	url(r'^/?$', NotificationsFeedView.as_view()),
	url(r'^read/?$', 'notifications.views.read_notification'),
)