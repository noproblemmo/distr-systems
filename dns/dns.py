"""DNS prototype."""


class NetworkInterface:
    """Network interface."""

    def __init__(self):
        self.net = None
        self.addr = None
        self.dns = None

    def setup(self, net, addr):
        """Set net and address to interface."""
        self.net = net
        self.addr = addr

    def set_dns(self, addr):
        # TODO docs:
        self.dns = addr

    def resolve(self, name):
        # TODO docs:
        return self.net.resolve(self.dns, name)


class Comp:
    """Computer."""
    def __init__(self):
        self.__iface = NetworkInterface()
        self.__local_db = None

    def set_net(self, net, addr):
        """Connect computer to net."""
        self.__iface.setup(net, addr)

    def ping(self, addr):
        """Send ping to address."""

        if not self.__iface.net:
            return "No network"

        return self.__iface.net.ping(
            self.__iface.addr, addr)

    def resolve(self, name):
        # TODO docs:
        if self.__local_db:
            addr = self.__local_db.resolve(name)
            if addr:
                return addr

        if not self.__iface.net:  # TODO: FIX
            return None

        return self.__iface.resolve(name)

    def set_dns_db(self, db):
        # TODO docs:
        self.__local_db = db

    def set_dns_server(self, addr):
        # TODO ref: access to iface
        self.__iface.set_dns(addr)


class Net:
    """Net represents net."""

    def __init__(self):
        self.__hosts = {}

    def add_host(self, comp, addr):
        """Add host to net."""
        self.__hosts[addr] = comp
        comp.set_net(self, addr)

    def ping(self, src, dst):
        """Ping sends ping to host."""
        if dst in self.__hosts:
            return f"ping from {src} to {dst}"

        return "Unknown host"

    def resolve(self, dns_addr, name):
        # TODO test: no host
        try:
            return self.__hosts[dns_addr].resolve(name)
        except KeyError:
            return None


class Record:
    """DNS record."""
    def __init__(self, name, addr):
        self.__name = name
        self.__addr = addr

    def get_name(self):
        return self.__name

    def get_addr(self):
        return self.__addr

    # TODO feat: ? + update_record()


class DnsDb:
    """DNS database."""
    def __init__(self):
        self.__records = {}
        self.__addrs = {}

    def num_records(self):
        """Return number of records."""
        return len(self.__records)

    def add_record(self, record):
        """Add record."""
        self.__check_record(record)
        self.__records[record.get_name()] = record

    def resolve(self, name):
        """Return IP address by name."""
        try:
            return self.__records[name].get_addr()
        except KeyError:
            return None

    def __check_record(self, record):
        if record.get_addr() in self.__addrs:
            raise ValueError("Duplicated address")
        self.__addrs[record.get_addr()] = True
