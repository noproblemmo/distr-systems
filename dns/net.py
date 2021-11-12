# TODO docs:

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
