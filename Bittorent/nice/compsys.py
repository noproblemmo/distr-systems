"""Computer and service sketch."""
import datetime


"""Computer network."""
class Network:
    """Network represents net."""

    def __init__(self):
        self.__hosts = {}
        messagebuffer = None
        self.__arpTable = {} #Table with IP addresses 
        
    def set_msgbuf(self, message):
        """Message buffer"""
        if message: 
           self.messagebuffer = message
           
    def hosts(self):
        return self.__hosts

    def add_host(self, comp, addr):
        """Add host to net."""
        self.__hosts[addr] = comp
        comp.iface().setup(self, addr)

    def ping(self, src, dst):
        """Ping sends ping to host."""
        if dst in self.__hosts:
            return f"ping from {src} to {dst}"
        return "Unknown host"
    
    def resolveIP(self, ip):
        if self.hosts()[ip]:
            return self.hosts()[ip]
    
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


class NetworkInterface:
    """Network interface."""

    def __init__(self):
        self.net = None
        self.addr = None #Self IP address 
        self.dns = None
        self.msg = None
        self.__arpTable = {} #Table with IP addresses 
        
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

    #Methods for net interractoion with DNS server

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
            
    #Methods for communication of 2 computers (Sendig messages or *files)
    
    def sendMessage(self, data, dst):
        message = [data, self.addr, dst]
        return message
        
    def readMessage(self, message):
        if(message[2] == self.addr):
            return f"\"{message[0]}\" from {message[1]}"
        else:
            return "No messages"
    

class FileSystem:
    """The file system stub."""

    def __init__(self):
        #Name of files
        self.__files = {"Win32.dll":"Win32.dll", "calc.exe":"calc.exe", "SIMS 4":"0xSIMS4"}
        
        self.__locationFiles =  {   
                                    "Archive":  {
                                                    "1 file":"92.168.0.113", 
                                                    "2 file":"56.128.128.143"
                                                }
                                }
        #Space is NONE mb?
        #TODO: Add feature / Add file's sizes
        self.__space = 12345

    def files(self):
        """Return the list of files."""
        return self.__files

    def space(self):
        """Return the free space in storage."""
        return self.__space
       
        """Add file in local file storage"""
    def add_file(self, file):
        #self.files().append(file)
        if file[0] in self.files():
            self.files()[file[0]][file[1][0]] = file[1][1]
        else:
            self.files()[file[0]] = file[1]
        
    def add_file_location(self, key, value):
        self.__locationFiles[key] = value
        
    def file_location(self):
        return self.__locationFiles

class Comp:
    """Computer."""

    def __init__(self):
        self.handlers = {} 
        self.__fs = FileSystem()
        self.__iface = NetworkInterface()
        self.__local_db = None
        self.__condition = True
        
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
        
    def turnOn(self):
        self.__condition = True
        
    def shutDown(self):
        self.__condition = False
        
    def getCondition(self):
        return self.__condition
        
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
        
    #Services interaction

    def send_request(self, dstip, name, command, *args):
        """Send to destination (dst) some (name) request with command
        and optional args."""
        #IP must be an IP address!
        
        dstpc = self.iface().net.resolveIP(dstip)
        if dstpc:
            ans = dstpc.handlers[name](command, *args)
            print(ans)
        else: 
            return f"There is not {dstip} IP address"

    def add_service(self, srv):
        """Add service to computer."""
        self.handlers[srv.name()] = srv.handle_request

    def file_system(self):
        """Give access to the file system."""
        return self.__fs


class Service:
    """Any service."""

    @staticmethod
    def name():
        """Return the name of service."""
        raise NotImplementedError

    def handle_request(self, command, *args):
        """Handle request."""
        raise NotImplementedError


class Files(Service):
    """The service providing the work with files."""

    @staticmethod
    def name():
        return "files"

    def __init__(self, comp):
        self.__comp = comp

    def handle_request(self, command, *args):
        if command == "list":
            if (args != () and args[0] == "flocation"):
                return self.file_location()
            if args == ():
                return self.list_of_files()

        if command == "space":
            return self.free_space()
            
        if command == "add":
            if(args[0] == "flocation"):
                print("Trying to add file in flocation...")
                self.add_file_location(args[1], args[2])
            else:
                self.add_file(args[0])
            
            return "File succesfully added on computer"

        return "Error"

    def list_of_files(self):
        """Return the list of files."""
        return self.__comp.file_system().files()

    def free_space(self):
        """Return the free space in storage."""
        return self.__comp.file_system().space()
        
    def add_file(self, file):
        """Add file in local storage"""
        self.__comp.file_system().add_file(file)
        
    def add_file_location(self, key, value):
        """Show file location"""
        self.__comp.file_system().add_file_location(key, value)
        
    def file_location(self):
        """Add info about file location"""
        return self.__comp.file_system().file_location()
        
        #Stub
    def send_file(self):
        """Send file on computer"""
        return 1


class Clock(Service):
    """Time service."""

    @staticmethod
    def name():
        return "clock"

    def handle_request(self, command, *args):
        if command == "now":
            if args[0] == "local":
                return '{0:%Y-%m-%d %H:%M:%S}'.format(
                    datetime.datetime.now())

            if args[0] == "utc":
                return '{0:%Y-%m-%d %H:%M:%S}'.format(
                    datetime.datetime.utcnow())

            return "Wrong args"

        return "Unknown command"

