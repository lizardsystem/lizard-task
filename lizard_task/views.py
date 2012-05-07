"""
API views not coupled to models.
"""
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

from lizard_task.models import PeriodicTaskExt
from lizard_map.views import AppView


class TasksView(AppView):
    """
        Get user context
    """

    template_name = "lizard_task/tasks_table_view.html"
    msg = ""

    def tasks(self):
        return PeriodicTaskExt.objects.filter(data_set__isnull=False)

    def get(self, request, *args, **kwargs):
        self.msg = request.GET.get('msg', '')
        return super(TasksView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Start PeriodicTaskExt with pk task_pk.
        """
        pk = request.POST['task_pk']
        # Lizard security is at work here.
        periodic_task_ext = PeriodicTaskExt.objects.get(pk=pk)
        periodic_task_ext.send_task(username=request.user.username)
        msg = "Taak '%s' is opgestart." % periodic_task_ext.task.name
        return HttpResponseRedirect('./?msg=%s' % msg)
