import json

def createJson(data, filename):
	with open(filename, "w") as outfile:
		json.dump(data, outfile)