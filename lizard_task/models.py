# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.db import models

from celery.execute import send_task
from django.utils import simplejson as json
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
        """
        Fetch current associated task state.

        In order for this function to work, the task need a taskname
        provided.
        """
        try:
            task_uuid = TaskExecution.objects.filter(
                task=self).order_by('-dt_start')[0].task_uuid
            return TaskState.objects.get(task_id=task_uuid)
        except IndexError:
            return None

    def send_task(self, username=None):
        task = self.task
        args_params = json.loads(task.args)
        kwargs_params = json.loads(task.kwargs)
        kwargs_params["username"] = username or '-'
        print task.task, args_params, kwargs_params
        result = send_task(task.task, args=args_params, kwargs=kwargs_params)

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
        return "%s %s" % (self.task or '-', self.id)


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
