import json

curr = open("current.data", "r")
dbf = open("colors.list", "r")
db = json.loads(dbf.read())
c = json.loads(curr.readline())

print "The current color has the following values:\nR: "+str(c[0])+"\nG: "+str(c[1])+"\nB: "+str(c[2])
exists = False
name = ""
alias = ""
for k in db:
    if db[k] == c:
        exists = True
        name = k
if name:
    print "This color's name is \""+name+"\"."
else:
    cr = raw_input("This color has no alias. Would you like to create one? (Y/N) ")
    if cr.lower() == "y":
        alias = raw_input("What would you like to name this color?\n")
        if alias in db:
            ow = raw_input("This alias already exists. It has a value of "+str(db[k])+".\nWould you like to overwrite? (Y/N) ")
            if ow.lower() == "y":
                db[alias] = c
                print "New color saved as \""+alias+"\"."
        else:
            db[alias] = c
            print "New color saved as \""+alias+"\"."
curr.close()
dbf.close()
dbf = open("colors.list", "w")
dbf.write(json.dumps(db))
dbf.close()
