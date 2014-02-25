import csv

from django.core.mail import EmailMessage

from django.http import HttpResponse

from django.template import Context, RequestContext
from django.template.loader import get_template

from time import time

def get_upload_file_name(instance, filename):
    return "%s" % (filename)

def export_as_csv_action(description="Export selected as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode("utf-8","replace") for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv


class SendEmail(object):
    
    def send(self, template, content, subject, from_email, to):
        render_content = template.render(content)

        try:
            mail = EmailMessage(subject, render_content, from_email, [to])
            mail.content_subtype = "html"
            mail.send()
        except Exception, e:
            print e