"""
This module provides  provides a foundation for a service that will run
a task at a set interval.
"""

from .constants import (
    Config,
    SigHandler,
    LOG_LEVELS,
    COMMAND_KEY,
    INI_FILE_KEY,
    INI_SECTION_KEY,
    LOG_FILE_KEY,
    LOG_LEVEL_KEY,
)
from .service import IntervalService
from .task import Task
