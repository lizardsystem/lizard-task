import datetime
from celery.task import Task

from lizard_task.models import TaskExecution
from lizard_task.models import SecuredPeriodicTask
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


def create_task_execution(task, username, task_uuid):
    """Create task execution object.

    Arguments:
    task -- object of SecuredPeriodicTask class
    username -- username as string
    task_uuid -- uuid of task execution
    """
    try:
        task_execution = TaskExecution(
            task=task,
            task_uuid=task_uuid,
            started_by=username,
            dt_start=datetime.datetime.now(),
            data_set=task.data_set if task else None)
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
    task = None
    if taskname:
        try:
            task = SecuredPeriodicTask.objects.filter(name=taskname)[0]
        except:
            logger.exception('Something went wrong fetching task')

    task_uuid = Task.request.id  # Current task uuid
    if task_uuid:
        task_execution = create_task_execution(task, username, task_uuid)
    else:
        task_execution = None
    return DBLoggingHandler(task_execution, username)
