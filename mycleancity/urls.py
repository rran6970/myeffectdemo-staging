from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
	# url(r'^$', 'mycleancity.views.index', name='home'),
    url(r'^$', TemplateView.as_view(template_name="index.html")),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^challenges/', include('challenges.urls')),
    url(r'^cleancreds/', include('cleancreds.urls')),
    url(r'^users/', include('users.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )