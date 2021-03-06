import csv
import datetime
import decimal

import sys,os

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.template.loader import get_template

from time import time

def hours_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")

    difference = d1 - d2
    difference_hours = (difference.days * 24) + (difference.seconds // 3600)
    difference_hours = (difference.days * 24) + (difference.seconds // 3600)

    return divmod(difference.days * 86400 + difference.seconds, 60)

def limiter(x, limit):
    for i in range(len(x)):
        if i >= limit:
            break
    return x[:i]

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

def current_site_url():
    """Returns fully qualified URL (no trailing slash) for the current site."""
    from django.contrib.sites.models import Site
    current_site = Site.objects.get_current()
    protocol = getattr(settings, 'MY_SITE_PROTOCOL', 'http')
    port     = getattr(settings, 'MY_SITE_PORT', '')
    url = '%s://%s' % (protocol, current_site.domain)
    if port:
        url += ':%s' % port
    return url

def django_root_url(fq=False):
    """Returns base URL (no trailing slash) for the current project.

    Setting fq parameter to a true value will prepend the base URL
    of the current site to create a fully qualified URL.

    The name django_root_url is used in favor of alternatives
    (such as project_url) because it corresponds to the mod_python
    PythonOption django.root setting used in Apache.
    """
    url = getattr(settings, 'MY_DJANGO_URL_PATH', '')
    if fq:
        url = current_site_url() + url
    return url

class SendEmail(object):
    
    def send(self, template, content, subject, from_email, to):
        render_content = template.render(content)

        try:
            mail = EmailMessage(subject, render_content, from_email, [to])
            mail.content_subtype = "html"
            mail.send()
        except Exception, e:
            print e

class UploadFileToS3(object):

    def upload(self, key, file):
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_BUCKET)
        k = Key(bucket)
        k.key = key
        k.set_contents_from_string(file.read())

        return k.key

#LOCAL_PATH= '/backup/S3'

#class DownloadFilefromS3(object):

  #  def download(self, key, file):
     #  conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
      # bucket = conn.get_bucket(settings.AWS_BUCKET)
       #bucket_list = bucket.list()
       #for l in bucket_list:
        #  keyString = str(l.key)
         # l.get_contents_to_filename(LOCAL_PATH+key)

    #return l.key

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
