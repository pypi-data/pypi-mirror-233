"""
An implementation of a IntervalService Task that used the implicit wait
between tasks to wait for the IntervalService to be stopped.
"""

from typing import Optional

import logging


class WaitTask:  # pylint: disable=too-few-public-methods
    """
    This class simply waits for its IntervalService to be stopped.
    """

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """

    def execute(self):
        """
        Executes the responsibilities of this executable.
        """
        logging.info("Executed task for %s instance", type(self).__name__)

    def get_interval(self) -> Optional[float]:
        """
        Returns the number of seconds to wait between executions.
        """
        return 10
