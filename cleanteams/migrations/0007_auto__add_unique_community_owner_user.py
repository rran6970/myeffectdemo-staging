# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Community', fields ['owner_user']
        db.create_unique(u'cleanteams_community', ['owner_user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Community', fields ['owner_user']
        db.delete_unique(u'cleanteams_community', ['owner_user_id'])


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
        u'cleanteams.cleanchampion': {
            'Meta': {'object_name': 'CleanChampion'},
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'approved'", 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cleanteams.cleanteam': {
            'Meta': {'object_name': 'CleanTeam'},
            'about': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clean_creds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'contact_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeamLevel']", 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'org_profile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['cleanteams.OrgProfile']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'cleanteams.cleanteamfollow': {
            'Meta': {'object_name': 'CleanTeamFollow'},
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'cleanteams.cleanteaminvite': {
            'Meta': {'object_name': 'CleanTeamInvite'},
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '70', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'agent'", 'max_length': '30'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cleanteams.cleanteamlevel': {
            'Meta': {'object_name': 'CleanTeamLevel'},
            'badge': ('django.db.models.fields.CharField', [], {'default': "'images/badge-level-1-75x63.png'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Seedling'", 'max_length': '30'}),
            'next_level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeamLevel']", 'null': 'True', 'blank': 'True'}),
            'tree_level': ('django.db.models.fields.CharField', [], {'default': "'images/clean-team-tree-stage-1.png'", 'max_length': '100'})
        },
        u'cleanteams.cleanteamlevelprogress': {
            'Meta': {'object_name': 'CleanTeamLevelProgress'},
            'approval_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level_task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeamLevelTask']"})
        },
        u'cleanteams.cleanteamleveltask': {
            'Meta': {'object_name': 'CleanTeamLevelTask'},
            'approval_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clean_team_level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeamLevel']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '60'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        u'cleanteams.cleanteammember': {
            'Meta': {'object_name': 'CleanTeamMember'},
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'leader'", 'max_length': '30'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cleanteams.cleanteampost': {
            'Meta': {'object_name': 'CleanTeamPost'},
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cleanteams.cleanteampresentation': {
            'Meta': {'object_name': 'CleanTeamPresentation'},
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'presentation': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'cleanteams.community': {
            'Meta': {'object_name': 'Community'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '120'}),
            'owner_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'cleanteams.leaderreferral': {
            'Meta': {'object_name': 'LeaderReferral'},
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']", 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'organization': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'cleanteams.orgprofile': {
            'Meta': {'object_name': 'OrgProfile'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'General'", 'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_users': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'org_type': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '30'}),
            'registered_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True'})
        },
        u'cleanteams.teamcommunitymembership': {
            'Meta': {'object_name': 'TeamCommunityMembership'},
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']"}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.Community']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cleanteams.usercommunitymembership': {
            'Meta': {'object_name': 'UserCommunityMembership'},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.Community']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cleanteams']