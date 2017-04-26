
import json

def readInput(inFile):

	with open(inFile, "r") as f:
		data = f.read()

	return json.loads(''.join(data.replace('\n','')))