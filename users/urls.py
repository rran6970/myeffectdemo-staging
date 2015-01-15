from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from cleanteams.views import *
from userorganization.views import *
from users.views import *

urlpatterns = patterns('',
	url(r'^login/?', LoginPageView.as_view()),
	url(r'^auth/?', 'users.views.auth_view'),
	url(r'^logout/?', 'users.views.logout'),	
	url(r'^register_success/?', 'users.views.register_success'),

	url(r'^leaderboard/?$', LeaderboardView.as_view()),
    url(r'^leaderboard/fr/?', TemplateView.as_view(template_name="mycleancity/french/leaderboard_fr.html")),
    
    url(r'^follow-twitter/?$', 'users.views.follow_on_twitter'),
    url(r'^register/(?P<qrcode>\w+)/?$', RegisterView.as_view()),
    url(r'^register/?$', RegisterView.as_view()),
    url(r'^profile/(?P<uid>\d+)/?$', ProfilePublicView.as_view()),
    url(r'^profile/?$', ProfileView.as_view()),  
    url(r'^settings/?$', SettingsView.as_view()),  
    url(r'^qrcode/?$', QRCodeView.as_view()),  
    url(r'^printable-card/?$', PrintableCardView.as_view()),  

    url(r'^/?$', 'users.views.get_user_json'),
)