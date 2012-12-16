# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Removing unique constraint on 'MatchEvent', fields ['match', 'microseconds']
        db.delete_unique('match_matchevent', ['match_id', 'microseconds'])

        # Adding field 'MatchEvent.collision_id'
        db.add_column('match_matchevent', 'collision_id', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        if not db.dry_run:
            i = 1
            for me in orm['match.MatchEvent'].objects.all():
                me.collision_id = i
                me.save()
                i += 1

        # Adding unique constraint on 'MatchEvent', fields ['collision_id', 'scorer']
        db.create_unique('match_matchevent', ['collision_id', 'scorer_id'])


    def backwards(self, orm):

        # Removing unique constraint on 'MatchEvent', fields ['collision_id', 'scorer']
        db.delete_unique('match_matchevent', ['collision_id', 'scorer_id'])

        # Deleting field 'MatchEvent.collision_id'
        db.delete_column('match_matchevent', 'collision_id')

        # Adding unique constraint on 'MatchEvent', fields ['match', 'microseconds']
        db.create_unique('match_matchevent', ['match_id', 'microseconds'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'match.match': {
            'Meta': {'object_name': 'Match'},
            'actual_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'blue_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'as_blue_1'", 'to': "orm['tournament.Team']"}),
            'blue_1_av_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blue_1_gv_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blue_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'as_blue_2'", 'to': "orm['tournament.Team']"}),
            'blue_2_av_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blue_2_gv_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blue_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blue_center_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blue_center_active_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'blue_penalties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blue_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blue_score_pre_penalty': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_practice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'red_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'as_red_1'", 'to': "orm['tournament.Team']"}),
            'red_1_av_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'red_1_gv_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'red_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'as_red_2'", 'to': "orm['tournament.Team']"}),
            'red_2_av_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'red_2_gv_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'red_bonus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'red_center_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'red_center_active_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'red_penalties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'red_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'red_score_pre_penalty': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'scorer_high_blue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scoring_high_blue'", 'null': 'True', 'to': "orm['auth.User']"}),
            'scorer_high_blue_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scorer_high_red': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scoring_high_red'", 'null': 'True', 'to': "orm['auth.User']"}),
            'scorer_high_red_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scorer_low_blue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scoring_low_blue'", 'null': 'True', 'to': "orm['auth.User']"}),
            'scorer_low_blue_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scorer_low_red': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scoring_low_red'", 'null': 'True', 'to': "orm['auth.User']"}),
            'scorer_low_red_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'match.matchevent': {
            'Meta': {'ordering': "['-id']", 'unique_together': "(('scorer', 'collision_id'),)", 'object_name': 'MatchEvent'},
            'alliance': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'collision_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['match.Match']"}),
            'microseconds': ('django.db.models.fields.BigIntegerField', [], {}),
            'scorer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'tower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['match.Tower']"})
        },
        'match.scoringdevice': {
            'Meta': {'object_name': 'ScoringDevice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_contact': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'on_center': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scorer': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'tower': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['match.Tower']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'match.scoringsystem': {
            'Meta': {'object_name': 'ScoringSystem'},
            'current_match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['match.Match']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'match.tower': {
            'Meta': {'object_name': 'Tower'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'})
        },
        'match.towerlevel': {
            'Meta': {'unique_together': "(('tower', 'level'),)", 'object_name': 'TowerLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'lighting_controller_id': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'tower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['match.Tower']"})
        },
        'tournament.team': {
            'Meta': {'object_name': 'Team'},
            'av_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'gv_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'have_av': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'have_gv': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'highest_match_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'match_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sponsors': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['match']
