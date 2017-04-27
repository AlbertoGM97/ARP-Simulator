# Main file for the program

from readInput import readInput

def main(inputScenario):

    for a in inputScenario["subnets"]:
        print(a["id"])

if __name__ == "__main__":
    
    inString = readInput("infile.json")
    main(inString)