# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PeriodicTaskExt'
        db.create_table('lizard_task_periodictaskext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.OneToOneField')(related_name='periodictaskext_task', unique=True, to=orm['djcelery.PeriodicTask'])),
            ('data_set', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='periodictaskext_data_set', null=True, to=orm['lizard_security.DataSet'])),
        ))
        db.send_create_signal('lizard_task', ['PeriodicTaskExt'])

        # Adding model 'TaskExecution'
        db.create_table('lizard_task_taskexecution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='taskexecution_task', to=orm['lizard_task.PeriodicTaskExt'])),
            ('started_by', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('dt_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('dt_finish', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('amount_updated', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('amount_created', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('amount_synchronized', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('amount_deactivated', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('amount_activated', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('configuration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('data_set', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='taskexecution_data_set', null=True, to=orm['lizard_security.DataSet'])),
        ))
        db.send_create_signal('lizard_task', ['TaskExecution'])

        # Adding model 'TaskLogging'
        db.create_table('lizard_task_tasklogging', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasklogging_task', to=orm['lizard_task.TaskExecution'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('level', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('data_set', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tasklogging_data_set', null=True, to=orm['lizard_security.DataSet'])),
        ))
        db.send_create_signal('lizard_task', ['TaskLogging'])


    def backwards(self, orm):
        
        # Deleting model 'PeriodicTaskExt'
        db.delete_table('lizard_task_periodictaskext')

        # Deleting model 'TaskExecution'
        db.delete_table('lizard_task_taskexecution')

        # Deleting model 'TaskLogging'
        db.delete_table('lizard_task_tasklogging')


    models = {
        'djcelery.crontabschedule': {
            'Meta': {'object_name': 'CrontabSchedule'},
            'day_of_week': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '64'}),
            'hour': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minute': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '64'})
        },
        'djcelery.intervalschedule': {
            'Meta': {'object_name': 'IntervalSchedule'},
            'every': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.CharField', [], {'max_length': '24'})
        },
        'djcelery.periodictask': {
            'Meta': {'object_name': 'PeriodicTask'},
            'args': ('django.db.models.fields.TextField', [], {'default': "'[]'", 'blank': 'True'}),
            'crontab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djcelery.CrontabSchedule']", 'null': 'True', 'blank': 'True'}),
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'exchange': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djcelery.IntervalSchedule']", 'null': 'True', 'blank': 'True'}),
            'kwargs': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            'last_run_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'queue': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'routing_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'total_run_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'lizard_security.dataset': {
            'Meta': {'ordering': "['name']", 'object_name': 'DataSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        'lizard_task.periodictaskext': {
            'Meta': {'object_name': 'PeriodicTaskExt'},
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'periodictaskext_data_set'", 'null': 'True', 'to': "orm['lizard_security.DataSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'periodictaskext_task'", 'unique': 'True', 'to': "orm['djcelery.PeriodicTask']"})
        },
        'lizard_task.taskexecution': {
            'Meta': {'object_name': 'TaskExecution'},
            'amount_activated': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'amount_created': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'amount_deactivated': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'amount_synchronized': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'amount_updated': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'configuration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taskexecution_data_set'", 'null': 'True', 'to': "orm['lizard_security.DataSet']"}),
            'dt_finish': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dt_start': ('django.db.models.fields.DateTimeField', [], {}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'started_by': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taskexecution_task'", 'to': "orm['lizard_task.PeriodicTaskExt']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'lizard_task.tasklogging': {
            'Meta': {'object_name': 'TaskLogging'},
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tasklogging_data_set'", 'null': 'True', 'to': "orm['lizard_security.DataSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasklogging_task'", 'to': "orm['lizard_task.TaskExecution']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lizard_task']
