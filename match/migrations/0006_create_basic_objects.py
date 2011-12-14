# encoding: utf-8
import datetime, random
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.contrib.auth.models import User

towers = ('low_red', 'high_red', 'low_blue', 'high_blue', 'center')

all_teams = [ \
    {'number': 1, 'name': 'ITR', 'school': 'Illinois Institute of Technology', \
        'location':'Chicago, IL', 'sponsors': 'Noone', 'av_name': 'Penguin', 'gv_name': 'Shooter'},
    {'number': 2, 'name': 'Oakland', 'school': 'Oakland University', 'location': 'Rochester, MI', \
        'sponsors': 'Blaah', 'av_name': 'Foamy', 'gv_name': 'Spot'},
    {'number': 3, 'name': 'Pacers', 'school': 'Pace University', 'location': 'New York, NY', \
        'sponsors': 'Wooot', 'av_name': 'Pink', 'gv_name': 'Pacey'},
    {'number': 4, 'name': 'Cheesers', 'school': 'University of Wisconsin Platteville', \
        'location': 'Platteville, WI', 'sponsors': 'Packers, Cheese Castle', \
        'av_name': 'Sharp', 'gv_name': 'Chedder'},
    {'number': 12, 'name': 'GO FIRST', 'school': 'University of Minnesota', \
        'location': 'Minneapolis, MN', 'sponsors': 'Baxster', 'av_name': 'Tubes', \
        'gv_name': 'Spinner'},
    {'number': 14, 'name': 'MSOE', 'school': 'Milwaukee School of Engineering', \
        'location': 'Milwaukee School of Engineering', 'sponsors': 'Brewers', \
        'av_name': 'Flopper', 'gv_name': 'Beery'},
    {'number': 20, 'name': 'UIUC', 'school': 'University of Illinois at Urbana Champaign', \
        'location': 'Champaign, IL', 'sponsors': 'Corn', 'av_name': 'Agro', \
        'gv_name': 'Corny'},
    {'number': 24, 'name': 'Flyers', 'school': 'Embry-Riddle Aeronautical University', \
        'location': 'Daytona Beach, FL', 'sponsors': 'FAA', 'av_name': 'Just us', \
        'gv_name': 'What is a ground vehicle?'},
]


class Migration(DataMigration):

    def forwards(self, orm):
        if not db.dry_run:
            users = User.objects.all()
            i = 0
            for tower in towers:
                t = orm['match.Tower'](name=tower)
                t.save()
                tl = orm['match.TowerLevel'](tower=t, level=1, lighting_controller_id=0, state='off')
                tl.save()
                if 'high_' in tower or tower=='center':
                    tl = orm['match.TowerLevel'](tower=t, level=2, lighting_controller_id=0, \
                            state='off')
                    tl.save()
                try:
                    user = users[i]
                    i += 1
                    orm['match.ScoringDevice'](scorer=user, tower=t)
                except: pass


            db_teams = []
            for team in all_teams:
                t = orm['tournament.Team'](number=team['number'], name=team['name'], \
                        school=team['school'], location=team['location'], sponsors=team['sponsors'], \
                        av_name=team['av_name'], gv_name=team['gv_name'])
                t.save()
                db_teams.append(t)

            start = datetime.datetime.now()
            matches = []
            for i in range(1, 13):
                start += datetime.timedelta(minutes=8)
                teams = random.sample(db_teams, 4)
                match = orm['match.Match'](is_practice=True, time=start, \
                    red_1=teams[0], red_2=teams[1], blue_1=teams[2], blue_2=teams[3], \
                    red_1_gv_present=True, red_1_av_present=True, \
                    red_2_gv_present=True, red_2_av_present=True, \
                    blue_1_gv_present=True, blue_1_av_present=True, \
                    blue_2_gv_present=True, blue_2_av_present=True)
                match.save()
                matches.append(match)

            ss = orm['match.ScoringSystem'](current_match=matches[0])
            ss.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        if not db.dry_run:
            orm['match.Tower'].objects.all().delete()
            orm['match.TowerLevel'].objects.all().delete()
            orm['match.ScoringDevice'].objects.all().delete()
            orm['tournament.Team'].objects.all().delete()
            orm['match.Match'].objects.all().delete()
            orm['match.ScoringSystem'].objects.all().delete()


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
            'blue_center_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'red_center_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'red_penalties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'red_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'red_score_pre_penalty': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'scorer_high_blue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scoring_high_blue'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'scorer_high_red': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scoring_high_red'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'scorer_low_blue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scoring_low_blue'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'scorer_low_red': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scoring_low_red'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'match.matchevent': {
            'Meta': {'object_name': 'MatchEvent'},
            'alliance': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
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
            'on_center': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scorer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'tower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['match.Tower']"})
        },
        'match.scoringsystem': {
            'Meta': {'object_name': 'ScoringSystem'},
            'current_match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['match.Match']"}),
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
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sponsors': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['match']
