import datetime
import logging
from lizard_task.models import TaskLogging

logger = logging.getLogger(__name__)


class DBLoggingHandler(logging.Handler):
    """
    Save logging message en results.
    """

    def __init__(self, task_execution=None, username=None):
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
        if not self.task_execution:
            # Nowhere to log
            return
        try:
            task_logging = TaskLogging(
                task_execution=self.task_execution,
                time=datetime.datetime.now(),
                level=record.levelno,
                message=record.msg,
                data_set=self.task_execution.data_set)
            task_logging.save()
        except Exception as ex:
            logger.error("Error on save logging: %s" % (
                    ",".join(map(str, ex.args))))
