# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Team'
        db.create_table('tournament_team', (
            ('number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sponsors', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('av_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('have_av', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('gv_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('have_gv', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('tournament', ['Team'])


    def backwards(self, orm):
        
        # Deleting model 'Team'
        db.delete_table('tournament_team')


    models = {
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

    complete_apps = ['tournament']
