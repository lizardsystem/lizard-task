"""
API views not coupled to models.
"""
from django.views.decorators.csrf import csrf_exempt
from celery.execute import send_task
from django.utils import simplejson as json

from lizard_task.models import PeriodicTaskExt
from lizard_map.views import AppView


class TasksView(AppView):
    """
        Get user context
    """

    template_name = "tasks_table_view.html"
    msg = ""

    def tasks(self):
        print len(PeriodicTaskExt.objects.all())
        print self.request.user.username
        return PeriodicTaskExt.objects.filter(data_set__isnull=False)
             
    def post(self, request, *args, **kwargs):
        task_name = request.POST.get('task_name', None)
        lizard_tasks = PeriodicTaskExt.objects.filter(
            task__name=task_name)
        if lizard_tasks.exists():
            task = lizard_tasks[0].task
            args_params = json.loads(task.args)
            kwargs_params = json.loads(task.kwargs)
            kwargs_params["username"] = request.user.username
            result = send_task(task.task, args=args_params, kwargs=kwargs_params)
            print type(result)
            print result
            self.msg = "Taak '%s' is opgestart." % task_name
        else:
            self.msg = "Taak '%s' is niet opgestart." % task_name
        return self.get(request, *args, **kwargs)


    
