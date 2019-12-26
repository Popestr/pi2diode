# Ryan Pope (Popestr)
# Copyright 2019

# listcolor.py: a simple script for writing the current color value as an alias in the dictionary.

import json

curr = open("current.data", "r")
dbf = open("colors.list", "r")
db = json.loads(dbf.read())
c = json.loads(curr.readline())


# Output current color
print "The current color has the following values:\nR: "+str(c[0])+"\nG: "+str(c[1])+"\nB: "+str(c[2])
exists = False
name = ""
alias = ""
for k in db:
    if db[k] == c:
        exists = True
        name = k
if name:
    print "This color's name is \""+name+"\"." # If color already exists, duplicate entries can't exist, so just print the name.
else:
    cr = raw_input("This color has no alias. Would you like to create one? (Y/N) ")
    if cr.lower() == "y":
        alias = raw_input("What would you like to name this color?\n") # Accepts user input for the alias name.
        if alias in db:
            ow = raw_input("This alias already exists. It has a value of "+str(db[k])+".\nWould you like to overwrite? (Y/N) ") # Overwrite protection
            if ow.lower() == "y":
                db[alias] = c
                print "New color saved as \""+alias+"\"."
        else:
            db[alias] = c
            print "New color saved as \""+alias+"\"."
curr.close()
dbf.close()
dbf = open("colors.list", "w")
dbf.write(json.dumps(db)) # Save new color dictionary to JSON.
dbf.close()
