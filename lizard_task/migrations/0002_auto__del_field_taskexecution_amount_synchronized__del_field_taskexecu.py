# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'TaskExecution.amount_synchronized'
        db.delete_column('lizard_task_taskexecution', 'amount_synchronized')

        # Deleting field 'TaskExecution.amount_deactivated'
        db.delete_column('lizard_task_taskexecution', 'amount_deactivated')

        # Deleting field 'TaskExecution.host'
        db.delete_column('lizard_task_taskexecution', 'host')

        # Deleting field 'TaskExecution.amount_created'
        db.delete_column('lizard_task_taskexecution', 'amount_created')

        # Deleting field 'TaskExecution.configuration'
        db.delete_column('lizard_task_taskexecution', 'configuration')

        # Deleting field 'TaskExecution.amount_activated'
        db.delete_column('lizard_task_taskexecution', 'amount_activated')

        # Deleting field 'TaskExecution.amount_updated'
        db.delete_column('lizard_task_taskexecution', 'amount_updated')

        # Deleting field 'TaskExecution.url'
        db.delete_column('lizard_task_taskexecution', 'url')

        # Adding field 'TaskExecution.task_uuid'
        db.add_column('lizard_task_taskexecution', 'task_uuid', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True), keep_default=False)

        # Changing field 'TaskExecution.task'
        db.alter_column('lizard_task_taskexecution', 'task_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['lizard_task.PeriodicTaskExt']))


    def backwards(self, orm):
        
        # Adding field 'TaskExecution.amount_synchronized'
        db.add_column('lizard_task_taskexecution', 'amount_synchronized', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'TaskExecution.amount_deactivated'
        db.add_column('lizard_task_taskexecution', 'amount_deactivated', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'TaskExecution.host'
        db.add_column('lizard_task_taskexecution', 'host', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True), keep_default=False)

        # Adding field 'TaskExecution.amount_created'
        db.add_column('lizard_task_taskexecution', 'amount_created', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'TaskExecution.configuration'
        db.add_column('lizard_task_taskexecution', 'configuration', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'TaskExecution.amount_activated'
        db.add_column('lizard_task_taskexecution', 'amount_activated', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'TaskExecution.amount_updated'
        db.add_column('lizard_task_taskexecution', 'amount_updated', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'TaskExecution.url'
        db.add_column('lizard_task_taskexecution', 'url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True), keep_default=False)

        # Deleting field 'TaskExecution.task_uuid'
        db.delete_column('lizard_task_taskexecution', 'task_uuid')

        # Changing field 'TaskExecution.task'
        db.alter_column('lizard_task_taskexecution', 'task_id', self.gf('django.db.models.fields.related.ForeignKey')(default=datetime.date(2012, 5, 3), to=orm['lizard_task.PeriodicTaskExt']))


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
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taskexecution_data_set'", 'null': 'True', 'to': "orm['lizard_security.DataSet']"}),
            'dt_finish': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dt_start': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'started_by': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taskexecution_task'", 'null': 'True', 'to': "orm['lizard_task.PeriodicTaskExt']"}),
            'task_uuid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
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
