# Ryan Pope (Popestr)
# Copyright 2019


# makelist.py: creates a JSON-readable text file from a .csv file.
# .csv file must be of form COLOR_NAME, "A,B,C"
# COLOR_NAME: name of the color to be read/written into the dictionary
# A, B, C: red, green, and blue values, respectively.

import json

list = open("colorcode.csv", "r")
out = open("colors.list", "w")
dict = {}
outstring = ""
for l in list:
    line = l[:]
    colorname = line[0:line.find(",")].strip(" ")
    line = line[line.find(",")+1:]
    line = line.strip('\n').strip("\"")
    vals = line.replace(" ", "").split(",")
    vals = [int(x) for x in vals]
    dict[colorname] = vals

out.write(json.dumps(dict))
out.close()
list.close()
