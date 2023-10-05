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

"""Provides generic machinery to spawn a bunch of local or remote monitoring processes in a
minimon application context
"""
# pylint: disable=too-few-public-methods,fixme

import argparse
import asyncio
import functools
import logging
import shlex
import sys
from asyncio import StreamReader
from asyncio.subprocess import PIPE, create_subprocess_exec
from collections.abc import AsyncIterable, AsyncIterator, Callable, Iterable, Sequence
from contextlib import suppress
from dataclasses import dataclass
from itertools import count
from typing import Any, TypeAlias

import asyncssh

from minimon.machinery import Bundler, Pipeline, StrIter, StrSeq, throttle
from minimon.server import AInsights, Context, Insight, Insights, Singleton, async_serve

__all__ = [
    "Monitor",
    "GlobalMonitorContext",
    "Pipeline",
    "Host",
    "Hosts",
    "LocalHost",
    "Insight",
    "Insights",
    "AInsights",
    "StrSeq",
    "StrIter",
    "view",
    "process_output",
    "Bundler",
]


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("minimon")


Args = argparse.Namespace


class GlobalMonitorContext(Context, metaclass=Singleton):
    """A singleton minimon application context"""


@dataclass
class Host:
    """Specification of a remote host with everything needed to establish an SSH connection"""

    name: str
    ip_address: None | str
    ssh_name: None | str
    ssh_key_file: None | str
    ssh_key_passphrase_cmd: None | str
    ssh_port: None | int
    use_ssh: bool

    def __init__(
        self,
        name: str,
        *,
        ip_address: None | str = None,
        ssh_name: None | str = None,
        ssh_key_file: None | str = None,
        ssh_key_passphrase_cmd: None | str = None,
        ssh_port: None | int = None,
        use_ssh: bool = True,
    ):
        self.name = name
        self.ip_address = ip_address or name
        self.ssh_name = ssh_name
        self.ssh_key_file = ssh_key_file
        self.ssh_key_passphrase_cmd = ssh_key_passphrase_cmd
        self.ssh_port = ssh_port
        self.use_ssh = use_ssh

    def __str__(self) -> str:
        name_str = f"{self.ssh_name}@" if self.ssh_name else ""
        return f"{name_str}{self.ip_address}-{'ssh' if self.use_ssh else 'local'}"


Hosts: TypeAlias = Sequence[Host]


class LocalHost(Host):
    """Convenience wrapper for Host"""

    def __init__(self) -> None:
        super().__init__("localhost", use_ssh=False)


class RemoteConnectionError(RuntimeError):
    """Raised when something's going wrong with a SSH connection"""


# https://realpython.com/primer-on-python-decorators/#syntactic-sugar
def view(
    arg_name: str, arg_values: Sequence[object]
) -> Callable[[Callable[[object], AsyncIterator[Insight]]], None]:
    """A decorator generating a minimon view for each value in @arg_values"""

    def decorator_view(afunc: Callable[[object], AsyncIterator[Insight]]) -> None:
        @functools.wraps(afunc)
        async def wrapper_view(*args: object, **kwargs: object) -> AsyncIterator[Insight]:
            while True:  # todo: handle elsewhere
                generator = afunc(*args, **kwargs)
                while True:
                    try:
                        yield await anext(generator)
                    except StopAsyncIteration:
                        log().info("StopAsyncIteration in %s", afunc.__name__)
                        return
                    except RemoteConnectionError as exc:
                        log().error("Connection failed: %s", exc)
                        await asyncio.sleep(5)  # todo: handle elsewhere
                    except Exception:  # pylint: disable=broad-except
                        log().exception("Unhandled exception in view generator:")
                        await asyncio.sleep(5)  # todo: handle elsewhere

        fn_name = afunc.__name__
        for arg_value in arg_values:
            GlobalMonitorContext().add(
                f"{fn_name}-{arg_value}", wrapper_view(**{arg_name: arg_value})
            )

    return decorator_view


