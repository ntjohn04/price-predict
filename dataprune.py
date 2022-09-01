import pandas as pd
import numpy as np

import csv

df = pd.read_csv("fetchall.csv")

with open('grade_sheet.txt', newline='\n') as f:
    reader = csv.reader(f, delimiter=',')
    dfGr = list(reader)


for array in dfGr:
    for string in array:
        print(string)

#print(dfGr[0])

npa = df.to_numpy()

#print(len(npa))

#print(len(npa[0]))
bpa = np.append(npa, np.zeros([len(npa),4]),1)
#print(len(bpa[0]))

#print(len(bpa))

for i in range(len(bpa)):

    if bpa[i][6] == " 'sorry :('":
        bpa[i][6] = j

    if bpa[i][3] == "0":
        bpa[i][3] = "None"

    for j in range(len(bpa[0])):
        if j != 4 and j != 5 and type(bpa[i][j]) == str and bpa[i][j][0:2] == " '" and bpa[i][j][-1] == "'":
            bpa[i][j] = bpa[i][j][2 : :]
            bpa[i][j] = bpa[i][j][: -1 :]

    if bpa[i][1] in dfGr[0]:
        bpa[i][7] = 1

    if bpa[i][1] in dfGr[1]:
        bpa[i][8] = 1

    if bpa[i][1] in dfGr[2]:
        bpa[i][9] = 1

    if bpa[i][1] in dfGr[3]:
        bpa[i][10] = 1

    


pd.DataFrame(bpa).to_csv("fetchalldf.csv", index=False, header = ["id", "name", "quality", "effect", "craftable", "price", "exist", "blue", "purple", "pink", "red"])

#df.to_csv("fetchalldf.csv", index=False)