# insightVM API

I developped these scripts to get information in an easier way than through the GUI or simply not available within the insightVM features as-is.

I hope these scripts will help some of you.

### Prerequisites
* Python 2.6 (maybe higher version supported I did not test).

* A valid user within insightVM with default **role User** and with Site access **ALL** and Asset group access **ALL**.

* The URL of your API and Port (default is 3780).

### Installing
* No installation.

## Getting Started

### connIvmAPI.py:
  This class will connect and retrieve JSON data from insightVM API.
  
  **INSERT** your user credentials as explained within the comments of the script.

### softwareList.py:
  This script will create a text file containing the full list of the software installed and detected by insightVM on your infrastructure.
  The script retrieves 10.000 different software by default, if you need more just adapt the value.
  You can then review manually which software is installed on your servers.

### assetList.py:
  This script will generate a JSON file as output.
  The output will be the complete list of your assets detected by insightVM and the installed software on it.
  The script is limited to retrieve info from 2000 assets by default, if you need more just adapt the value.
  ```
  Output Example:
  {
    "serverList": [
        {
            "hostname": "myServer1", 
            "ip": "10.10.0.1", 
            "os": "Microsoft Windows Server 2012 R2 Datacenter Edition", 
            "softList": ["soft1","soft2","soft3"]
        }, 
        {
            "hostname": "myServer2", 
            "ip": "10.10.0.2", 
            "os": "Linux 2.6.32", 
            "softList": ["soft4","soft5","soft6"]
        }
       ]
   }
   ```

### unwantedSoft.py:
  This script defines a list of software that you don't want on your infrastructure. Edit this list as you wish, I just entered some software as example.
  
  **With the output of assetList.py** it will generates a JSON file that will tell you on which asset this software is present.
  I recommend that you use the softwareList.py script, review the list and copy-paste the name of software you don't want.
  ```
  Output Example:
  [
    [
        "Adobe Reader", 
        [
            "myServer1", 
            "myServer2"
         ]
     ],
     [
        "Adobe Flash", 
        [
            "myServer2", 
            "myServer4", 
            "myServer5"
         ]
     ]
  ]
  ```
