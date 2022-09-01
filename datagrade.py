import pandas as pd
import numpy as np

import fnmatch

#df = pd.read_csv("fetchalldf.csv").to_numpy()

gradeFile = open("items_game.json", "r")
gradeLines = gradeFile.readlines()


test = "bingbongtrump"
print('"ancient"')

redList = []
pinkList = []
purpleList = []
blueList = []

for i in range(len(gradeLines)):
    if gradeLines[i].endswith('"ancient"\n') == True:
        #print(gradeLines[i])
        j = 2
        while gradeLines[i+j].endswith("}\n") == False:
            redList.append(gradeLines[i+j].replace("\t", "").replace('"10"', "").replace('"1"', "").replace("\n", "").replace('  ', '').replace('" ', '"')[1 : -1 :])
            j = j + 1


    if gradeLines[i].endswith('"legendary"\n') == True:
        #print(gradeLines[i])
        j = 2
        while gradeLines[i+j].endswith("}\n") == False:
            pinkList.append(gradeLines[i+j].replace("\t", "").replace('"10"', "").replace('"1"', "").replace("\n", "").replace('  ', '').replace('" ', '"')[1 : -1 :])
            j = j + 1

    if gradeLines[i].endswith('"mythical"\n') == True:
        #print(gradeLines[i])
        j = 2
        while gradeLines[i+j].endswith("}\n") == False:
            purpleList.append(gradeLines[i+j].replace("\t", "").replace('"10"', "").replace('"1"', "").replace("\n", "").replace('  ', '').replace('" ', '"')[1 : -1 :])
            j = j + 1


    if gradeLines[i].endswith('"rare"\n') == True:
        #print(gradeLines[i])
        j = 2
        while gradeLines[i+j].endswith("}\n") == False:
            blueList.append(gradeLines[i+j].replace("\t", "").replace('"10"', "").replace('"1"', "").replace("\n", "").replace('  ', '').replace('" ', '"')[1 : -1 :])
            j = j + 1


gradeList = []
gradeList.append(blueList)
gradeList.append(purpleList)
gradeList.append(pinkList)
gradeList.append(redList)

for line in blueList:
    print(line)


gradeTxt = open("grade_sheet.txt", "w")
for i in range(len(gradeList)):
    for j in range(len(gradeList[i])):
        gradeTxt.writelines(gradeList[i][j])
        gradeTxt.writelines(", ")
    gradeTxt.writelines("\n")
