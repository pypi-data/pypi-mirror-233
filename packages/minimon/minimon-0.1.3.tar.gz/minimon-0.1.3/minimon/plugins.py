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

""" Some little helper functions for checks
"""
from collections.abc import Iterable, Sequence
from typing import TypeAlias

from minimon.builder import Insights, StrSeq

ParsedDfType: TypeAlias = tuple[str, str, float]


def parse_df(lines: StrSeq) -> Iterable[Sequence[ParsedDfType]]:
    """
    Filesystem     1K-blocks      Used Available Use% Mounted on
    /dev/dm-0      981723644 814736524 117044544  88% /
    """
    yield [
        (mountpoint, device, use)
        for line in lines[1:]
        for elems in (line.split(),)
        if len(elems) > 5
        for mountpoint, device, use in ((elems[5], elems[0], int(elems[4][:-1])),)
    ]


def check_df(mountpoints: Sequence[ParsedDfType]) -> Insights:
    """Returns insights from preprocessed `df` output"""
    for mountp, dev, use in mountpoints:
        if dev not in {"tmpfs", "devtmpfs"}:
            yield (("info" if use < 80 else "warn"), f"{mountp} ({use}%)")


ParsedPsType: TypeAlias = tuple[str, float, float, str]


def parse_ps(lines: StrSeq) -> Iterable[Sequence[ParsedPsType]]:
    """
    USER  PID %CPU %MEM    VSZ   RSS TTY STAT START   TIME COMMAND
    root    1  0.0  0.0 173724  9996 ?   Ss   Aug13   0:04 /usr/lib/systemd rhgb --deserialize 31
    """
    yield [
        (user, cpu, mem, cmd)
        for line in lines[1:]
        for elems in (line.split(maxsplit=10),)
        if len(elems) > 10
        for user, cpu, mem, cmd in ((elems[0], float(elems[2]), float(elems[3]), elems[10]),)
    ]


def check_ps(processes: Sequence[ParsedPsType]) -> Insights:
    """Returns insights from preprocessed `ps` output"""
    for user, cpu, mem, cmd in processes:
        yield (("info" if cpu < 20 else "warn"), f"{user} {cpu} {mem} {cmd.split(maxsplit=1)[0]}")


ParsedDmesgType: TypeAlias = tuple[float, str, str]


def parse_dmesg(lines: StrSeq) -> Iterable[ParsedDmesgType]:
    """Extract usable data from dmesg lines
    >>> for parsed in parse_dmesg([
    ...   '[2122875.911999] Restarting tasks ... ',
    ...   '[2122875.912413] usb 3-6: USB disconnect, device number 41',
    ...   '[2122875.916483] done.',
    ... ]):
    ...     print(parsed)
    (2122875.911999, 'Restarting', 'tasks ... ')
    (2122875.912413, 'usb', '3-6: USB disconnect, device number 41')
    (2122875.916483, 'done.', '')
    """
    for line in lines:
        ts_raw, first, *rest = line.split(" ", maxsplit=2)
        yield float(ts_raw[1:-1]), first, " ".join(rest)


def check_dmesg(messages: ParsedDmesgType) -> Insights:
    """Yields insights from preprocessed incoming `dmesg` lines"""
    timestamp, source, message = messages
    print(timestamp, source, message)
    yield "info", "dummy"
