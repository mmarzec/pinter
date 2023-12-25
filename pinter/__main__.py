import psutil
import socket
from rich.console import Console
from rich.table import Table


def collect_intf_addresses():
    interfaces_psutil = psutil.net_if_addrs()

    intf_addresses = {}

    # get all interfaces names
    intf_names = (intf[1] for intf in socket.if_nameindex())

    # filter
    intf_names = (intf for intf in intf_names if intf.startswith(('enp', 'eth', 'wl', 'eno', 'br', 'tun')))
    intf_names = (intf for intf in intf_names if not intf.startswith(('br-')))

    # get addresses
    for intf in intf_names:
        intf_addresses[intf] = None
        for address in interfaces_psutil[intf]:
            if address.family == socket.AF_INET:
                intf_addresses[intf] = address.address

    return intf_addresses


def cli():
    table = Table(box=None)
    table.add_column()
    table.add_column(style="cyan")
    intf_addresses = collect_intf_addresses()
    for intf in intf_addresses:
        table.add_row(intf, intf_addresses[intf])
    console = Console()
    console.print(table)
