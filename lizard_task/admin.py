from django.contrib import admin

from celery.execute import send_task
from djcelery import loaders
from djcelery.models import TaskState
from djcelery.models import PeriodicTask
from djcelery.admin import PeriodicTaskAdmin
from djcelery.admin import LaxChoiceField
from celery import registry
from django import forms
from django.utils.translation import ugettext_lazy as _

from lizard_task.models import SecuredPeriodicTask
from lizard_task.models import TaskExecution
from lizard_task.models import TaskLogging

from lizard_security.models import DataSet

from django.utils import simplejson as json


class TaskLoggingAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_execution', 'time', 'level', 'message', 'data_set')
    list_filter = ('task_execution',)


class TaskExecutionAdmin(admin.ModelAdmin):
    list_display = ('task', 'task_uuid', 'status',
                    'started_by', 'log_messages',
                    'dt_start', 'dt_finish', 'task_uuid')

    def status(self, obj):
        states = TaskState.objects.filter(task_id=obj.task_uuid)
        if states.exists():
            return states[0].state

    def log_messages(self, obj):
        logs = TaskLogging.objects.filter(task__id=obj.id).order_by('id')
        msg = ""
        for log in logs:
            msg = "%s | %s" % (msg, log.message)
        return msg


def secured_periodic_task_form():
    """
    Based on djcelery.admin.periodic_task_form
    """
    loaders.autodiscover()
    tasks = list(sorted(registry.tasks.regular().keys()))
    choices = (("", ""), ) + tuple(zip(tasks, tasks))

    class SecuredPeriodicTaskForm(forms.ModelForm):
        """
        Either fill in "periodic_task", or the fields (reg)task, name, ...

        If periodic_task is filled, (reg)task, name will be filled if empty.
        """
        # name = forms.CharField(max_length=200, required=False)
        regtask = LaxChoiceField(label=_(u"Task (registered)"),
                                 choices=choices, required=False)
        task = forms.CharField(label=_("Task (custom)"), required=False,
                               max_length=200)
        data_set = forms.ModelChoiceField(queryset=DataSet.objects.all(),
                                          required=False)

        class Meta:
            model = SecuredPeriodicTask

        def clean(self):
            data = super(SecuredPeriodicTaskForm, self).clean()

            regtask = data.get("regtask")
            if regtask:
                data["task"] = regtask
            if not data["task"]:
                exc = forms.ValidationError(_(u"Need name of task"))
                self._errors["task"] = self.error_class(exc.messages)
                raise exc

            return data

    return SecuredPeriodicTaskForm


class SecuredPeriodicTaskAdmin(PeriodicTaskAdmin):
    model = SecuredPeriodicTask
    form = secured_periodic_task_form()
    fieldsets = (
            (None, {
                "fields": ("name", "regtask", "task", "enabled", "data_set"),
                "classes": ("extrapretty", "wide"),
            }),
            ("Schedule", {
                "fields": ("interval", "crontab"),
                "classes": ("extrapretty", "wide", ),
            }),
            ("Arguments", {
                "fields": ("args", "kwargs"),
                "classes": ("extrapretty", "wide", "collapse"),
            }),
            ("Execution Options", {
                "fields": ("expires", "queue", "exchange", "routing_key"),
                "classes": ("extrapretty", "wide", "collapse"),
            }),
    )

    def __init__(self, *args, **kwargs):
        super(SecuredPeriodicTaskAdmin, self).__init__(*args, **kwargs)
        self.form = secured_periodic_task_form()


admin.site.register(SecuredPeriodicTask, SecuredPeriodicTaskAdmin)
admin.site.register(TaskLogging, TaskLoggingAdmin)
admin.site.register(TaskExecution, TaskExecutionAdmin)
admin.site.unregister(PeriodicTask)  # We always want the SecuredPeriodicTask instead
