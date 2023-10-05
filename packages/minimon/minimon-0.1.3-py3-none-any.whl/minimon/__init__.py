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

"""Used for lazy wildcard import only"""

# pylint: disable=wrong-import-position

# this crazy shit is needed because asyncio will run code (logging setup) upon import and we have
# to be first...
from minimon.logging_utils import setup_logging

setup_logging()

from minimon.builder import (
    AInsights,
    Bundler,
    Host,
    Hosts,
    Insight,
    Insights,
    LocalHost,
    Monitor,
    Pipeline,
    StrIter,
    StrSeq,
    process_output,
    view,
)

__all__ = [
    "Host",
    "Hosts",
    "LocalHost",
    "Insight",
    "Insights",
    "AInsights",
    "Monitor",
    "Pipeline",
    "StrSeq",
    "StrIter",
    "Bundler",
    "process_output",
    "view",
]
