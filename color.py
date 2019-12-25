# Ryan Pope (Popestr)
# Copyright 2019

import json, random, pigpio
global pi, channels
pi = pigpio.pi();

channels = {}
# red_pin = 17
# blue_pin = 25
# green_pin = 27

channels[1] = [17,27,23]
channels[2] = [13,19,26]

json_list = open("colors.list", "r")
currsv = open("current.data", "w")
colors = json.loads(json_list.read())

json_list.close()

def makeColor(red, green, blue, a):
    r = int(red*a)
    g = int(green*a)
    b = int(blue*a)

    # print r
    # print g
    # print b
    for key in channels.keys():
        pi.set_PWM_dutycycle(channels[key][0],r)
        pi.set_PWM_dutycycle(channels[key][1],g)
        pi.set_PWM_dutycycle(channels[key][2],b)
    saveColor([r,g,b])

def translate(color):
    vals = colors[color]
    makeColor(vals[0], vals[1], vals[2], 1)
    return vals


def saveColor(c):
    currsv.write(json.dumps(c))
    currsv.close()
    save = raw_input("Colors set! Would you like to run these colors on startup? (Y/N) ")
    if save.lower() == "y":
        colorsaver = open("saved.data", "w")
        colorsaver.write(json.dumps(c))
        colorsaver.close()
        print "Saved."
    else: print "Not saved. Colors will revert on reboot."

req = ""
set = False
while not set:
    req = raw_input("What color would you like to assign? Enter \'rgb\' if you wish to enter RGB values, \'r\' for random or 0 to exit.\n")
    if req == '0': break
    elif req.lower() == 'r':
        rr = random.randint(0,255)
        gr = random.randint(0,255)
        br = random.randint(0,255)
        makeColor(rr,gr,br,1)
        set = True
    elif req.lower() == 'rgb':
        rin = raw_input("What value for R?\n")
        gin = raw_input("What value for G?\n")
        bin = raw_input("What value for B?\n")
        makeColor(rin,gin,bin,1)
        set = True
    else:
        if req not in colors:
            print "Invalid input. Try again!"
        else:
            c = translate(req)
            set = True
