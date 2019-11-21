#  Quick script to generate a suricata compatible File of all the Badips categories with a score of 1

# https://redmine.openinfosecfoundation.org/projects/suricata/wiki/IPReputationFormat
# to run just execute python3 gather.py and it will create the categories and iplist in the local directory
# These files can then get cloned to /etc/suricata/iprep/categories.txt and  /etc/suricata/iprep respectively

import requests
import json
import os
from urllib.parse import urlencode


categoryList = requests.get("https://www.badips.com/get/categories")

def getBadIps(category, score, age, badipsurl = "https://www.badips.com"):
         try:
            url = "?".join([
                "/".join([badipsurl, "get", "list", category, str(score)]),
                urlencode({'age': age})])            
            print(url)
            response = requests.get(url)
         except HTTPError as response: 
            print('Api Request Error %s' % response)
         else:
            print(response.content)
            return response.content.split()

def getCategories(badipsurl = "https://www.badips.com"):
         """Get badips.com categories.
 
         Returns
         -------
         set
             Set of categories.

         Raises
         ------
         HTTPError
             Any issues with badips.com request.
         ValueError
             If badips.com response didn't contain necessary information
         """
         try:
             response = requests.get("/".join([badipsurl, "get", "categories"]))
         except HTTPError as response: # pragma: no cover
            print('Api Request Error %s' % response)
         else:
             response_json = response.json()
             if not 'categories' in response_json:
                 err = "badips.com response lacked categories specification. Response was: %s" \
                   % (response_json,)
                 raise ValueError(err)
             categories = response_json['categories']
             categories_names = set(
                 value['Name'] for value in categories)
             return categories_names


def buildreputationlist():
    replist = open("categorylist.txt", "w")
    iplist = open("iplist.txt", "w")
    
    stopcategory = False
    categorynames = getCategories()
    categoryid = 0
    for name in getCategories():
        
        repitem = "%s,%s,%s\r\n" % (categoryid,name,"Item from BadIPS")

        if(stopcategory == False):
            replist.write(repitem)

        for ip in getBadIps(name, 4, 30):
            badip = "%s,%s,%s\r\n" % (ip.decode(),categoryid,1)
            iplist.write(badip)

        if(categoryid < 60):
            # Reptuation file is hard coded to no larger than 60 https://jasonish-suricata.readthedocs.io/en/latest/reputation/ipreputation/ip-reputation-format.html
            categoryid += 1
        else:
            stopcategory = True

    replist.close()
    iplist.close()

buildreputationlist()