# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'SecuredPeriodicTask.staff_only'
        db.add_column('lizard_task_securedperiodictask', 'staff_only', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'SecuredPeriodicTask.staff_only'
        db.delete_column('lizard_task_securedperiodictask', 'staff_only')


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
        'lizard_task.securedperiodictask': {
            'Meta': {'ordering': "('name',)", 'object_name': 'SecuredPeriodicTask', '_ormbases': ['djcelery.PeriodicTask']},
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_security.DataSet']", 'null': 'True', 'blank': 'True'}),
            'periodictask_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['djcelery.PeriodicTask']", 'unique': 'True', 'primary_key': 'True'}),
            'staff_only': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'lizard_task.taskexecution': {
            'Meta': {'object_name': 'TaskExecution'},
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taskexecution_data_set'", 'null': 'True', 'to': "orm['lizard_security.DataSet']"}),
            'dt_finish': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dt_start': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'started_by': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_task.SecuredPeriodicTask']", 'null': 'True', 'blank': 'True'}),
            'task_uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'lizard_task.tasklogging': {
            'Meta': {'ordering': "('time',)", 'object_name': 'TaskLogging'},
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_security.DataSet']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'task_execution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_task.TaskExecution']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lizard_task']
