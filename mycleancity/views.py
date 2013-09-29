from django.views.generic.base import TemplateView

def error404(request):
    return render(request,'mycleancity/404.html')

class HomePageView(TemplateView):
	template_name = "mycleancity/index.html"

	def get_context_data(self, **kwargs):
		context = super(HomePageView, self).get_context_data(**kwargs)
		return context

class AboutPageView(TemplateView):
	template_name = "mycleancity/about.html"

	def get_context_data(self, **kwargs):
		context = super(AboutPageView, self).get_context_data(**kwargs)
		return context

class ContactPageView(TemplateView):
	template_name = "mycleancity/contact.html"

	def get_context_data(self, **kwargs):
		context = super(ContactPageView, self).get_context_data(**kwargs)
		return context