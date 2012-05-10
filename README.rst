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


Usage in our project
--------------------
To use lizard-task, we need to

- Add celery, django-celery and lizard-security to INSTALLED_APPS
- Create celery database tables::

  $ bin/django syncdb

- Create django-celery, lizard-security and lizard-task database tables::

  $ bin/django migrate

- Configure celery to use message broker, by additing
  the following to your settings.py::

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
  from lizard_task.handler import get_handler

  @task()
  def import_dbf(username=None, taskname=None, loglevel=20):

      # Set up logging
      handler = get_handler(username=username, taskname=taskname)
      logger.addHandler(handler)
      logger.setLevel(loglevel)

      # Actual code to do the task

      <<your code>>
      logger.info("Logging message")
      <<your code>>

      # Remove logging handler
      logger.removeHandler(handler)

      # Task result
      return 'OK'
