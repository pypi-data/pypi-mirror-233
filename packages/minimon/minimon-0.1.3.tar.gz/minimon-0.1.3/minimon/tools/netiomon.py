#!/usr/bin/env python3

"""
Technical stuff:
- How to Make a Network Usage Monitor in Python
  https://thepythoncode.com/article/make-a-network-usage-monitor-in-python
- With command line tools + scripting, what's a possible/good way to gather endpoint, process and
  bandwidth information about network connections?
  https://stackoverflow.com/questions/77059315
- A Linux resource monitor based on Python language!
  https://www.fatalerrors.org/a/a-linux-resource-monitor-based-on-python-language.html
- Python Textual (TUI) https://juejin.cn/column/7098899902477893646
"""

# pylint: disable=too-many-locals,fixme,too-many-instance-attributes,protected-access
# mypy: ignore-errors

import asyncio
import logging
import socket
import sys
import time
from collections.abc import AsyncIterator, MutableMapping
from contextlib import suppress
from dataclasses import dataclass

import psutil
from rich.logging import RichHandler
from scapy.all import AsyncSniffer, Packet, Scapy_Exception, ifaces  # type: ignore
from textual import work
from textual.app import App, ComposeResult

# from textual.renderables.sparkline import SparklineRenderable
from textual.widgets import Footer, Header, RichLog

from minimon.machinery import bundle, throttle


def log() -> logging.Logger:
    """Returns the logger instance to use here"""
    return logging.getLogger("netiomon")


@dataclass
class Connection:
    """All information we want to know about a connection needed to identify one"""

    created: int
    socket_fd: int
    process_uid: str
    process_pid: int
    process_name: str
    local_ip: str
    local_port: int
    remote_ip: str
    remote_port: int
    remote_host: None | str
    bytes_sent: int
    bytes_recieved: int

    def uid(self) -> str:
        """A human lovable unique identifier"""
        return f"{self.created}-{self.local_port}-{self.remote_port}"

    def __str__(self) -> str:
        return (
            f"Connection(index=[{self.local_port},{self.remote_port}],"
            f" {self.process_name}({self.process_pid}) <==>"
            f" {self.remote_host[0] if self.remote_host else '?'}({self.remote_ip}),"
            f" r={self.bytes_recieved}, s={self.bytes_sent})"
        )

    def __repr__(self) -> str:
        return str(self)


def domain_from(ip_address: str) -> None | str:
    """A readable domain name from given IP address"""
    with suppress(socket.herror, OSError):
        return socket.gethostbyaddr(ip_address)[0]
    return None


class NetIOStats:
    """The network stats generator"""

    def __init__(self) -> None:
        self.connection: MutableMapping[tuple[int, int], Connection] = {}
        self.per_process: MutableMapping[
            str, tuple[tuple[str, ...], MutableMapping[str, Connection]]
        ] = {}

    def __enter__(self) -> "NetIOStats":
        return self

    def __exit__(self, *args: object) -> bool:
        if sys.exc_info() != (None, None, None):
            raise
        return True

    async def monitor_connections(self) -> AsyncIterator[tuple[str, Connection]]:
        """Continuously collect all open connections"""
        while True:
            connections = {
                (conn.laddr.port, conn.raddr.port): conn
                for conn in psutil.net_connections()
                if conn.laddr and conn.raddr and conn.pid
            }

            for index, connection in list(self.connection.items()):
                if index not in connections:
                    del self.connection[index]
                    yield "vanished", connection

            for index, conn in connections.items():
                if index in self.connection:
                    # todo: check pid/process
                    continue

                process = psutil.Process(conn.pid)

                connection = Connection(
                    int(time.time() * 1000),
                    conn.fd,
                    f"{process.create_time}-{process.pid}-{process.name()}",
                    process.pid,
                    process.name(),
                    conn.laddr.ip,
                    conn.laddr.port,
                    conn.raddr.ip,
                    conn.raddr.port,
                    domain_from(conn.raddr.ip),
                    0,
                    0,
                )
                self.connection[index] = connection
                yield "new", connection
            await asyncio.sleep(1)

    @staticmethod
    async def async_sniffer() -> AsyncIterator[Packet]:
        """Watch for packages and handle them"""
        queue: asyncio.Queue[Packet] = asyncio.Queue()

        def add_to_queue(packet: Packet) -> None:
            """Adds @packet to message queue in a thread aware manner"""
            queue.put_nowait(packet)
            queue._loop._write_to_self()  # type: ignore

        sniffer = AsyncSniffer(prn=add_to_queue, store=False, filter="tcp")
        try:
            sniffer.start()
            while packet := await queue.get():
                yield packet
        except PermissionError:
            log().error("Permission error")
        except KeyboardInterrupt:
            pass
        finally:
            with suppress(Scapy_Exception):
                sniffer.stop()

    async def monitor_traffic(self) -> AsyncIterator[Connection]:
        """Enrich connection information with actual traffic data"""
        all_macs = {iface.mac for iface in ifaces.values()}
        packet: Packet
        async for packet in self.async_sniffer():
            assert packet.src in all_macs or packet.dst in all_macs

            if packet.src in all_macs and packet.dst in all_macs:
                if connection := self.connection.get((packet.sport, packet.dport)):
                    connection.bytes_sent += len(packet)
                elif connection := self.connection.get((packet.dport, packet.sport)):
                    connection.bytes_recieved += len(packet)
                else:
                    # log().warning("missed local [%s, %s]", packet.sport, packet.dport)
                    continue
            elif packet.src in all_macs:
                if not (connection := self.connection.get((packet.sport, packet.dport))):
                    # log().warning("missed remote [%s, %s]", packet.sport, packet.dport)
                    continue
                connection.bytes_sent += len(packet)
            else:  # packet.dst in all_macs
                if not (connection := self.connection.get((packet.dport, packet.sport))):
                    # log().warning("missed remote [%s, %s]", packet.sport, packet.dport)
                    continue
                connection.bytes_recieved += len(packet)

            yield connection

    async def __aiter__(self) -> AsyncIterator[None]:
        async for source, data in bundle(
            connection=self.monitor_connections(),
            traffic=self.monitor_traffic(),
        ):
            if source == "connection":
                action, connection = data
                assert isinstance(connection, Connection)
                if action == "new":
                    connections = self.per_process.setdefault(
                        connection.process_uid,
                        ((connection.process_pid, connection.process_name), {}),
                    )[1]
                    connections[connection.uid()] = connection
                elif action == "vanished":
                    connections = self.per_process[connection.process_uid][1]
                    del connections[connection.uid()]
                    if len(connections) == 0:
                        del self.per_process[connection.process_uid]
            yield


