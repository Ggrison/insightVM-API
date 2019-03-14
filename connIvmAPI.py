# Purpose:
# 	This script is used by other scripts to establish connection
# 	and retrieve the JSON data from the API
#
# Usage:
#	You need to fill in the credential of the user you've created within
#	insightVM.
#	This user should have profile User and MUST have access to ALL sites and ALL groups
#	Without this privileges the user won't be able to access all assets and their details

import urllib2, base64

USER = "MY_USER"
PWD = "MY_PASSWORD"

class Connect:
        def __init__(self, url):
                self.user = USER
                self.pwd = PWD
                self.url = url
        #Retrieve JSON data provided by the API
        def getData(self):
                request = urllib2.Request(self.url)
                base64string = base64.b64encode("%s:%s" % (self.user, self.pwd))
                request.add_header("Authorization", "Basic %s" % base64string)
                return urllib2.urlopen(request)