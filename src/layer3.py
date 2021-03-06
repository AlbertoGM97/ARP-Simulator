import time

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
        if(self.is_your_IP(IP_dest)):#in case is a router and has more than one interface
            print("[o] Packet arrived to destination "+ IP_dest+".")
            return
        print("[+] Device "+ self.name +" sending packet to destination = " + IP_dest + ".")
        time.sleep(2)
        IP_next = self.findIPnext(IP_dest)            # Search in routing table for IP to send
        if IP_next == 0:
            print("[!] ERROR: No route to destination.")
            exit()

        interface = self.findIface(IP_next)           # Search which our own interfaces sends to that IP
        count = 0
        for i in self.ARP_table:  # Check if IP to send is in ARP table
            if i["IP_addr"] == IP_next:
                count = count+1
                print("[!] Address found on ARP table")
                break
        if count == 0:
            print("[!] Is not in ARP table. Sending ARP broadcast")
            #time.sleep(2)
            interface.send_ARP(IP_next) # Ask for the MAC of IP to send--no estoy seguro este bien puesto !!!

        for k in range(0, len(self.ARP_table)):
            if IP_next == self.ARP_table[k]["IP_addr"]:
                break

        interface.send_frame(self.ARP_table[k]["MAC_addr"], IP_dest, IP_next)
        
    def findIPnext(self, IP_dest):
        for each_route in self.routes:
            temp = IP_utils.IP_to_number(each_route["mask"]) & IP_utils.IP_to_number(IP_dest)

            if (each_route["IP_dest"] == IP_utils.number_to_IP(temp)):
                if(each_route["gateway"] != "0.0.0.0"):
                    return each_route["gateway"]#each_route["gateway"] # Next IP on route (If 0.0.0.0 then last IP)
                else:
                    return IP_dest
            
            if (each_route["IP_dest"] == "default" or each_route["IP_dest"] == "0.0.0.0"):
                    return each_route["gateway"]
        return "0"      # Not found
        
    def findIface(self, IP_next):
        for i in self.ifaces:          # Search among its ifaces objects if one has that IP
            #print(IP_next , "   ", i.IP_addr)
            if i.is_one_of_your_neighbors(IP_next):
                return i
        print("[E] Oh,oh, interface with neighbor = ", IP_next, "not found in ", self.name)

    def save_ARP_table(self, iface):
        count = 0
        for i in self.ARP_table:        # Check if IP to save is in ARP table
            if (i["IP_addr"] == iface.IP_addr) and (i["MAC_addr"] == iface.MAC_addr):
                count = count+1
                break
        if count == 0:
            self.ARP_table.append({"MAC_addr": iface.MAC_addr, "IP_addr": iface.IP_addr}) # Save it in ARP table
            print("[S] Saved in ARP table of host " + self.name + " the entry IP = " +iface.IP_addr + " MAC = " + iface.MAC_addr + ".")
            time.sleep(2)

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
                adjcent=i
        print("[!] Received ARP response.")
        time.sleep(2)
        self.layer3_parent.save_ARP_table(adjcent)

    def receive_ARP(self, IP, interface): # Receives interface that asks to pass to save ARP of layer3_device
        print("[-]", self.IP_addr + " receives ARP broadcast.")
        time.sleep(2)
        if IP == self.IP_addr:
            self.layer3_parent.save_ARP_table(interface)
            return True
        else:
            return False

    def send_frame(self, recvMAC, IP_dest, IP_next):
        print("[+]" , self.IP_addr + " sends to " + IP_next + " with MAC " + recvMAC)
        time.sleep(2)
        for i in self.adjacent: # Search among its adjacent objects if one has that IP
            if i.MAC_addr == recvMAC:
                i.receive_frame(IP_dest)
                break

    def receive_frame(self, IP_dest):
        if IP_dest == self.IP_addr:
            print("[o] Packet arrived to destination "+ IP_dest+".")
        else:
            self.layer3_parent.send_packet(IP_dest)
        
    def is_one_of_your_neighbors(self, IP_search):
        for i in self.adjacent: # Search among its ifaces objects if one has that MAC
            #print("neighbor is "+i.IP_addr)
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