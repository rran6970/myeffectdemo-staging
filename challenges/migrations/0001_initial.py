# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChallengeQRCode'
        db.create_table(u'challenges_challengeqrcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.CharField')(default='', max_length=200, null=True, blank=True)),
            ('qr_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('qr_image_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('qr_image_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'challenges', ['ChallengeQRCode'])

        # Adding model 'ChallengeType'
        db.create_table(u'challenges_challengetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('challenge_type', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
        ))
        db.send_create_signal(u'challenges', ['ChallengeType'])

        # Adding model 'Challenge'
        db.create_table(u'challenges_challenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('event_start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('event_start_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('event_end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('event_end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('clean_team', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['cleanteams.CleanTeam'], null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('last_updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_last_updated_by', to=orm['auth.User'])),
            ('clean_creds_per_hour', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('national_challenge', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['challenges.ChallengeType'], null=True, blank=True)),
            ('qr_code', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.ChallengeQRCode'], unique=True, null=True, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('promote_top', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('clean_team_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('contact_first_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('contact_last_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('contact_email', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'challenges', ['Challenge'])

        # Adding model 'UserChallenge'
        db.create_table(u'challenges_userchallenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.Challenge'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('time_in', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('time_out', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('total_hours', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=11, decimal_places=2)),
            ('total_clean_creds', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=11, decimal_places=2)),
        ))
        db.send_create_signal(u'challenges', ['UserChallenge'])

        # Adding model 'CleanTeamChallenge'
        db.create_table(u'challenges_cleanteamchallenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.Challenge'])),
            ('clean_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeam'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('time_in', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('time_out', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('total_hours', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=11, decimal_places=2)),
            ('total_clean_creds', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=11, decimal_places=2)),
        ))
        db.send_create_signal(u'challenges', ['CleanTeamChallenge'])

        # Adding model 'StaplesStores'
        db.create_table(u'challenges_staplesstores', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store_no', self.gf('django.db.models.fields.IntegerField')(default=0, unique=True)),
            ('district', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('store_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('gm', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'challenges', ['StaplesStores'])

        # Adding model 'StaplesChallenge'
        db.create_table(u'challenges_stapleschallenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.Challenge'], null=True, blank=True)),
            ('clean_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeam'], null=True, blank=True)),
            ('staples_store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.StaplesStores'], null=True, blank=True)),
        ))
        db.send_create_signal(u'challenges', ['StaplesChallenge'])

        # Adding model 'Voucher'
        db.create_table(u'challenges_voucher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.Challenge'], null=True, blank=True)),
            ('clean_creds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('claims_allowed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('claims_made', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'challenges', ['Voucher'])

        # Adding model 'UserVoucher'
        db.create_table(u'challenges_uservoucher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.Voucher'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'challenges', ['UserVoucher'])

        # Adding model 'CleanGrid'
        db.create_table(u'challenges_cleangrid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='None', max_length=60)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6)),
        ))
        db.send_create_signal(u'challenges', ['CleanGrid'])

        # Adding model 'ChallengeQuestionType'
        db.create_table(u'challenges_challengequestiontype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='None', unique=True, max_length=60)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'challenges', ['ChallengeQuestionType'])

        # Adding model 'AnswerType'
        db.create_table(u'challenges_answertype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='None', unique=True, max_length=60)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'challenges', ['AnswerType'])

        # Adding model 'ChallengeQuestion'
        db.create_table(u'challenges_challengequestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('question', self.gf('django.db.models.fields.TextField')(default='None')),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['challenges.ChallengeQuestionType'], blank=True)),
            ('answer_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['challenges.AnswerType'], blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'challenges', ['ChallengeQuestion'])

        # Adding model 'QuestionAnswer'
        db.create_table(u'challenges_questionanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.ChallengeQuestion'])),
            ('answer_number', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
            ('answer', self.gf('django.db.models.fields.CharField')(default='None', max_length=60)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('clean_grid', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['challenges.CleanGrid'], null=True, blank=True)),
        ))
        db.send_create_signal(u'challenges', ['QuestionAnswer'])

        # Adding model 'UserChallengeSurvey'
        db.create_table(u'challenges_userchallengesurvey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('clean_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cleanteams.CleanTeam'])),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.Challenge'])),
            ('total_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'challenges', ['UserChallengeSurvey'])

        # Adding model 'UserChallengeSurveyAnswers'
        db.create_table(u'challenges_userchallengesurveyanswers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.UserChallengeSurvey'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.QuestionAnswer'])),
        ))
        db.send_create_signal(u'challenges', ['UserChallengeSurveyAnswers'])


    def backwards(self, orm):
        # Deleting model 'ChallengeQRCode'
        db.delete_table(u'challenges_challengeqrcode')

        # Deleting model 'ChallengeType'
        db.delete_table(u'challenges_challengetype')

        # Deleting model 'Challenge'
        db.delete_table(u'challenges_challenge')

        # Deleting model 'UserChallenge'
        db.delete_table(u'challenges_userchallenge')

        # Deleting model 'CleanTeamChallenge'
        db.delete_table(u'challenges_cleanteamchallenge')

        # Deleting model 'StaplesStores'
        db.delete_table(u'challenges_staplesstores')

        # Deleting model 'StaplesChallenge'
        db.delete_table(u'challenges_stapleschallenge')

        # Deleting model 'Voucher'
        db.delete_table(u'challenges_voucher')

        # Deleting model 'UserVoucher'
        db.delete_table(u'challenges_uservoucher')

        # Deleting model 'CleanGrid'
        db.delete_table(u'challenges_cleangrid')

        # Deleting model 'ChallengeQuestionType'
        db.delete_table(u'challenges_challengequestiontype')

        # Deleting model 'AnswerType'
        db.delete_table(u'challenges_answertype')

        # Deleting model 'ChallengeQuestion'
        db.delete_table(u'challenges_challengequestion')

        # Deleting model 'QuestionAnswer'
        db.delete_table(u'challenges_questionanswer')

        # Deleting model 'UserChallengeSurvey'
        db.delete_table(u'challenges_userchallengesurvey')

        # Deleting model 'UserChallengeSurveyAnswers'
        db.delete_table(u'challenges_userchallengesurveyanswers')


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
        u'challenges.answertype': {
            'Meta': {'object_name': 'AnswerType'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'None'", 'unique': 'True', 'max_length': '60'})
        },
        u'challenges.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'clean_creds_per_hour': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['cleanteams.CleanTeam']", 'null': 'True', 'blank': 'True'}),
            'clean_team_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'contact_first_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'contact_last_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'event_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event_end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event_start_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_last_updated_by'", 'to': u"orm['auth.User']"}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'national_challenge': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'promote_top': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'qr_code': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['challenges.ChallengeQRCode']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['challenges.ChallengeType']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'challenges.challengeqrcode': {
            'Meta': {'object_name': 'ChallengeQRCode'},
            'data': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qr_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qr_image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qr_image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'challenges.challengequestion': {
            'Meta': {'object_name': 'ChallengeQuestion'},
            'answer_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['challenges.AnswerType']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'default': "'None'"}),
            'question_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['challenges.ChallengeQuestionType']", 'blank': 'True'})
        },
        u'challenges.challengequestiontype': {
            'Meta': {'object_name': 'ChallengeQuestionType'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'None'", 'unique': 'True', 'max_length': '60'})
        },
        u'challenges.challengetype': {
            'Meta': {'object_name': 'ChallengeType'},
            'challenge_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'challenges.cleangrid': {
            'Meta': {'object_name': 'CleanGrid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '60'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'})
        },
        u'challenges.cleanteamchallenge': {
            'Meta': {'object_name': 'CleanTeamChallenge'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_in': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'total_clean_creds': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '2'}),
            'total_hours': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '2'})
        },
        u'challenges.questionanswer': {
            'Meta': {'object_name': 'QuestionAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '60'}),
            'answer_number': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'clean_grid': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['challenges.CleanGrid']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.ChallengeQuestion']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'challenges.stapleschallenge': {
            'Meta': {'object_name': 'StaplesChallenge'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']", 'null': 'True', 'blank': 'True'}),
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staples_store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.StaplesStores']", 'null': 'True', 'blank': 'True'})
        },
        u'challenges.staplesstores': {
            'Meta': {'object_name': 'StaplesStores'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'district': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'gm': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'store_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'store_no': ('django.db.models.fields.IntegerField', [], {'default': '0', 'unique': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'challenges.userchallenge': {
            'Meta': {'object_name': 'UserChallenge'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_in': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'total_clean_creds': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '2'}),
            'total_hours': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'challenges.userchallengesurvey': {
            'Meta': {'object_name': 'UserChallengeSurvey'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'challenges.userchallengesurveyanswers': {
            'Meta': {'object_name': 'UserChallengeSurveyAnswers'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.QuestionAnswer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.UserChallengeSurvey']"})
        },
        u'challenges.uservoucher': {
            'Meta': {'object_name': 'UserVoucher'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'voucher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Voucher']", 'null': 'True', 'blank': 'True'})
        },
        u'challenges.voucher': {
            'Meta': {'object_name': 'Voucher'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']", 'null': 'True', 'blank': 'True'}),
            'claims_allowed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'claims_made': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'clean_creds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'voucher': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
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

    complete_apps = ['challenges']