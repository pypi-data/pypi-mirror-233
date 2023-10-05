#!/usr/bin/env python3
# pylint: disable=wildcard-import,unused-wildcard-import

""" Monitor my private infrastructure
Todo
- wth: monitor networks
"""
# pylint: disable=unused-import

from minimon.builder import (
    AInsights,
    Bundler,
    Host,
    Insight,
    LocalHost,
    Monitor,
    Pipeline,
    StrSeq,
    process_output,
    view,
)
from minimon.plugins import (
    check_df,
    check_dmesg,
    check_ps,
    parse_df,
    parse_dmesg,
    parse_ps,
)

hosts = (
    # LocalHost(),
    # Host("localhost"),
    # Host("localhost", ssh_name="root"),
    Host("om-office.de", ssh_port=2222),
    # Host("zentrale", ssh_name="pi"),
    # Host("reMarkable"),
    # Host("handy", ssh_name="frans"),
)

with Monitor("Private inf"):

    # @view("host", hosts)  # type: ignore[arg-type]
    # async def network_traffic(host: Host) -> Insights:
    # """Provides quick summary of system sanity"""
    # async for _ in Pipeline[StrSeq](
    # process_output(host, "ss --oneline --numeric --resolve --processes --info", "3"),
    # processor=parse_ss,
    # ):
    # yield {}

    @view("host", hosts)  # type: ignore[arg-type]
    async def local_resources(host: Host) -> AInsights:
        """Provides quick summary of system sanity"""
        async for _, insight in Bundler(
            df=Pipeline(process_output(host, "df -P", "2")).chain(parse_df).chain(check_df),
            # dos=Pipeline(process_output(host, "while true; do date; done", "1")),
            ps=Pipeline(process_output(host, "ps ww", "1")).chain(parse_ps).chain(check_ps),
            # dmesg=Pipeline(process_output(host, "dmesg -w", "2")).chain(parse_dmesg),
        ):
            yield insight
