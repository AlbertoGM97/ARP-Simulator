# Main file for the program

import json
import time

def readInput(inFile):

    with open(inFile, "r") as f:
        data = f.read()

    return json.loads(''.join(data.replace('\n','')))

SubnetList = []
HostList = []    #as global variables
RouterList = []
topologia = readInput("infile.json")


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


def main():

    for each_subnet in topologia["subnets"]:                    # SUBNETS
        SubnetList.append({"name":each_subnet["id"], "NET_addr": each_subnet["NETaddr"], "mask": each_subnet["mask"]})

    for a in range(0,len(topologia["subnets"])):                # HOSTS
        for b in range(0,len(topologia["subnets"][a]["host"])):
            HostCreator(a,b)

    for a in range(0,len(topologia["subnets"])):                # ROUTERS
        for b in range(0,len(topologia["subnets"][a]["router"])):
            CreateRouter(a,b)
            
    for router in RouterList: #create adjacents
        for interface in router.ifaces:
            Hosts_in_subnet = []
            for host in HostList:
                if(isinSubnet(interface.IP_addr,host.ifaces[0].IP_addr)):
                    interface.add_adjacent(host.ifaces[0])#Since in this simplification program, hosts only have one interface
                    host.ifaces[0].add_adjacent(interface)
                    Hosts_in_subnet.append(host)
            for router2 in RouterList:
                if (router != router2):
                    for iface in router2.ifaces:
                        if not interface.is_one_of_your_neighbors(iface.IP_addr):
                            if(isinSubnet(interface.IP_addr,iface.IP_addr)):
                                interface.add_adjacent(iface)#Since in this simplification program, hosts only have one interface
                                iface.add_adjacent(interface)
            for host1 in Hosts_in_subnet:
                for host2 in Hosts_in_subnet:
                    if (host1 != host2) and not host1.ifaces[0].is_one_of_your_neighbors(host2.ifaces[0].IP_addr):
                        host1.ifaces[0].add_adjacent(host2.ifaces[0]) #Since in this simplification program, hosts only have one interface
    
    # --------------- DEBUG -------------------------------
    print("\n--------- DEBUG-------")
    print("These are the hosts")
    for each_host in HostList:
        print(" -", each_host.name, " -> ", end = "")
        for each_interface in each_host.ifaces:
            print("IP: ", each_interface.IP_addr, end = "")
            #print(" MAC:", each_interface.MAC_addr, end = " ")
            
            print("  ADJACENTS: ", end = "")
            for each_adjacent in each_interface.adjacent:
                print(each_adjacent.layer3_parent.name, end = " ")

        print("")

    print("These are the Routers")
    for each_router in RouterList:
        print(" -", each_router.name, " -> ")
        for each_interface in each_router.ifaces:
            print("         IP: ", each_interface.IP_addr, end = "")
            #print(" MAC:", each_interface.MAC_addr, end = " ")
            
            print("         ADJACENTS:  ", end = "")
            for each_adjacent in each_interface.adjacent:
                print(each_adjacent.layer3_parent.name, end = " ")
            print("")
    print("-----------------------\n")

        
    #------------------------------------------------------
    while True:
        IPorigin = input("\n-> Enter the IP of the source for the packet: ")
        IPdest   = input("-> Enter the IP of the destination for the packet: ")
        print("")
        for a in HostList:
            if(a.is_your_IP(IPorigin)): # antes esto if(IPorigin== HostA.ifaces[0].IP_addr):
                a.send_packet(IPdest)
                break       #we have our starting host , this is the one for which we should start the ARP loop
    
def isinSubnet(ip_router,ip_host):

    for index_subnet in range(0,len(topologia["subnets"])):            #reading all subnets
        for index_router in range(0,len(topologia["subnets"][index_subnet]["router"])):  #reading hosts
            if (ip_router == topologia["subnets"][index_subnet]["router"][index_router]["IPaddr"]):
                return isInSubnet(ip_host, topologia["subnets"][index_subnet]["NETaddr"],topologia["subnets"][index_subnet]["mask"])



def isInSubnet(IP_addr_layer3_device, NET_addr, mask):

    temp = IP_utils.IP_to_number(mask) & IP_utils.IP_to_number(IP_addr_layer3_device)
    if (NET_addr == IP_utils.number_to_IP(temp)):
        return True
    return False

