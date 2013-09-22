from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

from mycleancity.views import HomePageView
from users.views import PrelaunchView

admin.autodiscover()

urlpatterns = patterns('',
	# url(r'^test/?', 'mycleancity.views.index', name='test'),

	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/login/?', 'users.views.login'),

	url(r'^challenges/', include('challenges.urls')),
	url(r'^cleancreds/', include('cleancreds.urls')),
	url(r'^users/', include('users.urls')),

	url(r'^$', PrelaunchView.as_view(), name='prelaunch'),
	url(r'^success/?', TemplateView.as_view(template_name='mycleancity/success.html')),
)

if settings.DEBUG:
	urlpatterns += patterns('django.contrib.staticfiles.views',
		url(r'^static/(?P<path>.*)$', 'serve'),
	)