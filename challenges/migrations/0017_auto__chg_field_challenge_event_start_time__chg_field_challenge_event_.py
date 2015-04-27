# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Challenge.event_start_time'
        db.alter_column(u'challenges_challenge', 'event_start_time', self.gf('django.db.models.fields.TimeField')())

        # Changing field 'Challenge.event_end_time'
        db.alter_column(u'challenges_challenge', 'event_end_time', self.gf('django.db.models.fields.TimeField')())

    def backwards(self, orm):

        # Changing field 'Challenge.event_start_time'
        db.alter_column(u'challenges_challenge', 'event_start_time', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Challenge.event_end_time'
        db.alter_column(u'challenges_challenge', 'event_end_time', self.gf('django.db.models.fields.TimeField')(null=True))

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
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'General'", 'max_length': '60'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'clean_creds_per_hour': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': u"orm['cleanteams.CleanTeam']", 'null': 'True', 'blank': 'True'}),
            'clean_team_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'contact_first_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'contact_last_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'event_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event_end_time': ('django.db.models.fields.TimeField', [], {'default': "'23:59:59'"}),
            'event_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event_start_time': ('django.db.models.fields.TimeField', [], {'default': "'0:00'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_last_updated_by'", 'to': u"orm['auth.User']"}),
            'limit': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'virtual_challenge': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'challenges.challengecommunitymembership': {
            'Meta': {'unique_together': "(('challenge', 'community'),)", 'object_name': 'ChallengeCommunityMembership'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.Community']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'challenges.challengeparticipant': {
            'Meta': {'object_name': 'ChallengeParticipant'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'receive_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
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
        u'challenges.challengeskilltag': {
            'Meta': {'object_name': 'ChallengeSkillTag'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skill_tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.SkillTag']"})
        },
        u'challenges.challengeteammembership': {
            'Meta': {'unique_together': "(('challenge', 'clean_team'),)", 'object_name': 'ChallengeTeamMembership'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'challenges.challengetype': {
            'Meta': {'object_name': 'ChallengeType'},
            'challenge_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'challenges.challengeuploadfile': {
            'Meta': {'object_name': 'ChallengeUploadFile'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
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
        u'challenges.skilltag': {
            'Meta': {'object_name': 'SkillTag'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.SkillTagCategory']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skill_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'challenges.skilltagcategory': {
            'Meta': {'object_name': 'SkillTagCategory'},
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        u'challenges.userchallengeevent': {
            'Meta': {'object_name': 'UserChallengeEvent'},
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
            'category': ('django.db.models.fields.CharField', [], {'default': "'General'", 'max_length': '60'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']", 'null': 'True', 'blank': 'True'}),
            'clean_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cleanteams.CleanTeam']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'challenges.userchallengesurveyanswers': {
            'Meta': {'object_name': 'UserChallengeSurveyAnswers'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.QuestionAnswer']", 'null': 'True', 'blank': 'True'}),
            'answerdetail': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
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
            'focus': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
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
        u'cleanteams.community': {
            'Meta': {'object_name': 'Community'},
            'about': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'General'", 'max_length': '60'}),
            'clean_creds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'contact_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contact_user'", 'to': u"orm['auth.User']"}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '120'}),
            'owner_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner_user'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'})
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