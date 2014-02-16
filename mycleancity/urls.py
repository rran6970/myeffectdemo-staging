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

	url(r'^coming-soon/', TemplateView.as_view(template_name="mycleancity/coming_soon.html")),
	url(r'^register-success/?', RegisterSuccessView.as_view()),
	url(r'^register/(?P<qrcode>\w+)/?$', RegisterView.as_view()),
	url(r'^register/?$', RegisterView.as_view()),
	url(r'^register-invite/(?P<token>\w+)/?$', RegisterInviteView.as_view()),
	url(r'^landing/?', PrelaunchView.as_view()),

	url(r'^about/fr/?', TemplateView.as_view(template_name="mycleancity/french/about_fr.html")),
	url(r'^about/?', TemplateView.as_view(template_name="mycleancity/about.html")),

	url(r'^students/fr/?', TemplateView.as_view(template_name="mycleancity/french/students_fr.html")),
	url(r'^students/?', TemplateView.as_view(template_name="mycleancity/students.html")),

	url(r'^rewards/fr/?', TemplateView.as_view(template_name="mycleancity/french/rewards_fr.html")),
	url(r'^rewards/?', TemplateView.as_view(template_name="mycleancity/rewards.html")),

	url(r'^organizations/fr/?', TemplateView.as_view(template_name="mycleancity/french/organizations_fr.html")),
	url(r'^organizations/?', TemplateView.as_view(template_name="mycleancity/organizations.html")),

	url(r'^communication-hub/fr?', TemplateView.as_view(template_name="mycleancity/french/communication_hub_fr.html")),
	url(r'^media-hub/fr?', TemplateView.as_view(template_name="mycleancity/french/communication_hub_fr.html")),
	url(r'^communication-hub/?', TemplateView.as_view(template_name="mycleancity/communication_hub.html")),
	url(r'^media-hub/?', TemplateView.as_view(template_name="mycleancity/communication_hub.html")),

	url(r'^contact/?', ContactPageView.as_view()),
	
	url(r'^fr/$', TemplateView.as_view(template_name="mycleancity/french/index_fr.html")),
	url(r'^$', TemplateView.as_view(template_name="mycleancity/index.html")),

	url(r'^download/$', 'mycleancity.views.download_file'),
)

handler404 = 'mycleancity.views.error404'
handler500 = 'mycleancity.views.error404'

if settings.DEBUG:
	urlpatterns += patterns('django.contrib.staticfiles.views',
		url(r'^static/(?P<path>.*)$', 'serve'),
	)