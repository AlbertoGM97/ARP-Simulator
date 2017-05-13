
class layer3_device:

    def __init__(self, name, ifaces, routes):       # Class constructor
        self.name = name            # Identification for the device
        self.ifaces = ifaces        # List of iface objects
        self.routes = routes        # List of dictionaries containing routes. Hosts have only one entry
        self.ARP_table = []         # Empty list for ARP table.

    def is_your_IP(self, IP_search):
        for i in self.ifaces:       # Search among its ifaces objects if one has that IP
            if i.IP_addr == IP_search:
                return True
        return False

    def send_packet(self, IP_dest):
        print("Sending packet to" + IP_dest + ".")
        IP_next = findIPnext(IP_dest)            # Search in routing table for IP to send
        interface = findIface(IP_next)           # Search which our own interfaces sends to that IP
        count = 0
        for i in self.ARP_table:  # Check if IP to send is in ARP table
            if i["IP_addr"] == IP_next:
                count = count+1
                break
        if count == 0:
            print("is not in ARP table. Sending ARP broadcast")
            self.ARP_table.append(interface.send_ARP(IP_next)) # Ask for the MAC of IP to send--no estoy seguro este bien puesto
        interface.send_frame(MAC, IP_dest)
        
    def findIPnext(self, IP_dest):
        pass
        
    def findIface(self, IP_next):
        for i in self.ifaces:          # Search among its ifaces objects if one has that IP
            if i.is_one_of_your_neighbors(IP_next):
                return i

    def save_ARP_table(self, iface):
        count = 0
        for i in self.ARP_table:        # Check if IP to save is in ARP table
            if (i["IP_addr"] == iface.IP_addr) && (i["MAC_addr"] == iface.MAC_addr):
                count = count+1
                break
        if count == 0:
            ARP_table.append({"MAC_addr": iface.MAC_addr, "IP_addr": iface.IP_addr}) # Save it in ARP table
            print("Saved in ARP table of host " + self.name + " the entry IP=" +iface.IP_addr + " MAC=" + iface.MAC_addr + ".")

class iface:

    def __init__(self, name, IP_addr, MAC_addr, layer3_parent):                # Class constructor
        self.name = name
        self.IP_addr = IP_addr
        self.MAC_addr = MAC_addr
        self.layer3_parent = layer3_parent
        self.adjacent = []

    def add_adjacent(self, new_iface):
        self.adjacent.append(new_iface)

    def send_ARP(self, IP_next):
        for i in self.adjacent: # Search among its adjacent objects if one has that IP
            if i.receive_ARP(IP_next, self):
                print("Received ARP response.")
                self.layer3_parent.save_ARP_table(i)
                break

    def receive_ARP(self, IP, interface): # Receives interface that asks to pass to save ARP of layer3_device
        print(self.IP_addr + " receives ARP broadcast.")
        if IP == self.IP_addr:
            self.layer3_parent.save_ARP_table(interface)
            return True
        else
            return False

    def send_frame(self, MAC, IP_dest):
        print(IP_addr + "sends to" + IP_dest + "with MAC" + MAC)
        for i in self.adjacent: # Search among its adjacent objects if one has that IP
            if i.MAC_addr == MAC:
                i.receive_frame(IP_dest)
                break

    def receive_frame(self, IP_dest):
        if IP_dest == IP_addr:
            print("Packet arrived to destination.")
        else:
            self.layer3_parent.send_packet(IP_dest)
        
    def is_one_of_your_neighbors(self, IP_search):
        for i in self.adjacent: # Search among its ifaces objects if one has that IP
            if i.IP_addr == IP_search:
                return True
        return False

class IP_utils:

    @staticmethod
    def IP_to_number(str_IP_addr):
        byte_elements = str_IP_addr.split(".")
        IP_num = 0

        for k in range(0, 4):
            IP_num = IP_num + int(byte_elements[3-k])*(2**(k*8))

        return IP_num

    @staticmethod
    def number_to_IP(num_IP_addr):
        IP_str = ""
        
        for k in range(0, 4):
            IP_str = IP_str + str((num_IP_addr >> ((3-k)*8)) & 0xFF) + "."

        return IP_str[0:-1]