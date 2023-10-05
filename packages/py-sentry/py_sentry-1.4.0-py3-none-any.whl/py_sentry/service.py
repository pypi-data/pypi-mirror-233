"""
Runs an instance of the Task class as a command line executable.

A Task run by this service must provide the following function:

    execute(self) -> bool

A Task run by this service may provide the following functions:

    create_argument_parser(self) -> argparse.ArgumentParser
        Creates and populates the argparse.ArgumentParser for this Task.

    get_command_key(self) -> Optional[str]
        Returns the config item containing the name of requested command.

    get_config_file_key(self) -> Optional[str]
        Returns the config item containing the name of the config file.
        
    get_config_ignore(self) -> Optional[List[str]]
        If no 'get_config_mapping' function is supplied, this will return a list of config items to
        ignore when building the parameters passed in to 'set_params'.
        
    get_config_mapping(self, parse: argparse.ArgumentParser) -> Optional[Dict[str, str]]
        Returns a Dict that maps config items onto option variables, if this function does not exist
        in the Task it will be automatically generated from the ArgumentParser.

    get_config_section_key(self) -> Optional[str]
        Returns the config item containing the section of the config file to use.

    get_defaults(self) -> Optional[Config]
        Returns a Config containing the default for every config item that has one.

    get_envar_mapping(self) -> Optional[Dict[str, str]]
        Return a dictionary that maps environmental variables onto option variables.

    get_interval(self) -> Optional[float]
        Returns the number of seconds to wait between executions, None stops loop execution.

    get_log_file_key(self) -> Optional[str]
        Returns config item containing the name of the log file to use, if any.

    get_log_level_key(self) -> Optional[str]
        Returns config item containing the name of the log level to use, if any.        

    get_param_names(self) -> Optional[List[str]]
        Returns a List of the config items that should be included when building the parameters
        passed in to 'set_params'. If this in None, 'set_params' will not be called.

    get_pid_file_key(self) ->  -> Optional[str]
        Returns config item containing the name of the pid file to use.  

    looping_starting(self) -> None
        Informs the Task that the execution loop is about to start.

    looping_stopped(self) -> None
        Informs the Task that the execution loop has stopped.

    set_params(self, params: Dict[str, Any]) -> Optional[str]:
        Informs the Task of the new set of parameters it should use.

    updated_configuration(self, config: Config) -> None
        Informs this instance of the contents of the current configuration file. This can be used to
        construct the return value of 'get_param_names'.

"""

from typing import Any, Callable, Dict, List, Optional, Type
from types import FrameType

import argparse
import atexit
from configparser import ConfigParser, NoSectionError
import errno
from importlib.metadata import entry_points
import logging
import os
from pathlib import Path
import signal
import sys
from threading import Event

import psutil

from .constants import Config, SigHandler, LOG_LEVELS
from .task import Task

DEFAULT_CONFIG_IGNORE = ["help"]

DEFAULT_INI_FILE = "py-sentry.ini"
INTERVAL_SERVICE_GROUP = "py-sentry"


def create_config_mapping(
    parser: argparse.Namespace, ignore: Optional[List[str]]
) -> Dict[str, str]:
    """
    Return a dictionary to map config variables to option variables.
    """
    result = {}
    for action in parser._actions:  # pylint: disable=protected-access
        name = ""
        for option in action.option_strings:
            option = option.lstrip("-")
            if len(option) > len(name):
                name = option
        if None is ignore or name not in ignore:
            result[name] = action.dest
    return result


def execute_command(command: str, pid: int):
    """
    Send the necessary signal to the running instance to carry out the
    requested command.
    """
    if "reload" == command:
        os.kill(pid, signal.SIGHUP)
        logging.debug("Sent SIGHUP to pid %i", pid)
    elif "stop" == command:
        os.kill(pid, signal.SIGINT)
        logging.debug("Sent SIGINT to pid %i", pid)
    else:
        logging.warning("Action %s is not currently supported", command)