def HostCreator(subnet,host): 

    temp_route = [{"IP_dest": topologia["subnets"][subnet]["NETaddr"], "mask" : topologia["subnets"][subnet]["mask"], "gateway": "0.0.0.0", "iface":"eth0"},{"IP_dest": "0.0.0.0", "mask" : "0.0.0.0", "gateway": topologia["subnets"][subnet]["host"][host]["gateway"], "iface":"eth0"}]
    newHost= layer3_device(topologia["subnets"][subnet]["host"][host]["id"],CreateInterfaces("host",subnet,host,0),temp_route)
    newHost.ifaces[-1].layer3_parent=newHost
    HostList.append(newHost)
    
    
def CreateInterfaces(device,subnet,host,parent):

    if(device=="host"):
        interface=iface("eth0",topologia["subnets"][subnet]["host"][host]["IPaddr"],topologia["subnets"][subnet]["host"][host]["MACaddr"],parent)
        return [interface]
    if(device=="router"):
        interface=iface(topologia["subnets"][subnet]["router"][host]["iface"],topologia["subnets"][subnet]["router"][host]["IPaddr"],topologia["subnets"][subnet]["router"][host]["MACaddr"],parent)
        return interface

 
def CreateRouter(subnet,router):
    
    for i in range(0, len(topologia["routing"])):
        if (topologia["routing"][i]["id"] == topologia["subnets"][subnet]["router"][router]["id"]):
            break

    temp_routing = topologia["routing"][i]["table"]
    #print(topologia["subnets"][subnet]["router"][router]["id"] , "-----------------")

    if(len(RouterList)==0):
        newRouter= layer3_device(topologia["subnets"][subnet]["router"][router]["id"],[],temp_routing)
        newRouter.ifaces.append(CreateInterfaces("router",subnet,router,"parent"))
        newRouter.ifaces[-1].layer3_parent=newRouter
        RouterList.append(newRouter)
    else:
        flag = 0
        for a in (RouterList):
            if (a.name==topologia["subnets"][subnet]["router"][router]["id"]):   #we have already created that router at the router list
                a.ifaces.append(CreateInterfaces("router",subnet,router,a))
                flag = 1
                
        if flag == 0:     # we create the router in the list
            newRouter= layer3_device(topologia["subnets"][subnet]["router"][router]["id"],[],temp_routing)
            newRouter.ifaces.append(CreateInterfaces("router",subnet,router,"parent"))
            newRouter.ifaces[-1].layer3_parent=newRouter
            RouterList.append(newRouter)
        

'''
def CreateRoutingTable()):     #this is only for routers since Host have only one entry (gateway)
    for a in RouterList:
        a.routes= topologia["routing"][a]["table"]

def CreateHostsRoutingTable:
    for a in range(0,len(HostList)):    #all hosts in the topology
      gateway= HostList[a].routes  #I had saved here before the gateway of each host.
      HostList[a].routes=[]
      IP=HostList[a].ifaces[0].IP_addr #saving in IP de IP address of the interface of the host.
       for b in range(0,len(SubnetsList)):   #going over all subnets 
           if(SubnetList[b]["NETaddr"]== IP^SubnetList[b]["mask"]):   #finding out in which subnet is the host --> at subnet 'b'
              for c in range(0,len(topologia["subnet"][b]["host"])):        #for all hosts in the correspondent subnet the gateway for the routing table should be IP of the host.
                 entrada= { 
                             "IP": topologia["subnet"][b]["host"][c]["IPaddr"]
                             "Mask": "255.255.255.255"                                    
                           "Gateway":   topologia["subnet"][b]["host"][c]["IPaddr"]
                           "Interface": HostList[a].ifaces[0].name
                 
                           }
                HostList[a].routes.append(entrada)           
             for c in range(0,len(topologia["subnet"]):   #we have to create another entry for each subnet
                 entrada=
                 {
                    "IP": topologia["subnet"][c]["NETaddr"]   
                    "Mask": topologia["subnet"][c]["mask"]
                    "Gateway": gateway      #We had saved the gateway 
                    "Interface": HostList[a].ifaces.name
                
                 }
        entrada_default=
        {
        "IP":    "0.0.0.0"    #this is the default.
        "Mask": "0.0.0.0"
      "Gateway": gateway
       "Interface": HostList[a].ifaces.name
       
       }
'''
if __name__ == "__main__":    # El c�digo va en main, no aqui
    
    main()
