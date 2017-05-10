# Main file for the program

from readInput import readInput
from layer3 import *

def main(topologia):
    IPorigin = input("Enter the IP of the source for the packet: ")
    IPdest   = input("Enter the IP of the destination for the packet: ")
    
    for a in topologia["subnets"]: # Esto simplemente es de ejemplo
        print(a["id"])



if __name__ == "__main__":    # El código va en main, no aqui
    
    inString = readInput("infile.json")
    main(inString)
