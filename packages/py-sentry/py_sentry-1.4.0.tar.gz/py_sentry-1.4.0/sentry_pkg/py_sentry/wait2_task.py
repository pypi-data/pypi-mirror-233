"""
An implementation of a IntervalService Task that used an explicit wait  to
wait for the IntervalService to be stopped.
"""

from typing import Optional

import logging
import signal
from threading import Event

from . import Config, LOG_LEVEL_KEY


class Wait2Task:  # pylint: disable=too-few-public-methods
    """
    This class simply waits for its IntervalService to be stopped.
    """

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """
        self.__exit = Event()

    def execute(self):
        """
        Executes the responsibilities of this executable.
        """
        while not self.__exit.is_set():
            logging.debug("Starting to wait")
            self.__exit.wait(60)
            logging.debug("Stopped waiting")

    def get_defaults(self) -> Optional[Config]:
        """
        Return a dictionary to map default value to option variables.
        """
        return {LOG_LEVEL_KEY: "DEBUG"}

    def get_log_level_key(self) -> Optional[str]:
        """
        Returns the name of the log level to use, if any.
        """
        return LOG_LEVEL_KEY

    def interrupt(self, signum):
        """
        Informs this instance that, if possible, it should cleanly
        abandon its current execution if it is in progress.
        """
        if signal.SIGINT == signum:
            self.__exit.set()
