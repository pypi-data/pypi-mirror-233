#!/usr/bin/env python3
# pylint: disable=wildcard-import,unused-wildcard-import

""" A minimal viable monitor"""

from minimon import *
from minimon.plugins import *

with Monitor("MVM"):

    @view("host", [Host("localhost")])  # type: ignore[arg-type]
    async def local_resources(host: Host) -> AInsights:
        """This async generator will be invoked by the above `view` and run continuously to
        gather and yield monitoring data"""
        async for _, insight in Bundler(
            ps=Pipeline(process_output(host, "ps wauxw", "1")).chain(parse_ps).chain(check_ps),
            df=Pipeline(process_output(host, "df -P", "2")).chain(parse_df).chain(check_df),
        ):
            yield insight
