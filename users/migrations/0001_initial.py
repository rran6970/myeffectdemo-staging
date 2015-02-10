# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PrelaunchEmails'
        db.create_table(u'users_prelaunchemails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=70)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('school_type', self.gf('django.db.models.fields.CharField')(default='High School', max_length=30)),
            ('ambassador', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('join', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['PrelaunchEmails'])

        # Adding model 'ProfilePhase'
        db.create_table(u'users_profilephase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='One', max_length=30)),
            ('drop_level', self.gf('django.db.models.fields.CharField')(default='images/clean-team-tree-stage-1.png', max_length=100)),
            ('next_level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.ProfilePhase'], null=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['ProfilePhase'])

        # Adding model 'ProfileTask'
        db.create_table(u'users_profiletask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile_phase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.ProfilePhase'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=60)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('approval_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'users', ['ProfileTask'])

        # Adding model 'ProfileProgress'
        db.create_table(u'users_profileprogress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('phase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.ProfilePhase'])),
            ('profile_task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.ProfileTask'])),
            ('approval_requested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'users', ['ProfileProgress'])

        # Adding model 'OrganizationLicense'
        db.create_table(u'users_organizationlicense', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('is_charity', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('from_date', self.gf('django.db.models.fields.DateField')()),
            ('to_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'users', ['OrganizationLicense'])


    def backwards(self, orm):
        # Deleting model 'PrelaunchEmails'
        db.delete_table(u'users_prelaunchemails')

        # Deleting model 'ProfilePhase'
        db.delete_table(u'users_profilephase')

        # Deleting model 'ProfileTask'
        db.delete_table(u'users_profiletask')

        # Deleting model 'ProfileProgress'
        db.delete_table(u'users_profileprogress')

        # Deleting model 'OrganizationLicense'
        db.delete_table(u'users_organizationlicense')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'users.organizationlicense': {
            'Meta': {'object_name': 'OrganizationLicense'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_charity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'users.prelaunchemails': {
            'Meta': {'object_name': 'PrelaunchEmails'},
            'ambassador': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '70'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'school_type': ('django.db.models.fields.CharField', [], {'default': "'High School'", 'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'users.profilephase': {
            'Meta': {'object_name': 'ProfilePhase'},
            'drop_level': ('django.db.models.fields.CharField', [], {'default': "'images/clean-team-tree-stage-1.png'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'One'", 'max_length': '30'}),
            'next_level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.ProfilePhase']", 'null': 'True', 'blank': 'True'})
        },
        u'users.profileprogress': {
            'Meta': {'object_name': 'ProfileProgress'},
            'approval_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.ProfilePhase']"}),
            'profile_task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.ProfileTask']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'users.profiletask': {
            'Meta': {'object_name': 'ProfileTask'},
            'approval_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '60'}),
            'profile_phase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.ProfilePhase']"})
        }
    }

    complete_apps = ['users']