def read_config(  # pylint: disable = too-many-arguments, too-many-branches
    config_file: str,
    section: str,
    strings: Optional[List[str]] = None,
    integers: Optional[List[str]] = None,
    booleans: Optional[List[str]] = None,
) -> Config:
    """
    Reads the supplied configuration ini

    Args:
        config_file: the path to the file containing the configuration information.
        section: the section within the file containing the configuration for this instance.
        booleans: a List of keys that should be returned as strings.
        booleans: a List of keys that should be returned as bools.
        integers: a List of keys that should be returned as integers.
    """

    resolved_path = os.path.expandvars(config_file)
    if not os.path.exists(resolved_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), resolved_path)
    config_parser = ConfigParser()
    config_parser.read(resolved_path)
    config: Config = {}
    for option in config_parser.options(section):
        try:
            if None is not strings and option in strings:
                config[option] = config_parser.get(section, option)
            if None is not integers and option in integers:
                config[option] = config_parser.getint(section, option)
            elif None is not booleans and option in booleans:
                config[option] = config_parser.getboolean(section, option)
            else:
                config[option] = config_parser.get(section, option)
        except:  # pylint: disable = bare-except
            config[option] = None

    if None is not strings:
        for option in strings:
            if not option in config:
                config[option] = None

    if None is not integers:
        for option in integers:
            if not option in config:
                config[option] = None

    if None is not booleans:
        for option in booleans:
            if not option in config:
                config[option] = None

    return config


def read_envar_values(mapping: Dict[str, str]) -> Optional[argparse.Namespace]:
    """
    Create a argparse.Namespace instance populated by the values of the
    envrionmental variables specified by the keys of the mapping.
    """
    result = {}
    if None is mapping:
        return None
    for key in mapping.keys():
        value = os.getenv(key)
        if None is not value:
            option = mapping[key]
            result[option] = value
    return argparse.Namespace(**result)


def select_task_class(group: str, name: str) -> Type[Task]:
    """
    Returns the selected service class object.
    """
    services = entry_points(group=group)
    for entry in services:
        if name == entry.name:
            return entry.load()
    raise ValueError(f'No known Task implementation named "{name}"')


