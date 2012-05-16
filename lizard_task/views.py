"""
API views not coupled to models.
"""
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

from lizard_task.models import SecuredPeriodicTask
from lizard_task.models import TaskExecution
from lizard_map.views import AppView


class SendTask(object):
    """
    Inherit this class in your view to react on post task messages.
    """
    def post(self, request, *args, **kwargs):
        """
        Start SecuredPeriodicTask with pk task_pk.
        """
        pk = request.POST['task_pk']
        # Lizard security is at work here.
        try:
            periodic_task = SecuredPeriodicTask.objects.get(pk=pk)
        except SecuredPeriodicTask.DoesNotExist:
            msg = ("Taak '%s' kan niet gevonden worden of mag niet worden uitgevoerd" %
                   periodic_task.name)
            return HttpResponseRedirect('./?msg=%s' % msg)
        # Staff-only?
        if not self.request.user.is_staff and periodic_task.staff_only:
            msg = ("Taak '%s' mag alleen door staff worden uitgevoerd." %
                   periodic_task.name)
            return HttpResponseRedirect('./?msg=%s' % msg)
        periodic_task.send_task(username=request.user.username)
        msg = "Taak '%s' is in de wachtrij geplaatst." % periodic_task.name
        return HttpResponseRedirect('./?msg=%s' % msg)


class TasksView(SendTask, AppView):
    """
    Show a list of all available tasks
    """

    template_name = "lizard_task/tasks_table_view.html"
    msg = ""

    def tasks(self):
        tasks = SecuredPeriodicTask.objects.all()
        if not self.request.user.is_staff:
            # Filter out non-staff tasks
            tasks = tasks.filter(staff_only=False)
        return tasks

    def get(self, request, *args, **kwargs):
        self.msg = request.GET.get('msg', '')
        return super(TasksView, self).get(request, *args, **kwargs)


class TaskDetailView(SendTask, AppView):
    """
    Show a task in detail, with history
    """

    template_name = 'lizard_task/task_detail.html'

    def task(self):
        return SecuredPeriodicTask.objects.get(pk=self.task_id)

    def get(self, request, *args, **kwargs):
        self.msg = request.GET.get('msg', '')
        self.task_id = kwargs['task_id']
        return super(TaskDetailView, self).get(request, *args, **kwargs)


class TaskExecutionDetailView(AppView):
    """
    Show a task execution with logs
    """

    template_name = 'lizard_task/task_execution_detail.html'

    def task_execution(self):
        return TaskExecution.objects.get(pk=self.task_execution_id)

    def task(self):
        task_execution = self.task_execution()
        return task_execution.task

    def get(self, request, *args, **kwargs):
        self.task_execution_id = kwargs['task_execution_id']
        return super(TaskExecutionDetailView, self).get(request, *args, **kwargs)
