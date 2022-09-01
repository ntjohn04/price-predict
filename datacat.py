import pandas as pd

file1 = open("fetchlog.log", "r")
file2 = open("fetchlog2.log", "r")
file3 = open("fetchlog3.log", "r")

lines1 = file1.readlines()
lines2 = file2.readlines()
lines3 = file3.readlines()

allLines = []

filefinal = open("fetchall.csv", "w")

for line in lines1:
    allLines.append(line)

for line in lines2:
    allLines.append(line)

for line in lines3:
    allLines.append(line)

filefinal.writelines("id, name, quality, effect, craftable, price, exist\n")
for line in allLines:
    filefinal.writelines(line[2:].replace("[", "").replace("]", ""))
filefinal.close()

df = pd.read_csv("fetchall.csv")

for string in df['name']:
    if string[0] == "'" and string[-1] == "'":
        string[0] = ""
        string[-1] = ""