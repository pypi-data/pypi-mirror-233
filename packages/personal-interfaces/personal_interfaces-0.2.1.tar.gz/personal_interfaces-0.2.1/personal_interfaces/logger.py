"""
Logger for the server
"""
import os
from functools import partial
from typing import Callable, Dict
from datetime import datetime
import attr
from rich.console import Console
# "Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i]."


@attr.s(slots=True)
class Logger:  # pylint: disable=R0903
    """Logger object for the server"""
    _console: Console = attr.ib(default=Console())
    _url: str = attr.ib(default=None)
    _date: Callable = attr.ib(default=None)
    _log: Dict[str, Callable] = attr.ib(default=None)

    def __attrs_post_init__(self):
        # Create a lambda function to obtain the time at each iteration that we call the logger
        self._date = datetime.now
        # Initialize the url as a localhost in case that we don't provide one
        self._url = os.environ.get('URL', "")
        # Initialize the status dict
        self.__status()

    def __status(self) -> None:
        """Private method to define the status for the logger."""
        # Define the lambda to be called in the dict
        def _print(color: str, status: str, msg: str) -> None:
            self._console.print(
                f"[bold {color}]-[S:{status}|D:{self._date()}|U:{self._url}][/bold {color}]: {msg}")
        # Now, define the _log dictionary
        self._log = {
            'INFO': partial(_print, "cyan", "INFO"),
            'DEBUG': partial(_print, "yellow", "DEBUG"),
            'ERROR': partial(_print, "red", "ERROR"),
            'SUCCESS': partial(_print, "green", "SUCCESS")
        }

    def log(self, message: str, status: str = 'DEBUG') -> None:
        """Method to print a log. The status are:

        - info
        - debug
        - error
        - success

        Args:
            status (str): The status for this log. Default to "DEBUG".
        """
        self._log[status.upper()](message)
