"""
The minimal implementation of a Task that can be used by a IntervalService
instance.
"""


class Task:  # pylint: disable=too-few-public-methods
    """
    This class is a minimal implementation of a Task that can be used by
    a IntervalService instance.
    """

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """

    def execute(self) -> bool:
        """
        Executes the responsibilities of this executable.

        Returns:
            False so the it is not repeated.
        """
        return False
