# Purpose:
# 	This script generates a JSON association of software <-> hostname
# 	I use this script to find unwanted software present on my servers
# 
# Dependance:
# 	connIVM.py -> to connect to insightVM API  (Fill-in your credentials within this script)
#	assetList.py -> output of assetList.py is the input of this script
#
# Usage:
# 	1) Fill-in the UNWANTED_SOFT list below (not case sensitive and the matching is not done on the whole soft name).
#	   You may want to use softwareList.py script to have a complete list of the software found on all your assets by insightVM.
# 	2) Run the assetList.py script that will generate a flat file of all installed software per assetList
# 	3) Run this script to parse the asseList.json file created by assetList.py
# 	4) unwantedSoft.json file is generated
# 	5) You can review the unwantedSoft.json list of software that you don't want and on which server they are deployed for uninstall plan
#

import json, os

FILE = "assetList.json"
RESULT_FILE = "unwantedSoft.json"

UNWANTED_SOFT = ["Adobe Reader", "Adobe Acrobat Reader", "Adobe PDF Reader", "Adobe AIR", "Adobe Flash", "Foxit", "LogMeIn", "Malwarebytes",
				 "Microsoft Office", "Silverlight", "Mozilla Firefox", "TeamViewer", "VideoLAN", "WebEx", "Wireshark"]

result = []
with open(FILE) as f:
	data = json.load(f)
for uwSoft in UNWANTED_SOFT:
	serverList = []
	for server in data["serverList"]:
		for soft in server["softList"]:
			if soft.lower().find(uwSoft.lower()) != -1:
				serverList.append(server["hostname"])
	result.append([uwSoft, serverList])
	serverList = []
if os.path.isfile(RESULT_FILE):
	os.remove(RESULT_FILE)
with open(RESULT_FILE,"a") as f:
	f.write(json.dumps(result, default=lambda o: o.__dict__, sort_keys=True, indent=4))
print(RESULT_FILE+ " has been created")