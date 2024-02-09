import psutil
import socket
import sys


def collect_intf_addresses(iall=None):
    interfaces_psutil = psutil.net_if_addrs()

    intf_addresses = {}

    # get all interfaces names
    intf_names = (intf[1] for intf in socket.if_nameindex())

    # filter
    if not iall:
        intf_names = (intf for intf in intf_names if intf.startswith(('enp', 'eth', 'wl', 'eno', 'br', 'tun')))
        intf_names = (intf for intf in intf_names if not intf.startswith(('br-')))

    # get addresses
    for intf in intf_names:
        intf_addresses[intf] = []
        for address in interfaces_psutil[intf]:
            if address.family == socket.AF_INET:
                intf_addresses[intf].append(address.address)

    return intf_addresses


def print_help():
    print(f'''Description:
  Print network interfaces and ip addresses

Usage:
  pinter [options]

Options:
  a  all interfaces
  h  help

''')


def cli():

    # cli options
    options = ''
    if len(sys.argv) > 1:
        options = sys.argv[1]

    iall = None
    if 'a' in options:
        iall = True

    if 'h' in options:
        print_help()

    intf_addresses = collect_intf_addresses(iall)
    intf_col_width = len(max(intf_addresses.keys(), key = len))
    for intf in intf_addresses:
        if not intf_addresses[intf]:
            intf_addresses[intf].append('')

        # print first ip
        print(f'{intf:<{intf_col_width}}  \033[36m{intf_addresses[intf][0]}\033[0m')

        # print rest ips
        for ip_addr in intf_addresses[intf][1:]:
            print(f'{"":<{intf_col_width}}  \033[36m{ip_addr}\033[0m')
