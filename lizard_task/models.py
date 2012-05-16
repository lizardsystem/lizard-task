# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.db import models

from celery.execute import send_task
from django.utils import simplejson as json
from django.db import models
from django.core.urlresolvers import reverse

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


class SecuredPeriodicTask(PeriodicTask):
    """
    Adds data_set to PeriodicTask to provide security.
    """
    objects = FilteredManager()
    data_set = models.ForeignKey(DataSet, null=True, blank=True)
    staff_only = models.BooleanField(default=True)

    class Meta:
        ordering = ('name', )

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

    def latest_taskexecution(self):
        return self.taskexecution_set.latest()

    def send_task(self, username=None):
        args_params = json.loads(self.args)
        kwargs_params = json.loads(self.kwargs)
        kwargs_params["username"] = username or '-'
        result = send_task(self.task, args=args_params, kwargs=kwargs_params)

    def get_absolute_url(self):
        return reverse('lizard_task_detail', kwargs={'task_id': self.id})


class TaskExecution(models.Model):
    """
    Keep track of executions of a SecuredPeriodicTask.
    """
    task = models.ForeignKey(SecuredPeriodicTask,
                             null=True, blank=True)
    task_uuid = models.CharField(max_length=255, unique=True)
    started_by = models.CharField(max_length=128, null=True, blank=True)
    dt_start = models.DateTimeField(auto_now_add=True)
    dt_finish = models.DateTimeField(null=True,
                                     blank=True)
    #supports_object_permissions = True
    objects = FilteredManager()
    data_set = models.ForeignKey(DataSet, null=True, blank=True,
                                 related_name="taskexecution_data_set")

    class Meta:
        get_latest_by = "dt_start"

    def __unicode__(self):
        return "%s %s" % (self.task or '-', self.id)

    def task_state(self):
        return TaskState.objects.get(task_id=self.task_uuid)

    def get_absolute_url(self):
        return reverse('lizard_task_execution_detail', kwargs={
                'task_execution_id': self.id})


class TaskLogging(models.Model):
    """
    Gets filled by the DBLoggingHandler
    """
    task_execution = models.ForeignKey(TaskExecution)
    time = models.DateTimeField(blank=True, null=True)
    level = models.IntegerField(
        choices=LOGGING_LEVELS,
        blank=True,
        null=True)
    message = models.CharField(max_length=256)
    supports_object_permissions = True
    objects = FilteredManager()
    data_set = models.ForeignKey(DataSet, null=True, blank=True)

    class Meta:
        get_latest_by = "time"
        ordering = ('time', )

    def __unicode__(self):
        return '%s: %s' % (str(self.time), self.message)
