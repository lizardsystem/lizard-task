# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin

from lizard_ui.urls import debugmode_urlpatterns

from lizard_task.views import TasksView
from lizard_task.views import TaskDetailView
from lizard_task.views import TaskExecutionDetailView

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    url(r'^$',
        TasksView.as_view(),
        name='lizard_task_home'),
    url(r'^(?P<task_id>\d+)/$',
        TaskDetailView.as_view(),
        name='lizard_task_detail'),
    url(r'^execution/(?P<task_execution_id>\d+)/$',
        TaskExecutionDetailView.as_view(),
        name='lizard_task_execution_detail'),
    )
urlpatterns += debugmode_urlpatterns()