class HostConnection:
    """An SSH connection to a given @host"""

    def __init__(self, host: Host, log_fn: Callable[[StrIter], None]) -> None:
        self.host_info = host
        self.log_fn = log_fn
        self.ssh_connection: None | asyncssh.SSHClientConnection = None

    async def __aenter__(self) -> "HostConnection":
        if self.host_info.use_ssh:
            remote_str = (
                f"{f'{self.host_info.ssh_name}@' if self.host_info.ssh_name else ''}"
                f"{self.host_info.ip_address}"
                f"{f':{self.host_info.ssh_port}' if self.host_info.ssh_port else ''}"
            )
            log().info("connect to remote %s", remote_str)
            try:
                self.ssh_connection = await asyncssh.connect(
                    self.host_info.ip_address,
                    **{
                        key: value
                        for key, value in (
                            ("port", self.host_info.ssh_port),
                            ("username", self.host_info.ssh_name),
                            # client_keys=[pkey],
                        )
                        if value is not None
                    },
                    keepalive_interval=2,
                    keepalive_count_max=2,
                )

            except asyncssh.PermissionDenied as exc:
                raise RemoteConnectionError(f"PermissionDenied({remote_str})") from exc
            except asyncssh.HostKeyNotVerifiable as exc:
                raise RemoteConnectionError(
                    f"Cannot connect to {self.host_info.name}: {exc}"
                ) from exc
            except OSError as exc:
                raise RemoteConnectionError(f"OSError({remote_str}): {exc}") from exc

        return self

    async def __aexit__(self, *args: object) -> bool:
        log().debug("close connection")
        if self.ssh_connection:
            self.ssh_connection.close()
        return True

    @staticmethod
    def clean_lines(raw_lines: Iterable[str], log_fn: Callable[[StrIter], None]) -> StrSeq:
        """Sanatize and log a str line"""
        lines = [raw_line.strip("\n") for raw_line in raw_lines]
        log_fn(lines)
        return lines

    @staticmethod
    def clean_bytes(raw_lines: Iterable[bytes], log_fn: Callable[[StrIter], None]) -> StrSeq:
        """Sanatize and log a bytes line"""
        lines = [raw_line.decode().strip("\n") for raw_line in raw_lines]
        log_fn(lines)
        return lines

    async def listen(
        self,
        stream: StreamReader | asyncssh.SSHReader[Any],
        clean_fn: Callable[[Iterable[bytes], Callable[[StrIter], None]], StrSeq]
        | Callable[[Iterable[str], Callable[[StrIter], None]], StrSeq],
    ) -> StrSeq:
        """Creates a sanatized list of strings from something iterable and logs on the go"""
        return [
            line
            async for raw_lines in throttle(aiter(stream), min_interval=3, bucket_size=5)
            for line in clean_fn(raw_lines, self.log_fn)
        ]

    async def execute(self, command: str) -> tuple[StrSeq, StrSeq, int]:
        """Executes @command via ssh connection if specified else locally"""
        if self.ssh_connection:
            # todo: catch channelopenerror
            ssh_process = await self.ssh_connection.create_process(command)
            assert ssh_process.stdout and ssh_process.stderr
            try:
                log().debug("run command via SSH..")
                stdout, stderr, completed = await asyncio.gather(
                    self.listen(ssh_process.stdout, self.clean_lines),
                    self.listen(ssh_process.stderr, self.clean_lines),
                    asyncio.ensure_future(ssh_process.wait()),
                )
                assert completed.returncode is not None
                return stdout, stderr, completed.returncode
            finally:
                log().debug("terminate() remote process '%s'..", command)
                ssh_process.terminate()

        log().debug("run command '%s' locally..", command)
        process = await create_subprocess_exec(*shlex.split(command), stdout=PIPE, stderr=PIPE)
        assert process.stdout and process.stderr
        try:
            return await asyncio.gather(
                self.listen(process.stdout, self.clean_bytes),
                self.listen(process.stderr, self.clean_bytes),
                process.wait(),
            )
        finally:
            log().debug("terminate() local process '%s'..", command)
            with suppress(ProcessLookupError):
                process.terminate()


async def process_output(
    host: Host,
    command: str,
    when: None | str = None,
) -> AsyncIterable[StrSeq]:
    """Executes a process defined by @command on @host in a manner specified by @when"""
    iterations = None
    interval = float(when) if when is not None else None

    try:
        async with HostConnection(host, GlobalMonitorContext().ctx_log_fn()) as connection:
            for iteration in count():
                if iterations is not None and iteration >= iterations:
                    break

                log().info("start task %r: %d", command, iteration)
                try:
                    stdout, _, return_code = await connection.execute(command)
                    log().debug("task %r: %d, returned %d", command, iteration, return_code)
                    yield stdout
                except Exception:  # pylint: disable=broad-except
                    log().exception("Executing command %s resulted in unhandled exception", command)
                    raise

                if interval is not None:
                    await asyncio.sleep(interval)
    except asyncssh.HostKeyNotVerifiable as exc:
        log().error("%s", exc)


def parse_args() -> Args:
    """Cool git like multi command argument parser"""
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument(
        "--log-level",
        "-l",
        choices=["ALL_DEBUG", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
        help="Sets the logging level - ALL_DEBUG sets all other loggers to DEBUG, too",
        type=str.upper,
    )

    return parser.parse_args()


def in_doctest() -> bool:
    """Self-introspect to find out if we're in the Matrix"""
    if "_pytest.doctest" in sys.modules:
        return True
    ##
    if hasattr(sys.modules["__main__"], "_SpoofOut"):
        return True
    ##
    if sys.modules["__main__"].__dict__.get("__file__", "").endswith("/pytest"):
        return True
    ##
    return False


class Monitor:
    """Top level application context, instantiating the monitoring application"""

    def __init__(self, name: str, log_level: str = "INFO") -> None:
        if not in_doctest():
            args = parse_args()
            self.name = name
            self.log_level = args.log_level or log_level or "INFO"

    def __enter__(self) -> "Monitor":
        return self

    def __exit__(self, *args: object) -> bool:
        if in_doctest():
            return True

        if sys.exc_info() != (None, None, None):
            raise

        asyncio.run(async_serve(GlobalMonitorContext(), self.log_level))
        return True
