from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from notifications.views import *

urlpatterns = patterns('',
	url(r'^/?$', NotificationsFeedView.as_view()),
	url(r'^read-all/?$', 'notifications.views.read_all_notifications'),
	url(r'^read/?$', 'notifications.views.read_notification'),
	url(r'^quick-read/?$', 'notifications.views.read_notification'),
	url(r'^quick-unread/?$', 'notifications.views.unread_notification'),
)