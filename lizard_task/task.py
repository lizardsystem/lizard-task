import logging
import datetime
import traceback

from django.db import transaction

from lizard_task.handler import get_handler


def task_logging(the_func):
    """
    Adds logger to another function. This logger makes TaskExecution
    objects.
    """
    def _decorated(*args, **kwargs):
        # Set up logging
        handler = get_handler(
            username=kwargs.get('username', None),
            taskname=kwargs.get('taskname', None))
        logger = logging.getLogger(kwargs.get('taskname', __name__))
        logger.addHandler(handler)
        logger.setLevel(kwargs.get('loglevel') or 20)

        try:
            with transaction.commit_on_success():
                the_func(*args, **kwargs)
            result = 'ok'
        except:
            logger.error('Exception')
            for exception_line in traceback.format_exc().split('\n'):
                logger.error(exception_line)
            result = 'failure'

        # Remove logging handler. Note that the handler is not removed if the_func crashes.
        if handler.task_execution:
            handler.task_execution.result = result
            handler.task_execution.dt_finish = datetime.datetime.now()
            handler.task_execution.save()

        logger.removeHandler(handler)

        return result

    # The celery @task decorator require these properties to match.
    _decorated.__module__ = the_func.__module__
    _decorated.__name__ = the_func.__name__

    return _decorated
