# Main file for the program

from readInput import readInput
from layer3 import *

def main(topologia):
    IPorigin = input("Enter the IP of the source for the packet: ")
    IPdest   = input("Enter the IP of the destination for the packet: ")
    HostList=[HostA,HostB,HostC,HostD,HostE,HostF]
    for a in HostList:
        if(IPorigin== HostA.ifaces[0].IP_addr):
        break                                        #we have our starting host , this is the one for which we should start the ARP loop
        

def HostCreator():
    
    HostA= Layer3_device("A",CreateInterfaces("A"),topologia["subnets"][0]["host"][0]["gateway"])
    HostB= Layer3_device("B",CreateInterfaces("B"),topologia["subnets"[0]["host"][1]["gateway"])
    HostC= Layer3_device("C",CreateInterfaces("C"),topologia["subnets"][0]["host"][2]["gateway"])
    HostD= Layer3_device("D",CreateInterfaces("D"),topologia["subnets"][1]["host"][0]["gateway"])
    HostE= Layer3_device("E",CreateInterfaces("E"),topologia["subnets"][2]["host"][0]["gateway"])
    HostF= Layer3_device("F",CreateIntercaces("F"),topologia["subnets"][2]["host"][1]["gateway"])
    
def CreateInterfaces(host):
    if(host=="A"):
        interface= iface("eth0",topologia["subnets"][0]["host"][0]["IPaddr"],topologia["subnets"][0]["host"][0]["MACaddr"],hostA)      # pongo a todas las interfaces de los hosts nombre eth0
        return interface  
    elif(host=="B"):
        interface=  iface("eth0",topologia["subnets"][0]["host"][1]["IPaddr"],topologia["subnets"][0]["host"][1]["MACaddr"],hostB)
        return interface
     elif(host=="C"):
        interface=  iface("eth0",topologia["subnets"][0]["host"][2]["IPaddr"],topologia["subnets"][0]["host"][2]["MACaddr"],hostC)
        return interface
     elif(host=="D"):
        interface=  iface("eth0",topologia["subnets"][1]["host"][0]["IPaddr"],topologia["subnets"][1]["host"][0]["MACaddr"],hostD)
        return interface
     elif(host=="E"):
        interface=  iface("eth0",topologia["subnets"][2]["host"][0]["IPaddr"],topologia["subnets"][2]["host"][0]["MACaddr"],hostE)
        return interface
     elif(host=="F"):
        interface=  iface("eth0",topologia["subnets"][2]["host"][1]["IPaddr"],topologia["subnets"][2]["host"][1]["MACaddr"],hostF)
        return interface
    elif(host=="R1"):
        interface=[iface("eth1",topologia["subnets"][0]["router"]["IPaddr"],topologia["subnets"][0]["router"]["MACaddr"],R1), iface("eth2",topologia["subnets"][1]["router"][0]["IPaddr"],topologia["subnets"][1]["router"][0]["MACaddr"],R1)]
        return interface
    elif(host=="R2"):
         interface=[iface("eth1",topologia["subnets"][1]["router"][1]["IPaddr"],topologia["subnets"][1]["router"][1]["MACaddr"],R2), iface("eth2",topologia["subnets"][2]["router"][0]["IPaddr"],topologia["subnets"][2]["router"][0]["MACaddr"],R2)]
         return interface
 
def CreateRouters():
    
    R1= Layer3_device("R1",CreateInterfaces("R1"),CreateRoutingTable("R1"))
    R2= Layer3_device("R2",CreateInterfaces("R2"),CreateRoutingTable("R2"))
 


def CreateRoutingTable(router):     #this is only for routers since Host have only one entry (gateway)
    if(router=="R1"):
      routingTable= topologia["routing"][0]["table"]              #creating routing table for R1
    if(router=="R2"): #routing table for R2
      routingTable= topologia["routing"][1]["table"] 
    for a in topologia["subnets"]: # Esto simplemente es de ejemplo
        print(a["id"])



if __name__ == "__main__":    # El c�digo va en main, no aqui
    
    inString = readInput("infile.json")
    main(inString)
