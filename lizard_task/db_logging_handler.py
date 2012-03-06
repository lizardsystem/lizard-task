import logging
from lizard_task.models import TaskLogging
from lizard_task.models import TaskExecution
from datetime import datetime

logger = logging.getLogger(__name__)


class DBLoggingHandler(logging.Handler):
    """
    Save logging message en results.
    """

    def __init__(self, task_execution, username=None):
        """Create a instance of DBLoggingHandler objectc.

        Arguments:
        task_execution -- instance of TaskExecution object (Required)
        username -- full username as string
        """
        logging.Handler.__init__(self)
        self.task_execution = task_execution

    def emit(self, record):
        """Override the function of logging to save
        logging message into database."""
        print "set logging for %s." % self.task_execution
        try:
            task_logging = TaskLogging(task=self.task_execution,
                                       time=datetime.today(),
                                       level=record.levelno,
                                       message=record.msg,
                                       data_set=self.task_execution.data_set)
            task_logging.save()
        except Exception as ex:
            logger.error(',HIER'.join(map(str, ex.args)))
