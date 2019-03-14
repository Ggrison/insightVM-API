# Purpose: 
# 	This script generates a JSON file that contains assets information
# 		{ hostname, IP, OS, installedSoftware:[] }
# 	for every asset present within insightVM
#
# Dependance:
#	connIVM.py -> to connect to insightVM API (Fill-in your credentials within this script)
#
# Usage:
#	1) Modify URL to your insightVM API
#	2) Run the script
#	3) Review the results within generated assetList.json file
#
# Performance:
# 	2.000 assets in around 3min

import json, os, math
import connIvmAPI

RESULT_FILE = "assetList.json"
NBSERVER = 2000
URL = []
API_URL_PAGE_N = "https://MYINSIGHTVMCONSOLESERVER:3780/api/3/assets?page="

for i in range(0, int(math.ceil(NBSERVER//500.0))):
        URL.append(API_URL_PAGE_N + str(i) + "&size=500&sort=id,asc")

class Server:
        def __init__(self, hostname, ip, os, softList):
                self.hostname = hostname
                self.ip = ip
                self.os = os
                self.softList = softList

class ServerList:
	serverList = []
	def __init__(self):
		self.serverList = []
	def addServer(self, server):
		self.serverList.append(server)
	def getList(self):
		return self.serverList
	def toJson(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
		
try:
    serverList = ServerList()
    if os.path.isfile(RESULT_FILE):
        os.remove(RESULT_FILE)
    for url in URL:
        #retrieve all assets info
        data = json.load(connIvmAPI.Connect(url).getData())
        for server in data["resources"]:
		softList = []
                #retrieve software installed on each asset
                dataSoft = json.load(connIvmAPI.Connect(server["links"][1]["href"]).getData())
                #create a list of installed software
                for soft in dataSoft["resources"]:
                        if "description" in soft:
                                softList.append(soft["description"])
                #create list of server with installed software
                serverList.addServer(Server(server["hostName"] if "hostName" in server else "Undefined",
                                         server["ip"] if "ip" in server else "Undefined",
                                         server["os"] if "os" in server else "Undefined",
                                         softList))
	if(len(data["resources"]) > 0):
		print(str(len(data["resources"])) + " servers treated...")
	#write result as JSON file
    with open(RESULT_FILE, "a") as f:
		f.write(serverList.toJson())
    print(RESULT_FILE + " has been created.")
except IOError, e:
    if hasattr(e, 'code'): # HTTPError
        print 'http error code: ', e.code, e
    elif hasattr(e, 'reason'): # URLError
        print "can't connect, reason: ", e.reason
    else:
        raise