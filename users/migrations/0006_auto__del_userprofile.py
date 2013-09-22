# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'users_userprofile')


    def backwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'users_userprofile', (
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('clean_creds', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['UserProfile'])


    models = {
        u'users.prelaunchemails': {
            'Meta': {'object_name': 'PrelaunchEmails'},
            'ambassador': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '70'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'school_type': ('django.db.models.fields.CharField', [], {'default': "'High School'", 'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['users']