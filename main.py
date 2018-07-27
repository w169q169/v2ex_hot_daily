# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq
from datetime import datetime
import os
import json
import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf8')

dataDir = "./data"

def get_hot_list():
    ret = []

    domain = "https://www.v2ex.com"
    url = domain + "/?tab=hot"
    res = requests.get(url)

    if res.status_code != requests.codes.ok:
        print("get http content not success:" + res.status_code)
        return ret
  
    doc = pq(res.text)
    alist = doc('table .item_title').items()
    
    for i in alist:
        tr = i.parent().parent()

        tdList = tr.find('td').items()

        count = 0
        item = {
            "imgsrc": "",
            "title": "",
            "url": "",
            "replyNum": "",
        }

        for ii in tdList:
            count = count + 1

            if count == 1:
                item["imgsrc"] = ii.find('a img').attr.src
                continue

            if count == 3:
                item["title"] = ii.find('.item_title a').text()
                item["url"] = ii.find('a').attr.href
                if item["url"]:
                    item["url"] = domain + item["url"]
                continue

            if count == 4:
                item["replyNum"] = ii.find('a').text()

        
        print(item)
        ret.append(item)

    return ret

def getDir(time, prefix):

    yearDir = dataDir + "/" + prefix+ "/" + str(time.year)
    monthDir = yearDir + "/" + str(time.month)

    if not os.path.exists(monthDir):
        os.makedirs(monthDir)

    return monthDir

def save_json_data(data, now):
    monthDir = getDir(now, "json")

    jsonFile = monthDir + "/" + str(now.day) + ".json"

    with open(jsonFile, "w") as f:
        
        jsonData = json.dumps(data)
        f.write(jsonData)

def save_md_data(data, now):
    monthDir = getDir(now, "md")

    jsonFile = monthDir + "/" + str(now.day) + ".md"

    with codecs.open(jsonFile, "w", "utf-8") as f:

        f.write("# " + str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " v2ex热点列表\r\n")
        f.write("\r\n")

        for item in data:
            f.write("+ ")
            f.write("[")
            f.write(item["title"])
            f.write("](")
            f.write(item["url"])
            f.write(") ")
            f.write("[" + item["replyNum"] +"]")
            f.write("\r\n")

if __name__ == "__main__":
     now = datetime.now()
     data = get_hot_list()

     if len(data) == 0:
         print("get hot list is zero")
         os._exit(1)

     save_json_data(data, now)
     save_md_data(data, now)

