"""
An implementation of a IntervalService Task that does nothing but report
its logging level.
"""

from typing import Any, Dict, List, Optional

import argparse
import logging

from . import Config


class NopTask:
    """
    This class does nothing but report its logging level.
    """

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """

    def execute(self):
        """
        Executes the responsibilities of this executable
        """
        logging.info("Executed task for %s instance", type(self).__name__)

    def get_command_key(self) -> Optional[str]:
        """
        Returns the config item containing the name of requested command.
        """
        return None

    def get_config_file_key(self) -> Optional[str]:
        """
        Returns the config item containing the name of the config file.
        """
        return None

    def get_config_ignore(self) -> Optional[List[str]]:
        """
        If no 'get_config_mapping' function is supplied, this will
        return a list of config items to ignore when build the
        parameters passed in to 'set_params'.
        """
        return None

    def get_config_mapping(
        self, _: argparse.ArgumentParser
    ) -> Optional[Dict[str, str]]:
        """
        Returns a Dict that maps config items onto option variables, if this function does not exist
        in the Task it will be automatically generated from the ArgumentParser.
        """
        return None

    def get_config_section_key(self) -> Optional[str]:
        """
        Returns the section of the config file to use.
        """
        return None

    def get_defaults(self) -> Optional[Config]:
        """
        Returns a Config containing the default for every config item that has one.
        """
        return None

    def get_envar_mapping(self) -> Optional[Dict[str, str]]:
        """
        Return a dictionary that maps environmental variables onto option variables.
        """
        return None

    def get_log_file_key(self) -> Optional[str]:
        """
        Returns the name of the log file to use, if any.
        """
        return None

    def get_log_level_key(self) -> Optional[str]:
        """
        Returns the name of the log level to use, if any.
        """
        return None

    def get_pid_file_key(self) -> Optional[str]:
        """
        Returns config item containing the name of the pid file to use.
        """
        return None

    def get_interval(self) -> Optional[float]:
        """
        Returns the number of seconds to wait between executions.
        """
        return None

    def get_param_names(self) -> Optional[List[str]]:
        """
        Returns a List of the config items that should be included when building the parameters
        passed in to 'set_params'.
        """
        return None

    def looping_starting(self) -> None:
        """
        Informs the Task that the execution loop is about to start.
        """
        logging.info("Looping is starting")

    def looping_stopped(self) -> None:
        """
        Informs the Task that the execution loop has stopped.
        """
        logging.info("Looping has stopped")

    def set_params(self, params: Dict[str, Any]) -> Optional[str]:
        """
        Informs the Task of the new set of parameters it should use.
        """

    def updated_configuration(self, config: Config) -> None:
        """
        Informs this instance of the contents of the current configuration file. This can be used to
        construct the return value of 'get_param_names'.
        """
