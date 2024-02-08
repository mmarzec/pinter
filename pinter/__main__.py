import psutil
import socket


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
    intf_addresses = collect_intf_addresses()
    intf_col_width = len(max(intf_addresses.keys(), key = len))
    addr_col_width = len(max(intf_addresses.values(), key = lambda x: len(x) if x else 0))
    for intf in intf_addresses:
        print(f'{intf:<{intf_col_width}}  \033[36m{intf_addresses[intf] or "":<{addr_col_width}}\033[0m')