class Bittorrent(Service):
    """Time service."""

    @staticmethod
    def name():
        return "bittorrent"
        
    def __init__(self, comp):
        self.__comp = comp

    def handle_request(self, command, *args):
        if command == "download":
            if len(args) != 2:
                print("""
Request error! The query should look like the following:
--------------------------------------------
com.send_request(server, \"bittorrent\", \"download\", \"Spider-man: No way to home\", comp)
--------------------------------------------
Where comp is the ID of your computer
""")
            if args[0]:
                fileDB = self.__comp.file_system().file_location()
                if args[0] in fileDB:
                    print(f"File \"{args[0]}\" was found in Torrent web!\nStart downloading...")
                    print(f"Bittable: {fileDB[args[0]]}")
                    
                    fileInfo = fileDB[args[0]] #Dict with info about parts of whole file 
                    keys = list(fileInfo.keys())
                    
                    pc = self.__comp.iface().net.resolveIP(args[1])
                    
                    pc.send_request(args[1], "files", "add", [args[0], {}])
                    
                    for key in keys:
                        print(f"Trying to recieve file \"{key}\"...")
                        """If file is in local strage of 1 of seed's"""
                        
                        if isinstance(fileInfo[key], str):
                            seed = self.__comp.iface().net.resolveIP(fileInfo[key])
                            if seed.getCondition() == True:
                                    print(f"Recieving file \"{key}\" from {fileInfo[key]}")
                            else:
                                print(f"Host {fileInfo[key]} is unavailable")
                            
                        else:
                            for i in range(len(fileInfo[key])):
                                seed = self.__comp.iface().net.resolveIP(fileInfo[key][i])
                                if seed.getCondition() == True:
                                    print(f"Recieving file \"{key}\" from {fileInfo[key][i]}")
                                    break
                                print(f"Host {fileInfo[key][i]} is unavailable")
                        
                        seedStorage = seed.file_system().files()
                        
                        if key in seedStorage:
                            seed.send_request(args[1], "files", "add", [args[0], [key, seedStorage[key]]])
                        else:
                            print(f"File \"{key}\" missing!")
                else:
                    return f"File \"{args[0]}\" not found!"
                
                return f"File \"{args[0]}\" succesfully dowloaded"

            return "Wrong args"
        return "Unknown command"

# Take it out to tests

def main():
    """Run example."""
    
    net = Network()
    comp = Comp()
    server = Comp()
    slave_1 = Comp()
    slave_2 = Comp()
    slave_3 = Comp()
    
    net.add_host(comp, "124.56.91.119")
    net.add_host(server, "92.163.4.113")
    net.add_host(slave_1, "92.168.0.113")
    net.add_host(slave_2, "56.128.128.143")
    net.add_host(slave_3, "97.15.15.3")

    comp.add_service(Bittorrent(comp))
    comp.add_service(Files(comp))
    
    server.add_service(Bittorrent(server))
    server.add_service(Files(server))
    
    slave_1.add_service(Bittorrent(slave_1))
    slave_1.add_service(Files(slave_1))
    
    slave_2.add_service(Bittorrent(slave_2))
    slave_2.add_service(Files(slave_2))
    
    slave_3.add_service(Bittorrent(slave_3))
    slave_3.add_service(Files(slave_3))
    
    comp.send_request("92.163.4.113", "files", "list")
    comp.send_request("92.163.4.113", "files", "list", "flocation")
    
    #server.send_request("92.163.4.113", "files", "add", "flocation", "Spider-man: No way to home", {"1 fragment":"92.168.0.113", "2 fragment":"56.128.128.143"})
    
    server.send_request("92.163.4.113", "files", "add", "flocation", "Spider-man: No way to home", {"1 fragment":"92.168.0.113", "2 fragment":["56.128.128.143", "97.15.15.3"]})
    
    server.send_request("92.168.0.113", "files", "add", ["1 fragment", "0x1_fragment"])
    server.send_request("56.128.128.143", "files", "add", ["2 fragment", "0x2_fragment"])
    print()
    server.send_request("97.15.15.3", "files", "add", ["2 fragment", "0x2_fragment"])
    
    print()
    print("--------------------------")
    
    slave_1.send_request("92.168.0.113", "files", "list")
    slave_2.send_request("56.128.128.143", "files", "list")
    
    slave_1.send_request("92.168.0.113", "files", "list", "flocation")
    slave_2.send_request("56.128.128.143", "files", "list", "flocation")
    
    #Bitrequest prototype
    print("----Bitrequest testing----")

    slave_2.shutDown()

    comp.send_request("92.163.4.113", "bittorrent", "download", "Spider-man: No way to home", "124.56.91.119")
    
    comp.send_request("124.56.91.119", "files", "list")
    
"""
    comp1 = Comp()
    comp2 = Comp()

    comp2.add_service(Files(comp2))
    comp2.add_service(Clock())

    comp1.send_request(comp2, "files", "list")
    comp1.send_request(comp2, "files", "space")
    
    comp1.send_request(comp2, "files", "add", "kernel32.dll")
    comp1.send_request(comp2, "files", "list")
    
    print()
    
    comp1.send_request(comp2, "clock", "now", "local")
    comp1.send_request(comp2, "clock", "now", "utc")
    comp1.send_request(comp2, "clock", "now", "+3")
    comp1.send_request(comp2, "clock", "date of birth", "Pushkin")
"""

if __name__ == "__main__": ## "!=" - Main disable, "==" - Main enable
    main()
