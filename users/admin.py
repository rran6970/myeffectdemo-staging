from django.contrib import admin
from django.contrib.sites.models import Site

from mycleancity.actions import export_as_csv_action

from users.models import *

class PrelaunchEmailsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'postal_code', 'school_type', 'ambassador', 'timestamp')
    search_fields = ['email', 'first_name', 'school_type']
    actions = [export_as_csv_action("CSV Export")]
    
admin.site.register(PrelaunchEmails, PrelaunchEmailsAdmin)
#admin.site.register(Site)