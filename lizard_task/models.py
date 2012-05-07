# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.db import models

# Create your models here.

from django.db import models

from lizard_security.models import DataSet
from lizard_security.manager import FilteredManager

from djcelery.models import PeriodicTask
from djcelery.models import TaskState


LOGGING_LEVELS = (
    (10, u'DEBUG'),
    (20, u'INFO'),
    (30, u'WARNING'),
    (40, u'ERROR'),
    (50, u'CRITICAL'),
)


class PeriodicTaskExt(models.Model):
    task = models.OneToOneField(PeriodicTask,
                                related_name="periodictaskext_task")
    supports_object_permissions = True
    objects = FilteredManager()
    data_set = models.ForeignKey(DataSet, null=True, blank=True,
                                 related_name="periodictaskext_data_set")

    def latest_state(self):
        state = None
        task_executions = TaskExecution.objects.filter(
                task=self).order_by('-dt_start')
        if task_executions.exists() == False:
            return state
        task_execution = task_executions[0]
        task_states = TaskState.objects.filter(task_id=task_execution.task_uuid)
        if task_states.exists() == False:
            return state
        return task_states[0]


    def __unicode__(self):
        return self.task.name


class TaskExecution(models.Model):
    """
    Jack: seems to me that this is the same as the list of Celery
    tasks.
    """
    task = models.ForeignKey(PeriodicTaskExt,
                             null=True,
                             related_name="taskexecution_task")
    task_uuid = models.CharField(max_length=255, unique=True)
    started_by = models.CharField(max_length=128, null=True, blank=True)
    dt_start = models.DateTimeField()
    dt_finish = models.DateTimeField(null=True,
                                     blank=True)
    supports_object_permissions = True
    objects = FilteredManager()
    data_set = models.ForeignKey(DataSet, null=True, blank=True,
                                 related_name="taskexecution_data_set")

    class Meta:
        get_latest_by = "dt_start"

    def __unicode__(self):
        return "%s %s" % (self.task.task.name, self.id)


class TaskLogging(models.Model):
    """
    Gets filled by the DBLoggingHandler
    """
    task = models.ForeignKey(TaskExecution,
                             related_name="tasklogging_task")
    time = models.DateTimeField(blank=True, null=True)
    level = models.IntegerField(
        choices=LOGGING_LEVELS,
        blank=True,
        null=True)
    message = models.CharField(max_length=256)
    supports_object_permissions = True
    objects = FilteredManager()
    data_set = models.ForeignKey(DataSet, null=True, blank=True,
                                 related_name="tasklogging_data_set")

    class Meta:
        get_latest_by = "time"
