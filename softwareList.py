# Purpose:
# 	This script will output in a text file all the installed software.
# 	detected by insightVM in order to perform a manual review.
#
# Dependance:
#	connIVM.py -> to connect to insightVM API (Fill-in your credentials within this script)
#
# Usage:
#	1) Modify URL to your insightVM API
#	2) Run the script
#	3) Review manually the result in generated softwareList.txt

import json, os, math
import connIvmAPI

RESULT_FILE = "softwareList.txt"
API_URL_PAGE_N = "https://MYINSIGHTVMCONSOLESERVER:3780/api/3/software?page="
NBSOFT = 10000
URL = []

for i in range(0, int(math.ceil(NBSOFT//500.0))):
	URL.append(API_URL_PAGE_N + str(i) + "&size=500&sort=id,asc")

try:
	softList = []
	for url in URL:
		data = json.load(connIvmAPI.Connect(url).getData())
		for soft in data["resources"]:
			softList.append(soft["description"])
		softList = sorted(softList)	
	if os.path.isfile(RESULT_FILE):
		os.remove(RESULT_FILE)
	with open(RESULT_FILE,"a") as f:
		for s in softList:
			f.write(s.encode("utf-8") + os.linesep)
	print(RESULT_FILE+ " has been created")
except IOError, e:
    if hasattr(e, 'code'): # HTTPError
        print 'http error code: ', e.code, e
    elif hasattr(e, 'reason'): # URLError
        print "can't connect, reason: ", e.reason
    else:
        raise