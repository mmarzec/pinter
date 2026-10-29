# Pinter - Print INTERfaces

Pinter is a small CLI tool that prints your network interfaces and their IP addresses in a clean, colored table. Forget about digging through `ifconfig` or `ip addr` output.

By default it shows only the interfaces that usually matter (Ethernet, Wi-Fi, bridges, VPN tunnels) and hides noise such as loopback, Docker and other virtual interfaces.

## Features

- One line per interface, aligned columns, colored output
- All IPv4 addresses of an interface, when it has more than one
- Optional MAC addresses
- Optional view of all interfaces, without filtering
- Only one dependency: [psutil](https://github.com/giampaolo/psutil)

## Installation

Install with `pipx` (preferred) or `pip`:

```console
pipx install pinter
```

```console
pip install pinter
```

Requires Python 3.8 or newer.

## Usage

```console
pinter [options]
```

Options are single letters and can be combined in one argument, for example `pinter am`:

| Option | Description                                         |
|--------|-----------------------------------------------------|
| `a`    | Show all interfaces (no filtering)                  |
| `m`    | Also print MAC addresses                            |
| `h`    | Print help                                          |

### Default view

Shows only the important interfaces:

```console
$ pinter
enp1s0  192.168.1.23
        192.168.1.24
wlp2s0  192.168.1.57
tun0    10.8.0.2
```

Interfaces whose names start with `lo`, `docker`, `veth`, `br-`, `virbr` or `vnet`
(loopback, containers and VM plumbing) are hidden. Everything else is shown.
If nothing is left to show, pinter says so and suggests `pinter a`.


### All interfaces

```console
$ pinter a
lo       127.0.0.1
enp1s0   192.168.1.23
wlp2s0   192.168.1.57
docker0  172.17.0.1
```

### With MAC addresses

```console
$ pinter m
enp1s0  192.168.1.23  52:54:00:12:34:56
wlp2s0  192.168.1.57  a4:c3:f0:65:43:21
```

### All interfaces with MAC addresses

```console
$ pinter am
lo       127.0.0.1     00:00:00:00:00:00
enp1s0   192.168.1.23  52:54:00:12:34:56
wlp2s0   192.168.1.57  a4:c3:f0:65:43:21
docker0  172.17.0.1    02:42:7a:1b:2c:3d
```

## License

MIT, see [LICENSE](LICENSE).
