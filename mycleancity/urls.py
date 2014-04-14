from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

from mycleancity.views import *
from api.views import *
from users.views import *
from userorganization.views import *
from challenges.views import *

admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^su/(?P<username>.*)/$', 'mycleancity.views.su', {'redirect_url': '/'}),
	(r'^suexit/$', 'mycleancity.views.su_exit', {'redirect_url': '/admin/'}),

	url(r'^captcha/', include('captcha.urls')),
	
	url(r'^users/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'users.views.reset_confirm', name='reset_confirm'),
	url(r'^users/reset-sent/$', TemplateView.as_view(template_name="users/password_reset_sent.html")),
	# url(r'^users/password_reset/$', 'users.views.reset', name='password_reset'),
	
	url(r'^users/reset/$', 'users.views.password_reset', {'post_reset_redirect' : '/users/reset-sent/', 'template_name' : 'users/password_reset_form.html', 'email_template_name' : 'emails/reset_email.html'}, name="password_reset"),

	url(r'^clean-team/', include('cleanteams.urls')),
	url(r'^challenges/', include('challenges.urls')),
	url(r'^cleancreds/', include('cleancreds.urls')),
	url(r'^notifications/', include('notifications.urls')),
	url(r'^users/', include('users.urls', namespace="users")),

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
	
	#webservices
	url(r'^api/webservices/login/$', 'api.api.login_user'),
    url(r'^api/webservices/register/$', "api.api.registration"),
	url(r'^api/webservices/studenteditprofile/$', "api.api.student_edit_profile"),
	url(r'^api/webservices/updateuser/$', "api.api.update_user"),
	url(r'^api/webservices/listchallenge/$', "api.api.list_challenge"),
	url(r'^api/webservices/listparticipants/$', "api.api.list_participants"),
	url(r'^api/webservices/addcleanteam/$', "api.api.add_cleanteam"),
	url(r'^api/webservices/listteam/$', "api.api.list_team"),
	url(r'^api/webservices/jointeam/$', "api.api.join_team"),
	url(r'^api/webservices/inviteuser/$', "api.api.invite_user"),
	url(r'^api/webservices/pendinglist/$', "api.api.pending_list"),
	url(r'^api/webservices/approvedlist/$', "api.api.approved_list"),
	url(r'^api/webservices/joinchampionteam/$', "api.api.joinchampion_team"),
	url(r'^api/webservices/listnotification/$', "api.api.list_notification"),
	url(r'^api/webservices/countnotification/$', "api.api.count_notification"),
	url(r'^api/webservices/uploadpicture/$', "api.api.upload_picture"),
	url(r'^api/webservices/viewparticipants/$', "api.api.view_participants"),
	url(r'^api/webservices/qrcodeuserchallenge/$', "api.api.qrcode_userchallenge"),
	url(r'^api/webservices/mychallenge/$', "api.api.my_challenge"),
	url(r'^api/webservices/checkin/$', "api.api.check_in"),
	url(r'^api/webservices/checkout/$', "api.api.check_out"),
	url(r'^api/webservices/search/$', "api.api.search"),
	url(r'^api/webservices/makemeread/$', "api.api.make_me_read"),
	url(r'^api/webservices/participatechallenge/$', "api.api.participate_challenge"),
	url(r'^api/webservices/onetimech/$', "api.api.onetime_ch"),
	url(r'^api/webservices/newsfeeds/$', "api.api.newsfeeds"),
	url(r'^api/webservices/cleanteamview/$', "api.api.cleanteam_view"),
	url(r'^api/webservices/teamchallenge/$', "api.api.team_challenge"),
	)

handler404 = 'mycleancity.views.error404'
handler500 = 'mycleancity.views.error404'

if settings.DEBUG:
	urlpatterns += patterns('django.contrib.staticfiles.views',
		url(r'^static/(?P<path>.*)$', 'serve'),
	)