#!/usr/bin/env python3
#            _       _
#  _ __ ___ (_)_ __ (_)_ __ ___   ___  _ __
# | '_ ` _ \| | '_ \| | '_ ` _ \ / _ \| '_ \
# | | | | | | | | | | | | | | | | (_) | | | |
# |_| |_| |_|_|_| |_|_|_| |_| |_|\___/|_| |_|
#
# minimon - a minimal monitor
# Copyright (C) 2023 - Frans Fürst
#
# minimon is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# minimon is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details at <http://www.gnu.org/licenses/>.
#
# Anyway this project is not free for machine learning. If you're using any content of this
# repository to train any sort of machine learned model (e.g. LLMs), you agree to make the whole
# model trained with this repository and all data needed to train (i.e. reproduce) the model
# publicly and freely available (i.e. free of charge and with no obligation to register to any
# service) and make sure to inform the author (me, frans.fuerst@protonmail.com) via email how to
# get and use that model and any sources needed to train it.

"""Common stuff shared among modules"""

import logging
import os
import signal
import sys
import threading
import traceback
from collections.abc import Callable, Iterator, Mapping
from types import FrameType, TracebackType
from typing import TextIO

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("minimon")


def setup_logging() -> None:
    """Make logging fun"""

    class CustomLogger(logging.Logger):
        """Logs a record the way we want it"""

        @staticmethod
        def stack_str(depth: int = 0) -> str:
            """Create a tiny string from current call stack"""

            def stack_fns() -> Iterator[str]:
                # pylint: disable=protected-access
                stack = list(reversed(traceback.extract_stack(sys._getframe(depth))))
                for site in stack:
                    if site.filename != stack[0].filename or site.name == "<module>":
                        break
                    yield site.name

            return ">".join(reversed(list(stack_fns())))

        # pylint: disable=too-many-arguments
        def makeRecord(
            self,
            name: str,
            level: int,
            fn: str,
            lno: int,
            msg: object,
            args: tuple[object, ...] | Mapping[str, object],
            exc_info: tuple[type[BaseException], BaseException, TracebackType | None]
            | tuple[None, None, None]
            | None,
            func: str | None = None,
            extra: Mapping[str, object] | None = None,
            sinfo: str | None = None,
        ) -> logging.LogRecord:
            """Creates a log record with a 'stack' element"""
            new_extra = {
                **(extra or {}),
                **{
                    "stack": self.stack_str(5),
                    "posixTID": threading.get_native_id(),
                },
            }
            return super().makeRecord(
                name, level, fn, lno, msg, args, exc_info, func, new_extra, sinfo
            )

    for lev in LOG_LEVELS:
        logging.addLevelName(getattr(logging, lev), f"{lev[0] * 2}")

    logging.setLoggerClass(CustomLogger)

    # log().setLevel(getattr(logging, level.split("_")[-1]))
    # stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(getattr(logging, level.split("_")[-1]))
    # stream_handler.setFormatter(
    #    logging.Formatter(
    #        "(%(levelname)s) %(asctime)s | %(posixTID)d | %(stack)s: %(message)s",
    #        datefmt="%Y-%m-%d %H:%M:%S",
    #    )
    # )
    # log().handlers = [stream_handler]
    # logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

    # https://stackoverflow.com/questions/76788727/how-can-i-change-the-debug-level-and-format-for-the-quart-i-e-hypercorn-logge
    # https://pgjones.gitlab.io/hypercorn/how_to_guides/logging.html#how-to-log
    # https://www.phind.com/agent?cache=clkqhh48y001smg0832tvq1rl

    # from quart.logging import default_handler
    # logging.getLogger('quart.app').removeHandler(default_handler)
    # logger = logging.getLogger("hypercorn.error")
    # logger.removeHandler(default_handler)
    # logger.addHandler(ch)
    # logger.setLevel(logging.WARNING)
    # logger.propagate = False


def print_stacktrace_on_signal(sig: int, frame: None | FrameType) -> None:
    """interrupt running process, and provide a python prompt for
    interactive debugging.
    see http://stackoverflow.com/questions/132058
       "showing-the-stack-trace-from-a-running-python-application"
    """
    import asyncio  # pylint: disable=import-outside-toplevel

    try:
        print(f"signal {sig} received - print stack trace", file=sys.stderr)

        def print_stack_frame(stack_frame: None | FrameType, file: TextIO) -> None:
            """Print a single stack frame"""
            for _f in traceback.format_stack(stack_frame):
                for _l in _f.splitlines():
                    print(_l, file=file)

        def print_stack_frames(file: TextIO) -> None:
            """Print all stack frames"""
            print("++++++ MAIN ++++++++", file=file)
            print_stack_frame(frame, file)
            for task in asyncio.all_tasks():
                coro = task.get_coro()
                print(f"++++++ task: '{task.get_name()}', coro={coro} ++++++++", file=file)
                for stack in task.get_stack(limit=1000):
                    print_stack_frame(stack, file)

        print_stack_frames(sys.stderr)
        # with open(Path("traceback.log").expanduser(), "w") as trace_file:
        # print_stack_frames(trace_file)
        # print(f"traceback also written to {trace_file}", file=sys.stderr)
    except Exception:  # pylint: disable=broad-except
        log().exception("Could not fully write application stack trace")


def setup_introspection_on_signal() -> None:
    """Install signal handlers for some debug stuff"""

    def setup_signal(sig: int, func: Callable[[int, FrameType | None], None], msg: str) -> None:
        signal.signal(sig, func)
        signal.siginterrupt(sig, False)
        sig_str = "USR1" if sig == signal.SIGUSR1 else "USR2" if sig == signal.SIGUSR2 else str(sig)
        print(f"Run `kill -{sig_str} {os.getpid()}` to {msg}", file=sys.stderr)

    # setup_signal(signal.SIGUSR1, increase_loglevel, "increase log level")
    setup_signal(signal.SIGUSR2, print_stacktrace_on_signal, "print stacktrace")
