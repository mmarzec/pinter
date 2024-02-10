import psutil
import socket
import sys


def collect_intf_addresses(include_all=False):
    interfaces_psutil = psutil.net_if_addrs()

    intf_addresses = {}

    # get all interfaces names
    intf_names = (intf[1] for intf in socket.if_nameindex())

    # filter
    if not include_all:
        intf_names = (intf for intf in intf_names if intf.startswith(('enp', 'eth', 'wl', 'eno', 'br', 'tun')))
        intf_names = (intf for intf in intf_names if not intf.startswith(('br-')))

    # get addresses
    for intf in intf_names:
        intf_addresses[intf] = {'ip': [], 'mac': ''}
        for address in interfaces_psutil[intf]:
            if address.family == socket.AF_INET:
                intf_addresses[intf]['ip'].append(address.address)
            elif address.family == socket.AF_PACKET:
                intf_addresses[intf]['mac'] = address.address

    return intf_addresses


def print_help():
    print(f'''Description:
  Print network interfaces and ip addresses

Usage:
  pinter [options]

Options:
  a  all interfaces
  h  help
  m  print mac addresses

''')


def cli():

    # cli options
    options = ''
    if len(sys.argv) > 1:
        options = sys.argv[1]

    include_all = None
    if 'a' in options:
        include_all = True

    if 'h' in options:
        print_help()

    include_mac = False
    if 'm' in options:
        include_mac = True

    intf_addresses = collect_intf_addresses(include_all)
    intf_col_width = len(max(intf_addresses.keys(), key=len))
    ip_col_width = len(max([ip for intf in intf_addresses for ip in intf_addresses[intf]['ip']], key=len))

    for intf in intf_addresses:
        if not intf_addresses[intf]['ip']:
            intf_addresses[intf]['ip'].append('')

        # print first row
        row = f'{intf:<{intf_col_width}}  \033[36m{intf_addresses[intf]["ip"][0]:<{ip_col_width}}\033[0m'

        if include_mac:
            row = f'{row}  \033[35m{intf_addresses[intf]["mac"]}\033[0m'
        print(row)

        # print rest rows
        for ip_addr in intf_addresses[intf]['ip'][1:]:
            print(f'{"":<{intf_col_width}}  \033[36m{ip_addr}\033[0m')
