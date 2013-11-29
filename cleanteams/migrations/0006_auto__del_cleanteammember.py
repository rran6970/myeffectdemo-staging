# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CleanTeamMember'
        db.delete_table(u'cleanteams_cleanteammember')


    def backwards(self, orm):
        # Adding model 'CleanTeamMember'
        db.create_table(u'cleanteams_cleanteammember', (
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=30)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cleam_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeam'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'cleanteams', ['CleanTeamMember'])


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