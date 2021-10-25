"""DNS prototype."""


class NetworkInterface:
    def __init__(self):
        self.net = None
        self.addr = None

    def setup(self, net, addr):
        """Set net and address to interface."""
        self.net = net
        self.addr = addr


class Comp:
    """Computer."""
    def __init__(self):
        self.__iface = NetworkInterface()

    def set_net(self, net, addr):
        """Connect computer to net."""
        self.__iface.setup(net, addr)

    def ping(self, addr):
        """Send ping to address."""

        if not self.__iface.net:
            return "No network"

        return self.__iface.net.ping(
            self.__iface.addr, addr)


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
