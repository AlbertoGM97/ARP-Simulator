# Main file for the program

from readInput import readInput
from layer3 import *

def main(topologia):
    while True:
        IPorigin = input("Enter the IP of the source for the packet: ")
        IPdest   = input("Enter the IP of the destination for the packet: ")
        HostList=[]
        RouterList=[]
        for a in HostList:
            if(a.is_your_IP(IPorigin)): # antes esto if(IPorigin== HostA.ifaces[0].IP_addr):
                a.sendpacket(IPdest)
                break       #we have our starting host , this is the one for which we should start the ARP loop


    for a in range(0,len(topologia["subnet"])):            #reading all subnets
        for b in range(0,len(topologia["subnet"][a]["host"])):  #reading hosts
            HostCreator(a,b)
    for a in range(0,len(topologia["subnet"][a])):
        for b in range(0,len(topologia["subnet"][a]["router"])):
            CreateRouter(a,b)
def HostCreator(subnet,host): 
    newHost= layer3_device(topologia["subnets"][subnet]["host"][host]["id"],CreateInterfaces("host",subnet,host,newHost),topologia["subnets"][subnet]["host"][host]["gateway"])
    HostList.append(newHost)
    
    #HostA= Layer3_device("A",CreateInterfaces("A"),topologia["subnets"][0]["host"][0]["gateway"])
    #HostB= Layer3_device("B",CreateInterfaces("B"),topologia["subnets"][0]["host"][1]["gateway"])
    #HostC= Layer3_device("C",CreateInterfaces("C"),topologia["subnets"][0]["host"][2]["gateway"])
    #HostD= Layer3_device("D",CreateInterfaces("D"),topologia["subnets"][1]["host"][0]["gateway"])
    #HostE= Layer3_device("E",CreateInterfaces("E"),topologia["subnets"][2]["host"][0]["gateway"])
    #HostF= Layer3_device("F",CreateIntercaces("F"),topologia["subnets"][2]["host"][1]["gateway"])
    
def CreateInterfaces(device,subnet,host,parent):

    if(device=="host"):
        interface=iface("eth0",topologia["subnets"][subnet]["host"][host]["IPaddr"],topologia["subnets"][subnet]["host"][host]["MACaddr"],parent)
        return interface
    if(device=="router"):
        interface=iface(topologia["subnet"][subnet]["router"][host]["iface"],topologia["subnet"][subnet]["router"][host]["IPaddr"],topologia["subnet"][subnet]["router"][host]["MACaddr"],parent)
        return interface
    #if(host=="A"):
       # interface= iface("eth0",topologia["subnets"][0]["host"][0]["IPaddr"],topologia["subnets"][0]["host"][0]["MACaddr"],hostA)      # pongo a todas las interfaces de los hosts nombre eth0
        # return interface  
   #  elif(host=="B"):
      #   interface=  iface("eth0",topologia["subnets"][0]["host"][1]["IPaddr"],topologia["subnets"][0]["host"][1]["MACaddr"],hostB)
      #   return interface
     # elif(host=="C"):
      #   interface=  iface("eth0",topologia["subnets"][0]["host"][2]["IPaddr"],topologia["subnets"][0]["host"][2]["MACaddr"],hostC)
      #   return interface
    #  elif(host=="D"):
    #     interface=  iface("eth0",topologia["subnets"][1]["host"][0]["IPaddr"],topologia["subnets"][1]["host"][0]["MACaddr"],hostD)
    #    return interface
    #  elif(host=="E"):
     #    interface=  iface("eth0",topologia["subnets"][2]["host"][0]["IPaddr"],topologia["subnets"][2]["host"][0]["MACaddr"],hostE)
    #     return interface
     # elif(host=="F"):
     #   interface=  iface("eth0",topologia["subnets"][2]["host"][1]["IPaddr"],topologia["subnets"][2]["host"][1]["MACaddr"],hostF)
     #    return interface
     #elif(host=="R1"):
     #    interface=[iface("eth1",topologia["subnets"][0]["router"]["IPaddr"],topologia["subnets"][0]["router"]["MACaddr"],R1), iface("eth2",topologia["subnets"][1]["router"][0]["IPaddr"],topologia["subnets"][1]["router"][0]["MACaddr"],R1)]
     #    return interface
    # elif(host=="R2"):
    #     interface=[iface("eth1",topologia["subnets"][1]["router"][1]["IPaddr"],topologia["subnets"][1]["router"][1]["MACaddr"],R2), iface("eth2",topologia["subnets"][2]["router"][0]["IPaddr"],topologia["subnets"][2]["router"][0]["MACaddr"],R2)]
     #     return interface
 
def CreateRouter(subnet,router):
    for a in range(0,len(RouterList)):
        if (a.name==topologia):   #we have already created that router at the router list
           a.ifaces.append(CreateInterfaces(subnet,router)) 
        else:     # we create the router in the list
        newRouter= Layer3_device(topologia["subnet"][subnet]["router"][router]["id"],CreateInterfaces("router",subnet,router,newRouter,)
        RouterList.append(newRouter)
        

def CreateRoutingTable(router):     #this is only for routers since Host have only one entry (gateway)
    for a in range(0,len(RouterList)):
        a.routes= topologia["routing"][a]["table"]



if __name__ == "__main__":    # El c�digo va en main, no aqui
    
    inString = readInput("infile.json")
    main(inString)
