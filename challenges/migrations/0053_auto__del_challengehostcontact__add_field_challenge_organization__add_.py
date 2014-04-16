# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ChallengeHostContact'
        db.delete_table(u'challenges_challengehostcontact')

        # Adding field 'Challenge.organization'
        db.add_column(u'challenges_challenge', 'organization',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=60),
                      keep_default=False)

        # Adding field 'Challenge.contact_first_name'
        db.add_column(u'challenges_challenge', 'contact_first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=60),
                      keep_default=False)

        # Adding field 'Challenge.contact_last_name'
        db.add_column(u'challenges_challenge', 'contact_last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=60),
                      keep_default=False)

        # Adding field 'Challenge.contact_phone'
        db.add_column(u'challenges_challenge', 'contact_phone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=15),
                      keep_default=False)

        # Adding field 'Challenge.contact_email'
        db.add_column(u'challenges_challenge', 'contact_email',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=60),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ChallengeHostContact'
        db.create_table(u'challenges_challengehostcontact', (
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.Challenge'])),
            ('orgnaization', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=60)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'challenges', ['ChallengeHostContact'])

        # Deleting field 'Challenge.organization'
        db.delete_column(u'challenges_challenge', 'organization')

        # Deleting field 'Challenge.contact_first_name'
        db.delete_column(u'challenges_challenge', 'contact_first_name')

        # Deleting field 'Challenge.contact_last_name'
        db.delete_column(u'challenges_challenge', 'contact_last_name')

        # Deleting field 'Challenge.contact_phone'
        db.delete_column(u'challenges_challenge', 'contact_phone')

        # Deleting field 'Challenge.contact_email'
        db.delete_column(u'challenges_challenge', 'contact_email')


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
        u'challenges.questionanswer': {
            'Meta': {'object_name': 'QuestionAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '60'}),
            'answer_number': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'clean_grid': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['challenges.CleanGrid']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.ChallengeQuestion']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'challenges.userchallenge': {
            'Meta': {'object_name': 'UserChallenge'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_in': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'total_clean_creds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']", 'null': 'True', 'blank': 'True'}),
            'clean_creds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'voucher': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        u'cleanteams.cleanteam': {
            'Meta': {'object_name': 'CleanTeam'},
            'about': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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