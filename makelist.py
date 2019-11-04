import json

list = open("colorcode.csv", "r")
out = open("colors.list", "w")
dict = {}
outstring = ""
for l in list:
    line = l[:]
    colorname = line[0:line.find(",")]
    line = line[line.find(",")+1:]
    line = line.strip('\n').strip("\"")
    vals = line.split(",")
    vals = [int(x) for x in vals]
    dict[colorname] = vals

out.write(json.dumps(dict))
out.close()
list.close()
