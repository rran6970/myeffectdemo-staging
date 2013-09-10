from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from users.views import *

urlpatterns = patterns('',
    url(r'^test/$', IndexView.as_view(), name='index'),
)