# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ChallengeQuestion.question'
        db.alter_column(u'challenges_challengequestion', 'question', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'ChallengeQuestion.question'
        db.alter_column(u'challenges_challengequestion', 'question', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'challenges.category': {
            'Meta': {'object_name': 'Category'},
            'clean_cred_value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '60'})
        },
        u'challenges.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['cleanteams.CleanTeam']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'event_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'host_organization': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'challenges.challengecategory': {
            'Meta': {'object_name': 'ChallengeCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Category']"}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'challenges.challengequestion': {
            'Meta': {'object_name': 'ChallengeQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'default': "'None'"}),
            'question_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.ChallengeQuestionType']", 'blank': 'True'})
        },
        u'challenges.challengequestiontype': {
            'Meta': {'object_name': 'ChallengeQuestionType'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'None'", 'unique': 'True', 'max_length': '60'})
        },
        u'challenges.cleangrid': {
            'Meta': {'object_name': 'CleanGrid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '60'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'})
        },
        u'challenges.questionanswer': {
            'Meta': {'object_name': 'QuestionAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '60'}),
            'clean_grid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.CleanGrid']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.ChallengeQuestion']"}),
            'question_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        u'challenges.userchallenge': {
            'Meta': {'object_name': 'UserChallenge'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_in': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'total_hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cleanteams.cleanteam': {
            'Meta': {'object_name': 'CleanTeam'},
            'about': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'clean_creds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeamLevel']", 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'team_type': ('django.db.models.fields.CharField', [], {'default': "'Independent'", 'max_length': '60'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'})
        },
        u'cleanteams.cleanteamlevel': {
            'Meta': {'object_name': 'CleanTeamLevel'},
            'badge': ('django.db.models.fields.CharField', [], {'default': "'images/badge-level-1-75x63.png'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Seedling'", 'max_length': '30'}),
            'next_level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeamLevel']", 'null': 'True', 'blank': 'True'}),
            'tree_level': ('django.db.models.fields.CharField', [], {'default': "'images/clean-team-tree-stage-1.png'", 'max_length': '100'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['challenges']