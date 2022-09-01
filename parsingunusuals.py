import pandas as pd
import numpy as np
import json

import sys

datafile = open('apidata.json')
data = json.load(datafile)

orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f

item_list = []
detailDict = {"Name": -1, "Quality": -1, "Price": -1, "Effect": -1}

def addItem(name, quality, price, currency, effect, craftable):
    item = {}
    item["Name"] = name
    item["Quality"] = quality
    item["Effect"] = effect
    item["Craftable"] = craftable

    if currency == "keys":
        price = price * 69.11
    elif currency == "hat":
        price = price * 1.39
    
    item["Price"] = price

    item_list.append(item)


for item in data["response"]["items"]:
    #print(item)
    for quality in data["response"]["items"][item]["prices"]:
        #print("Quality: " + str(quality))
        
        if "Craftable" in data["response"]["items"][item]["prices"][quality]["Tradable"]:
            #print("Craftable")

            if type(data["response"]["items"][item]["prices"][quality]["Tradable"]["Craftable"]) == dict:
                #print("Unusuals")
                for effect in data["response"]["items"][item]["prices"][quality]["Tradable"]["Craftable"]:
                    price = data["response"]["items"][item]["prices"][quality]["Tradable"]["Craftable"][effect]["value"]
                    #print("Price for " + str(effect) + ": " + str(price))

                    if item.find("War Paint") == -1:
                        if item.find("Cosmetic Case") == -1:
                            if item.find("Taunt") == -1:
                                addItem(item, quality, price, -1, effect, True)
    #print()
    #print()
    #print()

for item in item_list:
    print(item["Name"])
    print("Quality: ", item["Quality"])
    print("Effect: ", item["Effect"])
    print("Craftable: ", item["Craftable"])
    print("Price: ", item["Price"])
    
    print()
    print()

sys.stdout = orig_stdout
f.close()


'''
                Normal = 0
                Genuine = 1
                Vintage = 3
                Unusual = 5
                Unique = 6
                Self-Made = 9
                Strange = 11
                Collector = 14
                Decorated Weapon = 15
'''