from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

from mycleancity.views import *
from users.views import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^captcha/', include('captcha.urls')),

	url(r'^clean-team/', include('cleanteams.urls')),
	url(r'^challenges/', include('challenges.urls')),
	url(r'^cleancreds/', include('cleancreds.urls')),
	url(r'^notifications/', include('notifications.urls')),
	url(r'^users/', include('users.urls')),

	url(r'^register-success/?', RegisterSuccessView.as_view()),
	url(r'^register/(?P<qrcode>\w+)/?$', RegisterView.as_view()),
	url(r'^register/?$', RegisterView.as_view()),
	url(r'^register-invite/(?P<token>\w+)/?$', RegisterInviteView.as_view()),
	url(r'^landing/?', PrelaunchView.as_view()),
	url(r'^about/?', AboutPageView.as_view()),
	url(r'^students/?', StudentsPageView.as_view()),
	url(r'^rewards/?', RewardsPageView.as_view()),
	url(r'^organizations/?', OrganizationsPageView.as_view()),
	url(r'^contact/?', ContactPageView.as_view()),
	url(r'^media-hub/?', MediaHubPageView.as_view()),
	url(r'^$', HomePageView.as_view()),

	url(r'^download/$', 'mycleancity.views.download_file'),
)

handler404 = 'mycleancity.views.error404'
handler500 = 'mycleancity.views.error404'

if settings.DEBUG:
	urlpatterns += patterns('django.contrib.staticfiles.views',
		url(r'^static/(?P<path>.*)$', 'serve'),
	)