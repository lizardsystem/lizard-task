from datetime import datetime
from celery.task import Task

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
    return levelno


def create_task_execution(task_ext, username, task_uuid):
    """Create task execution object.

    Arguments:
    task_ext -- object of PeriodicTaskExt class
    username -- username as string
    task_uuid -- uuid of task execution
    """
    try:
        task_execution = TaskExecution(
            task=task_ext,
            task_uuid=task_uuid,
            started_by=username,
            dt_start=datetime.today(),
            data_set=task_ext.data_set if task_ext else None)
        task_execution.save()
        return task_execution
    except Exception as ex:
        logger.error(','.join(map(str, ex.args)))


def get_handler(taskname=None, username=None):
    """Create logging handler to log messages into database.

    Arguments:
    task_uuid -- uuid of task execution
    username -- username as string
    taskname -- name of periodic task
    """
    task_ext = None
    if taskname:
        try:
            task_ext = PeriodicTaskExt.objects.filter(task__name=taskname)[0]
        except:
            logger.exception('Something went wrong fetching task_ext')

    task_uuid = Task.request.id  # Current task uuid
    task_execution = create_task_execution(task_ext, username, task_uuid)
    logging.handlers.DBLoggingHandler = DBLoggingHandler
    handler = logging.handlers.DBLoggingHandler(
        task_execution, username)
    return handler
