"""
An implementation of a IntervalService Task that can be reloaded and stopped
by an external process.
"""

from typing import Optional

import argparse

from . import COMMAND_KEY
from .wait_task import WaitTask


class CommandTask(WaitTask):
    """
    This class simply waits for its IntervalService to be stopped.
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
            "-c",
            f"--{COMMAND_KEY}",
            dest="COMMAND",
            help="The command to execute on the running instance of this service",
        )
        return parser

    def get_command_key(self) -> Optional[str]:
        """
        Returns the config item containing the name of requested command.
        """
        return COMMAND_KEY
