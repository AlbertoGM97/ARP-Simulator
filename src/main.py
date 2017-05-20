# Main file for the program

from readInput import readInput
from layer3 import *

HostList=[]    #as global variables
RouterList=[]
topologia = readInput("infile.json")

def main():
    
    for a in range(0,len(topologia["subnets"])):            #reading all subnets
        for b in range(0,len(topologia["subnets"][a]["host"])):  #reading hosts
            HostCreator(a,b)

    for a in range(0,len(topologia["subnets"])):
        for b in range(0,len(topologia["subnets"][a]["router"])):
            CreateRouter(a,b)
            
    for router in RouterList: #create adjacents
        for interface in router.ifaces:
            Hosts_in_subnet = []
            for host in HostList:
                if(host.is_your_IP(interface.IP_addr)):
                    interface.add_adjacent(host.ifaces[0])#Since in this simplification program, hosts only have one interface
                    host.ifaces[0].add_adjacent(interface)
                    Hosts_in_subnet.append(host)
            for host1 in Hosts_in_subnet:
                for host2 in Hosts_in_subnet:
                    if (host1 != host2) and not host1.ifaces[0].is_one_of_your_neighbors(host2.ifaces[0].IP_addr):
                        host1.ifaces[0].add_adjacent(host2.ifaces[0]) #Since in this simplification program, hosts only have one interface
    
    # --------------- DEBUG -------------------------------
    print("These are the hosts")
    for each_host in HostList:
        print(" -", each_host.name, " -> ", end = "")
        for each_interface in each_host.ifaces:
            print("IP: ", each_interface.IP_addr, end = "")
            #print(" MAC:", each_interface.MAC_addr, end = " ")
            
            print("  ADJACENTS: ", end = "")
            for each_adjacent in each_interface.adjacent:
                print(each_adjacent.parent.name, end = "")

        print("")

    print("These are the Routers")
    for each_router in RouterList:
        print(" -", each_router.name, " -> ")
        for each_interface in each_router.ifaces:
            print("         IP: ", each_interface.IP_addr, end = "")
            #print(" MAC:", each_interface.MAC_addr, end = " ")
            
            print("         ADJACENTS:  ", end = "")
            for each_adjacent in each_interface.adjacent:
                print(each_adjacent.parent.name, end = ", ")
            print("")
    print("")

        
    #------------------------------------------------------
    while True:
        IPorigin = input("Enter the IP of the source for the packet: ")
        IPdest   = input("Enter the IP of the destination for the packet: ")
        for a in HostList:
            if(a.is_your_IP(IPorigin)): # antes esto if(IPorigin== HostA.ifaces[0].IP_addr):
                a.send_packet(IPdest)
                break       #we have our starting host , this is the one for which we should start the ARP loop
    

def HostCreator(subnet,host): 

    temp_route = [{"IP_dest": "0.0.0.0", "mask" : "0.0.0.0", "gateway": topologia["subnets"][subnet]["host"][host]["gateway"], "iface":"eth0"}]
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

    if(len(RouterList)==0):
        newRouter= layer3_device(topologia["subnets"][subnet]["router"][router]["id"],[],temp_routing)
        newRouter.ifaces.append(CreateInterfaces("router",subnet,router,"parent"))
        newRouter.ifaces[-1].layer3_parent=newRouter
        RouterList.append(newRouter)
    else:
        for a in (RouterList):
            if (a.name==topologia["subnets"][subnet]["router"][router]["id"]):   #we have already created that router at the router list
                a.ifaces.append(CreateInterfaces("router",subnet,router,a)) 
            else:     # we create the router in the list
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
