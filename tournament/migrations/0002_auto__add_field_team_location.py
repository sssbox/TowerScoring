# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Team.location'
        db.add_column('tournament_team', 'location', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Team.location'
        db.delete_column('tournament_team', 'location')


    models = {
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

    complete_apps = ['tournament']