class IntervalService:  # pylint: disable=too-many-instance-attributes
    """
    This class implements a simple interval service that can be run an OCI container.
    """

    def __init__(self, task: str):
        """
        Creates an instance of this class.

        Args:
            task_name: the name of the class implementing the task.
        """
        self.__config: Optional[Config] = None
        self.__config_mapping: Optional[Dict[str, str]] = None
        self.__defaults: Optional[Config] = None
        self.__delaying = Event()
        self.__logging_initialized = False
        self.__prelogging_warnings: List[str] = []
        self.__options: Optional[argparse.Namespace] = None
        self.__options_dictionary: Optional[Dict[str, Any]] = None
        self.__pid_file: Optional[Path] = None
        self.__reconfigure = False
        self.__stopping = False
        self.__supported_signals: Dict[
            int, Callable[[int, Optional[FrameType]], Any]
        ] = {}
        self.__supported_signals[signal.SIGINT] = self.__sigint
        self.__supported_signals[signal.SIGHUP] = self.__sighup
        task_class = select_task_class(INTERVAL_SERVICE_GROUP, task)
        self.__task = task_class()

    def close(self) -> None:
        """
        Deletes the pid file when this instance was execution the service.
        """
        if None is not self.__pid_file:
            self.__pid_file.unlink(True)

    def configure_task(self) -> Optional[str]:
        """
        Set the configuration for this service.

        Returns:
            None if task configured successfully, otherwise it return
            the reason why configuration failed.
        """
        if hasattr(self.__task, "get_config_file_key") and hasattr(
            self.__task,
            "get_config_section_key",
        ):
            self.__read_config_from_file()
        if not self.__logging_initialized:
            self.__initialize_logging()
            self.__logging_initialized = True
        if hasattr(self.__task, "updated_configuration"):
            self.__task.updated_configuration(self.__config)
        if hasattr(self.__task, "get_param_names") and hasattr(
            self.__task,
            "set_params",
        ):
            param_names = self.__task.get_param_names()
            if None is not param_names and 0 != len(param_names):
                param_values: Dict[str, Any] = {}
                for param_name in param_names:
                    param_values[param_name] = self.select_value(param_name)
                return self.__task.set_params(param_values)
        return None

    def __resolve_interval(self) -> Optional[float]:
        if not hasattr(self.__task, "get_interval"):
            logging.debug("Task does not supply an interval, so terminating now")
            return None
        interval_string = self.__task.get_interval()
        if None is interval_string:
            logging.debug("No interval specified, so terminating now")
            return None
        interval = float(interval_string)
        if 0.0 < interval:
            logging.debug("Waiting %i seconds before next execution", interval)
            return interval
        if 0.0 > interval:
            logging.debug("Task has requested termination of loop")
            return None
        logging.debug("No wait before next execution")
        return None

    def get_pid(self) -> Optional[int]:
        """
        Returns the pid of the process containing the running instance
        of the service.
        """
        if hasattr(self.__task, "get_pid_file_key"):
            filename = self.select_value(self.__task.get_pid_file_key())
            if None is not filename:
                self.__pid_file = Path(filename)
        if None is self.__pid_file:
            self.__pid_file = Path(f"/tmp/py-sentry.{type(self.__task).__name__}.pid")

        if not self.__pid_file.exists():
            result = os.getpid()
            with open(self.__pid_file, "w", encoding="utf-8") as pid_file:
                pid_file.write(str(result))
            atexit.register(self.close)
            return result

        with open(self.__pid_file, "r", encoding="utf-8") as pid_file:
            try:
                result = int(pid_file.read())
            except (OSError, ValueError):
                return None

        if psutil.pid_exists(result):
            return result
        self.close()
        return None

    def __initialize_logging(self) -> None:  # pylint: disable=too-many-branches
        """
        Initializes the logging infrastructure.
        """
        if self.__logging_initialized:
            return
        if hasattr(self.__task, "get_log_file_key"):
            log_file_key = self.__task.get_log_file_key()
            if None is log_file_key:
                log_file = None
            else:
                log_file = self.select_value(log_file_key)
        else:
            log_file = None
        if hasattr(self.__task, "get_log_level_key"):
            log_level_key = self.__task.get_log_level_key()
            if None is log_level_key:
                log_level = None
            else:
                log_level = self.select_value(log_level_key)
        else:
            log_level = None

        if None is log_level:
            level_to_use = logging.INFO
        else:
            level_to_use = LOG_LEVELS[log_level]

        if None is log_file:
            logging.basicConfig(stream=sys.stdout, level=level_to_use)
        else:
            logging.basicConfig(filename=log_file, level=level_to_use)

        for warning in self.__prelogging_warnings:
            logging.warning(warning)

    def __loop(self) -> None:
        """
        Repeatedly runs the execute method of the supplied task.
        """
        logging.debug(
            "Starting repeated execution of %s instance", type(self.__task).__name__
        )
        previous_signals: Dict[int, SigHandler] = {}
        for sig, handler in self.__supported_signals.items():
            previous_signals[sig] = signal.signal(sig, handler)

        if hasattr(self.__task, "looping_starting"):
            self.__task.looping_starting()

        self.__delaying.clear()
        if not self.__stopping:
            self.__reconfigure_when_required()
            self.__task.execute()
        while not self.__stopping:
            interval = self.__resolve_interval()
            if None is interval:
                self.stop()
            else:
                self.__delaying.wait(interval)
                self.__delaying.clear()
            if not self.__stopping:
                self.__reconfigure_when_required()
                self.__task.execute()

        for sig2, handler2 in previous_signals.items():
            signal.signal(sig2, handler2)
        if hasattr(self.__task, "looping_stopped"):
            self.__task.looping_stopped()
        logging.debug(
            "Stopped repeated execution of %s instance", type(self.__task).__name__
        )

    def prepare_options(self):
        """
        Prepares the options derived from the command line and
        environmental variables.
        """
        if hasattr(self.__task, "create_argument_parser"):
            parser = self.__task.create_argument_parser()
        else:
            parser = argparse.ArgumentParser(
                description=f"Executes an instance of the {type(self.__task).__name__} class"
            )
        if hasattr(self.__task, "get_envar_mapping"):
            envar_mapping = self.__task.get_envar_mapping()
            if None is envar_mapping:
                envar_mapping = {}
        else:
            envar_mapping = {}
        envar_values = read_envar_values(envar_mapping)
        self.__options = parser.parse_args(namespace=envar_values)
        if None is not self.__options:
            if hasattr(self.__task, "get_config_mapping"):
                self.__config_mapping = self.__task.get_config_mapping(parser)
            else:
                if hasattr(self.__task, "get_config_ignore"):
                    ignore = self.__task.get_config_ignore()
                else:
                    ignore = DEFAULT_CONFIG_IGNORE
                self.__config_mapping = create_config_mapping(parser, ignore)
            self.__options_dictionary = vars(self.__options)
            if hasattr(self.__task, "get_defaults"):
                self.__defaults = self.__task.get_defaults()

    def __read_config_from_file(self):
        """
        Reads this task's configuration from a file.
        """
        ini_filename = self.select_value(self.__task.get_config_file_key())
        if None is not ini_filename:
            ini_section = self.select_value(self.__task.get_config_section_key())
            if None is not ini_section:
                try:
                    self.__config = read_config(ini_filename, ini_section)
                except FileNotFoundError as _:
                    self.__prelogging_warnings.append(
                        f'Configuration file, "{ini_filename}", does not exist'
                    )
                except NoSectionError as _:
                    self.__prelogging_warnings.append(
                        f'Section "{ini_section}" does not appear in the configuration file'
                    )

    def __reconfigure_when_required(self):
        """
        Reconfigures the Task when such action has been requested.
        """
        if self.__reconfigure:
            failure_message = self.configure_task()
            if None is not failure_message:
                logging.warning(failure_message)
                return
            logging.debug("Reconfigured Task")
            self.__reconfigure = False

    def run(self) -> int:
        """
        Main routine that executes an instance of a drop.Dropper class.
        """
        self.prepare_options()
        failure_message = self.configure_task()

        logging.debug("Begin options:")
        options_dictionary = self.__options.__dict__
        for option in options_dictionary:
            value = options_dictionary[option]
            if value is not None:
                logging.debug("    %s = %s", option, value)
        logging.debug("End options:")

        if None is not failure_message:
            logging.critical(failure_message)
            return 1

        pid = self.get_pid()
        if None is pid:
            logging.warning(
                "Can not determine if another instance is running. Try again"
            )
            return 2

        if hasattr(self.__task, "get_command_key"):
            command = self.select_value(self.__task.get_command_key())
        else:
            command = None

        if os.getpid() == pid:
            if None is command:
                self.__loop()
        else:
            if None is not command:
                execute_command(command, pid)
            else:
                logging.debug("The running instance of this service has pid %i", pid)
            return 0
        return 0

    def select_value(self, name: str):
        """
        Selects a value by going down through the available values.
        """
        if None is name:
            return None
        if None is not self.__options:
            if None is not self.__config_mapping and name in self.__config_mapping:
                option_name = self.__config_mapping[name]
                if (
                    None is not self.__options_dictionary
                    and option_name in self.__options_dictionary
                ):
                    value = self.__options_dictionary[option_name]
                    if None is not value:
                        return value
        if None is not self.__config:
            if name in self.__config:
                value = self.__config[name]
                if None is not value:
                    return value
        if None is not self.__defaults:
            if name in self.__defaults:
                value = self.__defaults[name]
                if None is not value:
                    return value
        return None

    def __sighup(self, signum, __) -> None:
        """
        Signal handler for SIGINT signal.
        """
        logging.debug("SIGHUP recevied")
        if hasattr(self.__task, "interrupt"):
            self.__task.interrupt(signum)
        self.__reconfigure = True
        self.__delaying.set()

    def __sigint(self, signum, __) -> None:
        """
        Signal handler for SIGINT signal.
        """
        logging.debug("SIGINT recevied")
        if hasattr(self.__task, "interrupt"):
            self.__task.interrupt(signum)
        self.stop()

    def stop(self) -> None:
        """
        Signals that the drip-feeding loop should exit.
        """
        self.__stopping = True
        self.__delaying.set()
