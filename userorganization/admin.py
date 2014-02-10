from django.contrib import admin
from django.core.mail import EmailMessage
from django.template import Context, RequestContext
from django.template.loader import get_template

from mycleancity.actions import export_as_csv_action

from userorganization.models import *

class UserOrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'organization', 'website')
    search_fields = ['user__id', 'user__first_name', 'user__last_name']
    actions = ['approved_organization', export_as_csv_action("CSV Export")]

    def approved_organization(self, request, queryset):
		for row in queryset:
			row.user.is_active = True
			row.user.save()

			template = get_template('emails/organization_approval_success.html')
			content = Context({ 'first_name': row.user.first_name })
			content = template.render(content)

			subject, from_email, to = 'My Clean City - Approval Successful', 'info@mycleancity.org', row.user.email

			mail = EmailMessage(subject, content, from_email, [to])
			mail.content_subtype = "html"
			mail.send()

# admin.site.register(UserOrganization, UserOrganizationAdmin)