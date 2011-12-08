# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tower'
        db.create_table('match_tower', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=9)),
            ('alliance', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('match', ['Tower'])

        # Adding model 'TowerLevel'
        db.create_table('match_towerlevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
            ('lighting_controller_id', self.gf('django.db.models.fields.IntegerField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('match', ['TowerLevel'])

        # Adding model 'Match'
        db.create_table('match_match', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('actual_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('red_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='as_red_1', to=orm['tournament.Team'])),
            ('red_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='as_red_2', to=orm['tournament.Team'])),
            ('blue_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='as_blue_1', to=orm['tournament.Team'])),
            ('blue_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='as_blue_2', to=orm['tournament.Team'])),
            ('red_1_gv_present', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('red_1_av_present', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('red_2_gv_present', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('red_2_av_present', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('blue_1_gv_present', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('blue_1_av_present', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('blue_2_gv_present', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('blue_2_av_present', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('red_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('blue_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('red_score_pre_penalty', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('blue_score_pre_penalty', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('red_penalties', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('blue_penalties', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('scorer_low_red', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scoring_low_red', to=orm['auth.User'])),
            ('scorer_high_red', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scoring_high_red', to=orm['auth.User'])),
            ('scorer_low_blue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scoring_low_blue', to=orm['auth.User'])),
            ('scorer_high_blue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scoring_high_blue', to=orm['auth.User'])),
        ))
        db.send_create_signal('match', ['Match'])

        # Adding model 'MatchEvent'
        db.create_table('match_matchevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ts', self.gf('django.db.models.fields.IntegerField')()),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['match.Match'])),
            ('scorer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('team', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('tower', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['match.Tower'])),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('match', ['MatchEvent'])


    def backwards(self, orm):
        
        # Deleting model 'Tower'
        db.delete_table('match_tower')

        # Deleting model 'TowerLevel'
        db.delete_table('match_towerlevel')

        # Deleting model 'Match'
        db.delete_table('match_match')

        # Deleting model 'MatchEvent'
        db.delete_table('match_matchevent')


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
            'actual_start': ('django.db.models.fields.DateTimeField', [], {}),
            'blue_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'as_blue_1'", 'to': "orm['tournament.Team']"}),
            'blue_1_av_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blue_1_gv_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blue_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'as_blue_2'", 'to': "orm['tournament.Team']"}),
            'blue_2_av_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blue_2_gv_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blue_penalties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blue_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'blue_score_pre_penalty': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'red_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'as_red_1'", 'to': "orm['tournament.Team']"}),
            'red_1_av_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'red_1_gv_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'red_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'as_red_2'", 'to': "orm['tournament.Team']"}),
            'red_2_av_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'red_2_gv_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'red_penalties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'red_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'red_score_pre_penalty': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'scorer_high_blue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scoring_high_blue'", 'to': "orm['auth.User']"}),
            'scorer_high_red': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scoring_high_red'", 'to': "orm['auth.User']"}),
            'scorer_low_blue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scoring_low_blue'", 'to': "orm['auth.User']"}),
            'scorer_low_red': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scoring_low_red'", 'to': "orm['auth.User']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'match.matchevent': {
            'Meta': {'object_name': 'MatchEvent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['match.Match']"}),
            'scorer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'tower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['match.Tower']"}),
            'ts': ('django.db.models.fields.IntegerField', [], {})
        },
        'match.tower': {
            'Meta': {'object_name': 'Tower'},
            'alliance': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'})
        },
        'match.towerlevel': {
            'Meta': {'object_name': 'TowerLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'lighting_controller_id': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        'tournament.team': {
            'Meta': {'object_name': 'Team'},
            'av_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'gv_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'have_av': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'have_gv': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sponsors': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['match']
