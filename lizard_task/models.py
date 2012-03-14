# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.db import models

# Create your models here.

from django.db import models

from lizard_security.models import DataSet
from lizard_security.manager import FilteredManager

from djcelery.models import PeriodicTask


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

    def __unicode__(self):
        return self.task.name


class TaskExecution(models.Model):
    task = models.ForeignKey(PeriodicTaskExt,
                             related_name="taskexecution_task")
    started_by = models.CharField(max_length=128, null=True, blank=True)
    dt_start = models.DateTimeField()
    dt_finish = models.DateTimeField(null=True,
                                     blank=True)
    amount_updated = models.IntegerField(null=True,
                                         blank=True)
    amount_created = models.IntegerField(null=True,
                                         blank=True)
    amount_synchronized = models.IntegerField(null=True,
                                             blank=True)
    amount_deactivated = models.IntegerField(null=True,
                                             blank=True)
    amount_activated = models.IntegerField(null=True,
                                           blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    configuration = models.TextField(blank=True, null=True)
    supports_object_permissions = True
    objects = FilteredManager()
    data_set = models.ForeignKey(DataSet, null=True, blank=True,
                                 verbose_name="tttt",
                                 related_name="taskexecution_data_set")

    class Meta:
        get_latest_by = "dt_start"

    def __unicode__(self):
        return "%s %s" % (self.task.task.name, self.id)


class TaskLogging(models.Model):
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
