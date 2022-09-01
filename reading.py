import pandas as pd
import numpy as np
import json

#with open("response.json") as f:
#    data_str = f.read()
#data = json.load(data_str)

datafile = open('response.json')
data = json.load(datafile)

item_list = []
detailDict = {"Name": -1, "Quality": -1, "Price": -1}

for item in data["response"]["items"]:
    print(item)
    item_details = detailDict
    for version in data["response"]["items"][item]["prices"]:
        #print(version)
        if "Tradable" in data["response"]["items"][item]["prices"][version].keys():
            if "Craftable" in data["response"]["items"][item]["prices"][version]["Tradable"].keys():
                for priceNums in data["response"]["items"][item]["prices"][version]["Tradable"]["Craftable"]:
                    print(priceNums)
                    item_details["Name"] = item
                    item_details["Quality"] = version

                    if type(data["response"]["items"][item]["prices"][version]["Tradable"]["Craftable"]) == list:
                        item_details["Price"] = data["response"]["items"][item]["prices"][version]["Tradable"]["Craftable"][0]["value"]
                        print(item_details["Price"])
                    elif type(data["response"]["items"][item]["prices"][version]["Tradable"]["Craftable"]) == dict:
                        for effect in data["response"]["items"][item]["prices"][version]["Tradable"]["Craftable"]:
                            price_dict = {}
                            price_dict[effect] = data["response"]["items"][item]["prices"][version]["Tradable"]["Craftable"][effect]["value"]
                            item_details["Price"] = price_dict
                            print(price_dict[effect])

    if item_details["Name"] != -1 and item_details["Quality"] != -1 and item_details["Price"] != -1:
        item_list.append(item_details)

'''
i = 0
while i < len(item_list):
    if item_list[i]["Name"] == -1:
        del item_list[i]
        i = i -1
    elif item_list[i]["Quality"] == -1:
        del item_list[i]
        i = i -1
    elif item_list[i]["Price"] == -1:
        del item_list[i]
        i = i -1
    i = i + 1
'''

#for item in item_list:
 #   print(item)
    #print(item["Name"])
    #print(item["Quality"])
    #print(item["Price"])
  #  print()


#alvin = pd.read_json("data.json", 'r')
#print(alvin)