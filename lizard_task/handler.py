from datetime import datetime

from lizard_task.models import TaskExecution
from lizard_task.models import PeriodicTaskExt
from lizard_task.models import LOGGING_LEVELS
from lizard_task.db_logging_handler import DBLoggingHandler

import logging
logger = logging.getLogger(__name__)


def logging_level(level):
    """Return numeric level of logging.

    Arguments:
    level -- logging level as string, like 'debug', 'INFO'
    """
    levelno = 40
    if level is None:
        return levelno

    for record in LOGGING_LEVELS:
        if level.upper() in record:
            levelno = record[0]
    print "return level %s." % levelno
    return levelno


def create_task_execution(task_ext, username):
    """Create task execution object.

    Arguments:
    """
    print
    try:
        task_execution = TaskExecution(
            task=task_ext,
            started_by=username,
            dt_start=datetime.today(),
            data_set=task_ext.data_set)
        task_execution.save()
        print task_execution
        return task_execution
    except Exception as ex:
        logger.error(','.join(map(str, ex.args)))


def get_handler(taskname, username, level):
    """Create logging handler to log messages into database.

    Arguments:
    taskname -- taskname of defined periodic task in admin interface
    username -- username as string
    level -- logging level as string like 'debug', 'INFO', ...
    """
    task_ext = PeriodicTaskExt.objects.get(task__name=taskname)
    task_execution = create_task_execution(task_ext, username)
    print task_execution
    print "+++++++++++++++++++++++++++++++++++++++++++"
    logging.handlers.DBLoggingHandler = DBLoggingHandler
    handler = logging.handlers.DBLoggingHandler(
        task_execution, username)
    handler.setLevel(logging_level(level))
    return handler
