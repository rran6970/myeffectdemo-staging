# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from users.forms import RegisterUserForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
import json

class APIRegisterView(FormView):
        
	template_name = "users/register.html"
	form_class = RegisterUserForm
	success_url = "mycleancity/index.html"

	def get_initial(self):
		initial = {}
		initial['role'] = 'individual'

		return initial

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form

		return self.render_to_response(context)

	def form_valid(self, form):

                success = {'status':'false'}
                try:
                        u = User.objects.create_user(
                        #form.cleaned_data['email'],
                        #form.cleaned_data['email'],
                        #form.cleaned_data['password']
                        )
                        u.first_name = form.cleaned_data['first_name']
                        #u.last_name = form.cleaned_data['last_name']
                        #u.profile.city = form.cleaned_data['city']
                        #u.profile.province = form.cleaned_data['province']
                        #u.profile.school_type = form.cleaned_data['school_type']
                        #u.profile.save()
                        u.save()
                        success['status'] = 'true'
                except:
                        success['status'] = 'false'
		return HttpResponse(json.dumps(str(success)))


	def get_context_data(self, **kwargs):
		context = super(APIRegisterView, self).get_context_data(**kwargs)

		if 'qrcode' in self.kwargs:
			context['popup'] = True
	
		context['user'] = self.request.user

		return context

	
