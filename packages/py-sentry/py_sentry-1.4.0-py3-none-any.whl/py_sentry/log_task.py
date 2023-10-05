"""
An implementation of a IntervalService Task that shows how the logging
system can be configured.
"""

from typing import Optional

import argparse
import logging

from . import Config, LOG_LEVELS, LOG_FILE_KEY, LOG_LEVEL_KEY


class LogTask:
    """
    This class shows how the logging system can be configured.
    """

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """

    def create_argument_parser(self) -> argparse.ArgumentParser:
        """
        Creates and populates the argparse.ArgumentParser for this Task.
        """
        parser = argparse.ArgumentParser(
            description=f"Executes an instance of the {type(self).__name__} class"
        )
        parser.add_argument(
            f"--{LOG_FILE_KEY}",
            dest="LOG_FILE",
            help="The file, as opposed to stdout, into which to write log messages",
        )
        parser.add_argument(
            "-l",
            f"--{LOG_LEVEL_KEY}",
            dest="LOG_LEVEL",
            help="The logging level for this execution",
            choices=LOG_LEVELS.keys(),
        )
        return parser

    def execute(self):
        """
        Executes the responsibilities of this executable
        """
        logging.debug("Debug level is being output")
        logging.info("Info level is being output")
        logging.warning("Warning level is being output")
        logging.error("Error level is being output")
        logging.critical("Critical level is being output")

    def get_defaults(self) -> Optional[Config]:
        """
        Return a dictionary to map default value to option variables.
        """
        return {LOG_LEVEL_KEY: "INFO"}

    def get_interval(self) -> Optional[float]:
        """
        Returns the number of seconds to wait between executions.
        """
        return -1

    def get_log_file_key(self) -> Optional[str]:
        """
        Returns the name of the log file to use, if any.
        """
        return LOG_FILE_KEY

    def get_log_level_key(self) -> Optional[str]:
        """
        Returns the name of the log level to use, if any.
        """
        return LOG_LEVEL_KEY
