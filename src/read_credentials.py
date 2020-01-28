import json

def return_keys(pathname="credentials.json"):
	with open(pathname, "r") as jsonfile:
		keys = json.load(jsonfile)
	return keys