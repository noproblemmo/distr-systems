"""Computer."""


class NetworkInterface:
    """Network interface."""

    def __init__(self):
        self.net = None
        self.addr = None
        self.dns = None
        self.msg = None

    def setup(self, net, addr):
        """Set net and address to interface."""
        self.net = net
        self.addr = addr

    def set_dns_server(self, addr):
        """Set DNS server."""
        self.dns = addr

    def ping(self, addr):
        """Send ping to address."""
        if not self.net:
            return "No network"
        return self.net.ping(self.addr, addr)

    def resolve(self, name):
        """Resolve name."""
        if not self.net:
            return None
        return self.net.resolve(self.dns, name)
        
    def resolveNonRec(self, dns, name):
        """Resolve name."""
        if not self.net:
            return None
        ans = self.net.resolveNonRec(dns, name)
        if ans[1] == "IP":
            return ans
        if ans[1] == "DNS":
            ans = self.resolveNonRec(ans[0], name)
            return ans
    
    def sendMessage(self, data, dst):
        message = [data, self.addr, dst]
        return message
        
    def readMessage(self, message):
        if(message[2] == self.addr):
            return f"\"{message[0]}\" from {message[1]}"
        else:
            return "No messages"
        
class Comp:
    """Computer."""
    def __init__(self):
        self.__iface = NetworkInterface()
        self.__local_db = None

    def iface(self):
        """Return network interface."""
        return self.__iface
    
    def localDb(self):
        return self.__local_db
    
    def resolve(self, name):
        """Resolve name."""
        if self.__local_db:
            addr = self.__local_db.resolve(name)
            if addr:
                return addr
        return self.__iface.resolve(name)
        
    def resolveNonRec(self, name):
        """Resolve name."""
        if self.__local_db:
            addr = self.__local_db.resolve(name)
            if addr: 
                return addr
        ans = self.__iface.resolveNonRec(self.iface().dns, name)
        return ans[0]

    def set_dns_db(self, db):
        """Set DNS db."""
        self.__local_db = db
    
    

"""Computer network."""


class Network:
    """Network represents net."""

    def __init__(self):
        self.__hosts = {}
        messagebuffer = None
        
    def set_msgbuf(self, message):
        """Message buffer"""
        if message: 
           self.messagebuffer = message

    def add_host(self, comp, addr):
        """Add host to net."""
        self.__hosts[addr] = comp
        comp.iface().setup(self, addr)

    def ping(self, src, dst):
        """Ping sends ping to host."""
        if dst in self.__hosts:
            return f"ping from {src} to {dst}"
        return "Unknown host"
    
    #Recursive DNS
    def resolve(self, dns_addr, name):
        try:
            return self.__hosts[dns_addr].resolve(name)
        except KeyError:
            return None
     
    #NonRecursive DNS
    def resolveNonRec(self, dns_addr, name):
            
        if self.__hosts[dns_addr].localDb().resolve(name):
            addr = self.__hosts[dns_addr].localDb().resolve(name)
            if addr: 
                ans = [addr, "IP"]
                return ans
        ans = [self.__hosts[dns_addr].iface().dns, "DNS"]
        return ans
    
    