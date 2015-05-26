import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404

from django.utils.timezone import utc

from django.views.generic import *
from django.views.generic.base import View

from mycleancity.mixins import LoginRequiredMixin

from notifications.models import UserNotification

class NotificationsFeedView(TemplateView):
	template_name = "notifications/notifications_feed.html"

	def get_context_data(self, **kwargs):
		context = super(NotificationsFeedView, self).get_context_data(**kwargs)
		context['notifications'] = UserNotification.objects.filter(user=self.request.user).order_by('-timestamp')
		context['user'] = self.request.user

		return context

def read_all_notifications(request):
	user_notifications = UserNotification.objects.filter(user=request.user)

	for n in user_notifications:
		n.read_notification()
			
	return HttpResponseRedirect('/notifications/')

def read_notification(request):
	if 'unread' in request.POST:
		return unread_notification(request) ## Really ugly, find how to hook the nav bar notification control to a glloal function then redirect to read_notificaion or unread_notification according to post['read'] and post['unread']
		

	
	if request.method == 'POST' and request.is_ajax:
			nids = request.POST.getlist('nid')
			 
			for nid in nids:
				 
				user_notification = UserNotification.objects.get(id=nid, user=request.user)
				user_notification.read_notification()
			
	return HttpResponseRedirect('/notifications/')

def unread_notification(request):
	if request.method == 'POST' and request.is_ajax:
			nids = request.POST.getlist('nid')
			
			for nid in nids:
				user_notification = UserNotification.objects.get(id=int(nid), user=request.user)
				user_notification.unread_notification()
			
	return HttpResponseRedirect('/notifications/')
