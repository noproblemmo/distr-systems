"""Computer."""


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
        """Set DNS server."""
        self.dns = addr

    def resolve(self, name):
        """Resolve name."""
        if not self.net:
            return None

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
        """Resolve name."""
        if self.__local_db:
            addr = self.__local_db.resolve(name)
            if addr:
                return addr

        return self.__iface.resolve(name)

    def set_dns_db(self, db):
        """Set DNS db."""
        self.__local_db = db

    def set_dns_server(self, addr):
        """Set DNS server."""
        self.__iface.set_dns(addr)
