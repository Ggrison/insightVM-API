# Purpose:
# 	This script generates a JSON association of hostname -> software
# 	I use this script to find unwanted software present on my servers
# 
# Dependance:
# 	connIVM.py -> to connect to insightVM API (Fill-in your credentials within this script)
#	assetList.py -> output of assetList.py is the input of this script
#
# Usage:
# 	1) Fill-in the UNWANTED_SOFT list below (not case sensitive and the matching is not done on the whole soft name).
#	   You may want to use softwareList.py script to have a complete list of the software found on all your assets by insightVM.
# 	2) Run the assetList.py script that will generate a flat file of all installed software per assetList
# 	3) Run this script to parse the asseList.json file created by assetList.py
# 	4) unwantedSoftPerAsset.json file and unwantedSoftPerAsset.csv are generated
# 	5) Review your results
#
# Output:
#	A Json file and a CSV file

import json, os

FILE = "assetList.json"
RESULT_FILE_JSON = "unwantedSoftPerAsset.json"
RESULT_FILE_CSV = "unwantedSoftPerAsset.csv"

UNWANTED_SOFT = ["Adobe Reader", "Adobe Acrobat Reader", "Adobe PDF Reader", "Adobe AIR", "Adobe Flash", "Foxit", "LogMeIn", "Malwarebytes",
				 "Microsoft Office", "Silverlight", "Mozilla Firefox", "TeamViewer", "VideoLAN", "WebEx", "Wireshark"]

class Server:
        def __init__(self, hostname, ip, os, softList=[]):
                self.hostname = hostname
                self.ip = ip
                self.os = os
                self.softList = softList
        def toCSV(self):
                return self.hostname + ";" + self.ip + ";" + self.os + ";" + "".join([str(soft) + ";" for soft in self.softList]) + "\n"

result = []
with open(FILE) as f:
	data = json.load(f)
for server in data["serverList"]:
	softList = []
	for uwSoft in UNWANTED_SOFT:
		for soft in server["softList"]:
			if soft.lower().find(uwSoft.lower()) != -1:
				softList.append(soft)
	if len(softList) > 0:
		result.append(Server(server["hostname"], server["ip"], server["os"],softList))
	softList = []
if os.path.isfile(RESULT_FILE_JSON):
	os.remove(RESULT_FILE_JSON)
with open(RESULT_FILE_JSON,"a") as f:
	f.write(json.dumps(result, default=lambda o: o.__dict__, sort_keys=True, indent=4))
print(RESULT_FILE_JSON + " has been created.")
	
if os.path.isfile(RESULT_FILE_CSV):
	os.remove(RESULT_FILE_CSV)
with open(RESULT_FILE_CSV,"a") as f:
	for s in result:
		f.write(s.toCSV())
print(RESULT_FILE_CSV + " has been created.")