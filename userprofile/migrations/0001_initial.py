# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserSettings'
        db.create_table(u'userprofile_usersettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True)),
            ('communication_language', self.gf('django.db.models.fields.CharField')(default='English', max_length=10)),
            ('receive_newsletters', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_privacy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('data_privacy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timezone', self.gf('timezone_field.fields.TimeZoneField')(default='America/Toronto')),
        ))
        db.send_create_signal(u'userprofile', ['UserSettings'])

        # Adding model 'QRCodeSignups'
        db.create_table(u'userprofile_qrcodesignups', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'userprofile', ['QRCodeSignups'])

        # Adding model 'UserQRCode'
        db.create_table(u'userprofile_userqrcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('data', self.gf('django.db.models.fields.CharField')(default='', max_length=60, null=True, blank=True)),
            ('qr_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('qr_image_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('qr_image_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'userprofile', ['UserQRCode'])

        # Adding model 'UserProfile'
        db.create_table(u'userprofile_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('emergency_contact_fname', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('emergency_contact_lname', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('clean_creds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('student_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('school_type', self.gf('django.db.models.fields.CharField')(default='High School', max_length=30, blank=True)),
            ('school_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.CharField')(default='17-21', max_length=30, blank=True)),
            ('smartphone', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('emergency_phone', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('clean_team_member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeamMember'], null=True, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, null=True, blank=True)),
            ('hear_about_us', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('settings', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['userprofile.UserSettings'], unique=True, null=True)),
            ('qr_code', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['userprofile.UserQRCode'], unique=True, null=True)),
            ('referral_token', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('phase', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
        ))
        db.send_create_signal(u'userprofile', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'UserSettings'
        db.delete_table(u'userprofile_usersettings')

        # Deleting model 'QRCodeSignups'
        db.delete_table(u'userprofile_qrcodesignups')

        # Deleting model 'UserQRCode'
        db.delete_table(u'userprofile_userqrcode')

        # Deleting model 'UserProfile'
        db.delete_table(u'userprofile_userprofile')


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
        u'cleanteams.cleanteamlevel': {
            'Meta': {'object_name': 'CleanTeamLevel'},
            'badge': ('django.db.models.fields.CharField', [], {'default': "'images/badge-level-1-75x63.png'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Seedling'", 'max_length': '30'}),
            'next_level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeamLevel']", 'null': 'True', 'blank': 'True'}),
            'tree_level': ('django.db.models.fields.CharField', [], {'default': "'images/clean-team-tree-stage-1.png'", 'max_length': '100'})
        },
        u'cleanteams.cleanteammember': {
            'Meta': {'object_name': 'CleanTeamMember'},
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'leader'", 'max_length': '30'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
        },
        u'userprofile.qrcodesignups': {
            'Meta': {'object_name': 'QRCodeSignups'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'userprofile.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.CharField', [], {'default': "'17-21'", 'max_length': '30', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'clean_creds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'clean_team_member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeamMember']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'emergency_contact_fname': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'emergency_contact_lname': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'emergency_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'hear_about_us': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phase': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'qr_code': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['userprofile.UserQRCode']", 'unique': 'True', 'null': 'True'}),
            'referral_token': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'school_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'school_type': ('django.db.models.fields.CharField', [], {'default': "'High School'", 'max_length': '30', 'blank': 'True'}),
            'settings': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['userprofile.UserSettings']", 'unique': 'True', 'null': 'True'}),
            'smartphone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        u'userprofile.userqrcode': {
            'Meta': {'object_name': 'UserQRCode'},
            'data': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qr_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qr_image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qr_image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'userprofile.usersettings': {
            'Meta': {'object_name': 'UserSettings'},
            'communication_language': ('django.db.models.fields.CharField', [], {'default': "'English'", 'max_length': '10'}),
            'data_privacy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_privacy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receive_newsletters': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'default': "'America/Toronto'"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['userprofile']