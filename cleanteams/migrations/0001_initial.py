# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CleanTeam'
        db.create_table(u'cleanteams_cleanteam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(default='http://', max_length=200)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, null=True, blank=True)),
            ('clean_creds', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'cleanteams', ['CleanTeam'])


    def backwards(self, orm):
        # Deleting model 'CleanTeam'
        db.delete_table(u'cleanteams_cleanteam')


    models = {
        u'cleanteams.cleanteam': {
            'Meta': {'object_name': 'CleanTeam'},
            'clean_creds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'default': "'http://'", 'max_length': '200'})
        }
    }

    complete_apps = ['cleanteams']