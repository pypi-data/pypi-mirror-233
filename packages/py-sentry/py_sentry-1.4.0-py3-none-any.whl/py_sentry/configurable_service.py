"""
This shows how to create an executeable to run a Task using the
py-sentry.service module.
"""

from .service import IntervalService


def main() -> int:
    """
    Runs the configurable_task as a py-sentry.
    """
    service = IntervalService("configurable_task")
    return service.run()


if __name__ == "__main__":
    main()
