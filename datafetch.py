import requests
import steam
import pandas as pd
import json
import sys

import urllib.request
import re

import time

from urllib import parse

import logging

'''
0 normal
6 unique
3 vintage
5 unusual
11 strange
14 collectors
'''

steam.api.key.set("DB2CF0896A1B5A00399BC289D8CF28F1")

headers = {
    'accept': 'application/json',
}
params = {
    'key': '62ba0e9adc5dd1cfcc0d290c',
}
response = requests.get('https://backpack.tf/api/IGetPrices/v4?raw=1&key=62ba0e9adc5dd1cfcc0d290c', params=params, headers=headers)
bptfData = response.json()

#quality dict
qualityDict = {0: "Normal", 1: "Genuine", 6: "Unique", 5: "Unusual", 11: "Strange", 3: "Vintage", 14: "Collector's", 13: "Haunted"}

#effects dict
effectsFile = open('effects.json')
effectsDict = json.load(effectsFile)

cnt = 0

def numberScraper(name, quality, effect, craftable):
    global cnt
    name = name.replace("%", "%25")
    name = name.replace(" ", "%20")
    name = name.replace("'", "%27")
    name = name.replace("é", "%C3%A9")
    name = name.replace("Ü", "%C3%9C")
    name = name.replace("ü", "%C3%BC")
    

    if cnt < 23227:
        cnt = cnt + 1
        print(cnt)
        return

    quality = qualityDict[int(quality)]

    if effect == 0:
        effect = ""

    if craftable == 1:
        craftable = "Craftable"
    else:
        craftable = "Non-Craftable"

    header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

    link = "https://backpack.tf/stats/" + str(quality) + "/" + name + "/Tradable/" + str(craftable) + "/" + str(effect)

    #scheme, netloc, path, query, fragment = parse.urlsplit(link)
    #path = parse.quote(path)
    #link = parse.urlunsplit((scheme, netloc, path, query, fragment))


    htmlReq = urllib.request.Request(link, None, header)
    
    try:
        htmlResp = urllib.request.urlopen(htmlReq)
        cnt = cnt+1
        print(cnt)
    except:
        '''
        if htmlResp.headers["Retry-After"] != 0:
            timewait = htmlResp.headers["Retry-After"]
            print("waiting", htmlResp.headers["Retry-After"], "Seconds")
            time.sleep(timewait)
            htmlResp = urllib.request.urlopen(htmlReq)
        '''
        #else:
        timewait = 5
        print("waiting 9 seconds")
        time.sleep(9)
        htmlResp = urllib.request.urlopen(htmlReq)
        cnt = cnt + 1
        print(cnt)

    html = htmlResp.read()
    htmlText = str(html)

    try:
        found = re.search("inventories, there are <strong>(.+?)</strong> known instances of this item.", htmlText).group(1)
    except AttributeError:
        found = "sorry :("

    return found.replace(",", "")

#print(numberScraper("Terror-antula", 6, 0, 1))

#hat convention: "ID, Name, Quality, Price, Effect, Craftable, Exist"
hatList = []

level = logging.INFO
format   = '  %(message)s'
handlers = [logging.FileHandler('fetchlog3.log'), logging.StreamHandler()]

logging.basicConfig(level = level, format = format, handlers = handlers)
logging.info('Hey, this is working!')

def addItem(id, name, quality, price, currency, effect, craftable):
    item = []

    if currency == "keys":
        price = price * 69.11
    elif currency == "hat":
        price = price * 1.39

    #exist = 0
    exist = numberScraper(name, quality, effect, craftable)

    if effect != 0:
        effect = effectsDict[effect]

    item.append(id)
    item.append(name)
    item.append(quality)
    item.append(effect)
    item.append(craftable)
    item.append(price)
    item.append(exist)

    hatList.append(item)

    logging.info(item)

schema = steam.items.schema(440)
#print(schema[30745].name)

#blacklist funny schema tradable items
blackList = []
for item in schema:
    if item.tradable == True:
        if item.name not in  bptfData["response"]["items"].keys():
            blackList.append(item.name)

#the main loop
for item in schema:
    
    if item.craft_material_type == 'hat' and item.tradable == True and item.name not in blackList:
        for quality in bptfData["response"]["items"][item.name]["prices"]:
            if "Non-Craftable" in bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]:
            #print("Non-Craftable")
            
                if type(bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Non-Craftable"]) == list:
                    price = bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Non-Craftable"][0]["value"]
                    #print("Price: " + str(price))
                    #print()
                    currency = bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Non-Craftable"][0]["currency"]
                    addItem(item.schema_id, item.name, quality, price, currency, 0, 0)

                else:
                    #print("Unusuals")
                    for effect in bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Non-Craftable"]:
                        price = bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Non-Craftable"][effect]["value"]
                        #print("Price for " + str(effect) + ": " + str(price))

                        currency = bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Non-Craftable"][effect]["currency"]
                        addItem(item.schema_id, item.name, quality, price, currency, effect, 0)



            if "Craftable" in bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]:
                #print("Craftable")

                if type(bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Craftable"]) == list:
                    price = bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Craftable"][0]["value"]
                    #print("Price: " + str(price))
                    #print()
                    currency = bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Craftable"][0]["currency"]
                    addItem(item.schema_id, item.name, quality, price, currency, 0, 1)

                else:
                    #print("Unusuals")
                    for effect in bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Craftable"]:
                        price = bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Craftable"][effect]["value"]
                        #print("Price for " + str(effect) + ": " + str(price))

                        currency = bptfData["response"]["items"][item.name]["prices"][quality]["Tradable"]["Craftable"][effect]["currency"]
                        addItem(item.schema_id, item.name, quality, price, currency, effect, 1)


#print to txt
orig_stdout = sys.stdout
f = open('outfetch.txt', 'w')
sys.stdout = f

for item in hatList:
       print(item)
print(len(hatList))

sys.stdout = orig_stdout
f.close()
