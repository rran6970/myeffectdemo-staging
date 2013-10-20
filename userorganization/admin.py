from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template import Context, RequestContext
from django.template.loader import get_template

from userorganization.models import *

class UserOrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'organization', 'city', 'postal_code', 'country')
    search_fields = ['user__id', 'user__first_name', 'user__last_name', 'province']
    actions = ['approved_organization']

    def approved_organization(self, request, queryset):
		for row in queryset:
			row.user.is_active = True
			row.user.save()

			plaintext = get_template('emails/organization_approval_success.txt')
			htmly = get_template('emails/organization_approval_success.html')

			d = Context({ 'first_name': row.user.first_name })

			subject, from_email, to = 'My Clean City - Approval Successful', 'info@mycleancity.org', row.user.email
			text_content = plaintext.render(d)
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()

admin.site.register(UserOrganization, UserOrganizationAdmin)