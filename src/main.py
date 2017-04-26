# Main file for the program

from readInput import readInput

def main(inputScenario):

	print(inputScenario["subnet_A"]["NETaddr"])
	print(inputScenario["subnet_A"]["mask"])

if __name__ == "__main__":
	
	inString = readInput("infile.json")
	main(inString)