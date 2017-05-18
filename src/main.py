# Main file for the program

from readInput import readInput
from layer3 import *
HostList=[]    #as global variables
RouterList=[]
def main(topologia):
    
    for a in range(0,len(topologia["subnet"])):            #reading all subnets
        for b in range(0,len(topologia["subnet"][a]["host"])):  #reading hosts
            HostCreator(a,b)
    for a in range(0,len(topologia["subnet"][a])):
        for b in range(0,len(topologia["subnet"][a]["router"])):
            CreateRouter(a,b)
    CreateRoutingTable()    #creates the routing table for the routers
    CreateHostsRoutingTable()  #creates the routing table for the hosts;
    
    while True:
        IPorigin = input("Enter the IP of the source for the packet: ")
        IPdest   = input("Enter the IP of the destination for the packet: ")
        for a in HostList:
            if(a.is_your_IP(IPorigin)): # antes esto if(IPorigin== HostA.ifaces[0].IP_addr):
                a.sendpacket(IPdest)
                break       #we have our starting host , this is the one for which we should start the ARP loop
    

def HostCreator(subnet,host): 
    temp_route = [{"IP_dest": "0.0.0.0", "mask" : "0.0.0.0", "gateway": topologia["subnets"][subnet]["host"][host]["gateway"], "iface":"eth0"}]
    newHost= layer3_device(topologia["subnets"][subnet]["host"][host]["id"],CreateInterfaces("host",subnet,host,newHost),temp_route)
    HostList.append(newHost)
    
    
def CreateInterfaces(device,subnet,host,parent):

    if(device=="host"):
        interface=iface("eth0",topologia["subnets"][subnet]["host"][host]["IPaddr"],topologia["subnets"][subnet]["host"][host]["MACaddr"],parent)
        return [interface]
    if(device=="router"):
        interface=iface(topologia["subnet"][subnet]["router"][host]["iface"],topologia["subnet"][subnet]["router"][host]["IPaddr"],topologia["subnet"][subnet]["router"][host]["MACaddr"],parent)
        return interface

 
def CreateRouter(subnet,router):
if(len(RouterList)==0):
    newRouter= Layer3_device(topologia["subnet"][subnet]["router"][router]["id"],CreateInterfaces("router",subnet,router,newRouter)
    RouterList.append(newRouter)
else:
    for a in (RouterList)):
        if (a.name==topologia["subnets"][subnet]["router"][router].id):   #we have already created that router at the router list
           a.ifaces.append(CreateInterfaces("router",subnet,router,a)) 
        else:     # we create the router in the list
            newRouter= Layer3_device(topologia["subnet"][subnet]["router"][router]["id"],CreateInterfaces("router",subnet,router,newRouter)
            RouterList.append(newRouter)
        

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

if __name__ == "__main__":    # El c�digo va en main, no aqui
    
    inString = readInput("infile.json")
    main(inString)
