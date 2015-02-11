# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OrgProfile'
        db.create_table(u'cleanteams_orgprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('org_type', self.gf('django.db.models.fields.CharField')(default='other', max_length=30)),
            ('registered_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(default='General', max_length=60)),
            ('number_of_users', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True)),
        ))
        db.send_create_signal(u'cleanteams', ['OrgProfile'])

        # Adding model 'CleanTeamLevel'
        db.create_table(u'cleanteams_cleanteamlevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Seedling', max_length=30)),
            ('badge', self.gf('django.db.models.fields.CharField')(default='images/badge-level-1-75x63.png', max_length=100)),
            ('tree_level', self.gf('django.db.models.fields.CharField')(default='images/clean-team-tree-stage-1.png', max_length=100)),
            ('next_level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeamLevel'], null=True, blank=True)),
        ))
        db.send_create_signal(u'cleanteams', ['CleanTeamLevel'])

        # Adding model 'CleanTeam'
        db.create_table(u'cleanteams_cleanteam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(default='', max_length=200, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, null=True, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('facebook', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('instagram', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('clean_creds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeamLevel'], null=True, blank=True)),
            ('admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('org_profile', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cleanteams.OrgProfile'], unique=True, null=True, blank=True)),
            ('contact_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal(u'cleanteams', ['CleanTeam'])

        # Adding model 'CleanChampion'
        db.create_table(u'cleanteams_cleanchampion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('clean_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeam'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='approved', max_length=30)),
        ))
        db.send_create_signal(u'cleanteams', ['CleanChampion'])

        # Adding model 'CleanTeamMember'
        db.create_table(u'cleanteams_cleanteammember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('clean_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeam'])),
            ('role', self.gf('django.db.models.fields.CharField')(default='leader', max_length=30)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=30)),
        ))
        db.send_create_signal(u'cleanteams', ['CleanTeamMember'])

        # Adding model 'CleanTeamPost'
        db.create_table(u'cleanteams_cleanteampost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clean_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeam'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal(u'cleanteams', ['CleanTeamPost'])

        # Adding model 'CleanTeamInvite'
        db.create_table(u'cleanteams_cleanteaminvite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=70, blank=True)),
            ('clean_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeam'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(default='agent', max_length=30)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=30)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'cleanteams', ['CleanTeamInvite'])

        # Adding model 'CleanTeamLevelTask'
        db.create_table(u'cleanteams_cleanteamleveltask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clean_team_level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeamLevel'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=60)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('approval_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'cleanteams', ['CleanTeamLevelTask'])

        # Adding model 'CleanTeamLevelProgress'
        db.create_table(u'cleanteams_cleanteamlevelprogress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clean_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeam'])),
            ('level_task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeamLevelTask'])),
            ('approval_requested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'cleanteams', ['CleanTeamLevelProgress'])

        # Adding model 'LeaderReferral'
        db.create_table(u'cleanteams_leaderreferral', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('email', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('organization', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('clean_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeam'], null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=30)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal(u'cleanteams', ['LeaderReferral'])

        # Adding model 'CleanTeamPresentation'
        db.create_table(u'cleanteams_cleanteampresentation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('presentation', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('clean_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeam'], null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal(u'cleanteams', ['CleanTeamPresentation'])


    def backwards(self, orm):
        # Deleting model 'OrgProfile'
        db.delete_table(u'cleanteams_orgprofile')

        # Deleting model 'CleanTeamLevel'
        db.delete_table(u'cleanteams_cleanteamlevel')

        # Deleting model 'CleanTeam'
        db.delete_table(u'cleanteams_cleanteam')

        # Deleting model 'CleanChampion'
        db.delete_table(u'cleanteams_cleanchampion')

        # Deleting model 'CleanTeamMember'
        db.delete_table(u'cleanteams_cleanteammember')

        # Deleting model 'CleanTeamPost'
        db.delete_table(u'cleanteams_cleanteampost')

        # Deleting model 'CleanTeamInvite'
        db.delete_table(u'cleanteams_cleanteaminvite')

        # Deleting model 'CleanTeamLevelTask'
        db.delete_table(u'cleanteams_cleanteamleveltask')

        # Deleting model 'CleanTeamLevelProgress'
        db.delete_table(u'cleanteams_cleanteamlevelprogress')

        # Deleting model 'LeaderReferral'
        db.delete_table(u'cleanteams_leaderreferral')

        # Deleting model 'CleanTeamPresentation'
        db.delete_table(u'cleanteams_cleanteampresentation')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cleanteams']