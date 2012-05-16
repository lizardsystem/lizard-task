Running cellery tasks from admin interface with lizard-task
===========================================================


What lizard-task does
-------------------------

Lizard-task extends django-celery with next functionalities:

- Lizard-task provides the possibility to run periodic tasks from
  admin interface
- lizard-task provides the logging handler to save logging messages
  into database
- Lizard-task provides the possibility to view and filter task and
  loggings using lizard-security


Setting up lizard-task
----------------------
To use lizard-task, we need to

- Add celery, django-celery and lizard-security to INSTALLED_APPS
- Create celery database tables::

  $ bin/django syncdb

- Create django-celery, lizard-security and lizard-task database tables::

  $ bin/django migrate

- Configure celery to use message broker, by additing
  the following to your settings.py::

Option 1: Django database, easiest but limited (though mostly
sufficient). The biggest drawback is that you can't see the status,
because the Django Admin monitor doesn't work.

In your INSTALLED_APPS, add 'kombu.transport.django',

  BROKER_URL = "django://"


Option 2: RabbitMQ, flexible but more cumbersome:

  BROKER_HOST = "localhost"
  BROKER_PORT = 5672
  BROKER_USER = "myuser"
  BROKER_PASSWORD = "mypassword"
  BROKER_VHOST = "myvhost"

- Add modules with tasks to your settings.py::

  CELERY_IMPORTS = ('vss.tasks',
                    'lizard_wbconfiguration.tasks',
                    'lizard_fewsnorm.tasks',
                    'lizard_area.tasks',
                    'lizard_esf.tasks',)

- Created tasks in djcelery admin interface

- Create tasks in lizard-task admin interface

- Start celery worker::

  $ bin/django celeryd

  However, in production you probably want to run the worker in the
  background as a daemon. To do this you can use supervisor or other
  tools provided by your platform.


Example usage lizard-task logging handler
-----------------------------------------


  import logging
  from celery.task import task
  from lizard_task.task import task_logging


  @task
  @task_logging
  def import_dbf(username=None, taskname=None, loglevel=20):
      logger.getLogger(taskname)
      # Do your thing



task_logging accepts kwargs username, taskname, loglevel.

You have to use logger.getLogger(taskname) to get the TaskExecution
logger. This means that probably the logging in your sub-calls will
get lost.


Executing tasks
---------------

In admin, define a secured periodic task. As argument, provide
{"taskname": <fill in your name>}. Optionally, set your data_set and
staff_only.

Now you can view the list of available tasks in the frontend::

http://localhost:8000/task/
