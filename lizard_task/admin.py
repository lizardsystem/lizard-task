from django.contrib.gis import admin

from celery.execute import send_task
from djcelery import loaders

from lizard_task.models import PeriodicTaskExt
from lizard_task.models import TaskExecution
from lizard_task.models import TaskLogging

from django.utils import simplejson as json


class TaskLoggingAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'time', 'level', 'message', 'data_set')
    list_filter = ('task',)


class TaskExecutionAdmin(admin.ModelAdmin):
    list_display = ('task', 'started_by', 'log_messages',
                    'dt_start', 'dt_finish', 'task_uuid')

    def log_messages(self, obj):
        logs = TaskLogging.objects.filter(task__id=obj.id).order_by('id')
        msg = ""
        for log in logs:
            msg = "%s | %s" % (msg, log.message)
        return msg


class PeriodicTaskExtAdmin(admin.ModelAdmin):
    loaders.autodiscover()

    list_display = (
        'id_no_link', 'task', 'args', 'kwargs', 'data_set')
    list_filter = ('data_set',)

    actions = ['empty_action', 'run_tasks']

    def args(self, obj):
        return obj.task.args

    def kwargs(self, obj):
        return obj.task.kwargs

    def id_no_link(self, obj):
        return u'</a>%s<a>' % obj.id
    id_no_link.allow_tags = True
    id_no_link.short_description = "id"

    def run_tasks(self, request, queryset):
        for item in queryset: 
            task_name = str(item.task.task)
            args = json.loads(item.task.args)
            kwargs = json.loads(item.task.kwargs)
            kwargs["username"] = request.user.username
            send_task(task_name, args=args, kwargs=kwargs)
        self.message_user(request, "Taak is opgestart.")
    run_tasks.short_description = "Uitvoeren geselecteerde task"


admin.site.register(PeriodicTaskExt, PeriodicTaskExtAdmin)
admin.site.register(TaskLogging, TaskLoggingAdmin)
admin.site.register(TaskExecution, TaskExecutionAdmin)