class RichLogHandler(RichHandler):
    """Redirects rich.RichHanlder capabilities to a textual.RichLog"""

    def __init__(self, widget: RichLog):
        super().__init__(show_path=False, markup=False, show_time=False, show_level=False)
        self.widget: RichLog = widget

    def emit(self, record: logging.LogRecord) -> None:
        self.widget.write(
            self.render(
                record=record,
                message_renderable=self.render_message(record, self.format(record)),
                traceback=None,
            )
        )


class NetIOMon(App[None]):
    """Nice UI for NetIOMon"""

    CSS_PATH = "netiomon.css"

    def __init__(self) -> None:
        super().__init__()
        #        self.msg_queue = msg_queue
        # random.seed(73)
        # self.data = [random.expovariate(1 / 3) for _ in range(100)]
        # self._sparkline = Sparkline(self.data, summary_function=max)
        self._monlog = RichLog(id="monitor")
        self._loglog = RichLog(id="log")

    def compose(self) -> ComposeResult:
        # yield self._sparkline
        yield Header(show_clock=True)
        yield self._monlog
        yield self._loglog
        yield Footer()

    @work(exit_on_error=True)
    async def produce(self) -> None:
        """The actual monitoring main loop"""
        with NetIOStats() as stats:
            async for _ in throttle(aiter(stats), min_interval=0.2):
                # print(update)
                # self._log.write(update)
                self._monlog.clear()
                for process, connections in stats.per_process.values():
                    self._monlog.write(f"{' '.join(map(str, process))}:")
                    for conn in connections.values():
                        endpoint_str = conn.remote_host and conn.remote_host or conn.remote_ip
                        self._monlog.write(
                            f"    {endpoint_str:60s}"
                            f"{conn.bytes_recieved:12d}{conn.bytes_sent:12d}"
                        )

    async def on_mount(self) -> None:
        """UI entry point"""

        def fmt_filter(record: logging.LogRecord) -> bool:
            record.levelname = f"[{record.levelname}]"
            record.funcName = f"[{record.funcName}]"
            return True

        logging.getLogger().setLevel(logging.WARNING)
        log().setLevel(logging.DEBUG)

        logging.getLogger().handlers = [handler := RichLogHandler(self._loglog)]
        handler.setFormatter(
            logging.Formatter(
                "%(levelname)-9s %(asctime)s %(funcName)-12s| %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        handler.addFilter(fmt_filter)

        self.produce()


async def amain() -> None:
    """Entry point for headless (text-only) output"""
    with NetIOStats() as stats:
        async for update in stats:
            print(update)


if __name__ == "__main__":
    # cli_args = parse_arguments()

    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(NetIOMon().run_async())
