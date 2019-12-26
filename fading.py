# Ryan Pope (Popestr)
# Copyright 2019

# fading.py: A more complex script for generating fades and fade sequences (referred to as rainbows).

# Documentation for fading.py is still in progress.

import time, json, pigpio, random, math
global pollColor, dbName, r, g, b, fadeTime, step, red_pin, green_pin, blue_pin, pi
pi = pigpio.pi();

start = time.time()

red_pin = 17
green_pin = 27
blue_pin = 23

def reversal(out, varMax):
    if out > varMax:
        return varMax*2-out
    return out

def translate(colorName):
    db = json.loads(open(dbName, "r").read())
    while colorName not in db:
        colorName = raw_input("Invalid color name. Try again: ")
    return db[colorName]

def randbow():
    out = []
    for i in range(8):
        r1 = r2 = r3 = 0
        while r1+r2+r3 < 255:
            r1 = random.randint(0, 255)
            r2 = random.randint(0, 255)
            r3 = random.randint(0, 255)
        out.append([r1,r2,r3])
    return out

def generateSlopes(a, b, delta):
    return [(b[0]-a[0])/delta,(b[1]-a[1])/delta,(b[2]-a[2])/delta]

def displayColor(r, g, b):
    global red_pin, green_pin, blue_pin, pi
    pi.set_PWM_dutycycle(red_pin,r)
    pi.set_PWM_dutycycle(green_pin,g)
    pi.set_PWM_dutycycle(blue_pin,b)

#---------V----------------ADJUSTABLE VARIABLES--------------V-----------

# CHOOSE FADE TYPE (SPECTRUM, ON-OFF, RANDOM)
fadeType = "spectrum"

# ENABLE/DISABLE COLOR DATABASE COMPATIBILITY
pollColor = True
dbName = "colors.list"

# RED, GREEN, BLUE VALUES (0-255)
r=255
g=0
b=0

# TIME BETWEEN CYCLES (IN SECONDS)
fadeTime = 5.0

# HOW OFTEN THE BRIGHTNESS WILL UPDATE (IN SECONDS)
step = 0.01

#-------------V--------------AUTOMATIC FADING-----------------V-----------

def fadeOff():
    global r, g, b, pollColor, dbName, fadeTime, step
    if pollColor:
        pc = ""
        while pc.lower() != "y" and pc.lower() != "n":
          pc = raw_input("Would you like to use a color from the database? (Y/N) ")
        if pc.lower() == "y":
          res = translate(raw_input("Enter the name of the desired color: "))
          r = res[0]
          g = res[1]
          b = res[2]

    fadeTimeMS = fadeTime/step
    rs = float(r*2)/fadeTimeMS
    bs = float(b*2)/fadeTimeMS
    gs = float(g*2)/fadeTimeMS
    rout = gout = bout = 0
    s = time.time()
    #stepc = 0
    while True:
        #stepc +=1
        # if not stepc % 1000:
        #     print stepc
        #     print time.time()-s
        buff = time.time()
        if r != 0: rout = (rout + rs)%(r*2)
        if g != 0: gout = (gout + gs)%(g*2)
        if b != 0: bout = (bout + bs)%(b*2)
        radj = int(reversal(rout, r))
        gadj = int(reversal(gout, g))
        badj = int(reversal(bout, b))
        # print radj
        # print gadj
        # print badj
        # print radj ##
        # print gadj # TODO: replace with GPIO instructions
        # print badj ##
        displayColor(radj, gadj, badj)
        #print step-(time.time()-buff)
        #d = step-(time.time()-buff) # adjust delay to account for processing
        #if d > 0: time.sleep(d)
        #print time.time()-s
        #print step-(time.time()-buff)
        d = step-(time.time()-buff)
        if d > 0: time.sleep(d)

def fadeSpectrum():
    global fadeTime
    mode = raw_input("Use default rainbow? If no, a random sequence will be generated. (Y/N) ").lower()

    dump = open("dump.dat", "w")

    if mode == "y": rnbw = [[148, 0, 211], [75, 0, 130], [0, 0, 255],[0, 255, 0], [255, 255, 0], [255, 127, 0], [255, 0 , 0], [148, 0, 211]]
    else: rnbw = randbow()

    dump.write("Sequence: "+str(rnbw))
    currcol = rnbw[0]
    dataset = set()
    curr = 0
    runtime = fadeTime/len(rnbw)
    step = 0.001
    cycles = 0
    try:
        while True:
          print curr+1
          slp = generateSlopes(currcol, rnbw[curr], (runtime/step)/len(rnbw))
          print slp
          print "**"+str(currcol)+str(rnbw[curr])
          while int(abs(currcol[0]-rnbw[curr][0])) or int(abs(currcol[1]-rnbw[curr][1])) or int(abs(currcol[2]-rnbw[curr][2])):
              for i in range(0, 3): currcol[i]+=slp[i]
              print currcol
              displayColor(*[int(i) for i in currcol])
              time.sleep(step)
          displayColor(*[int(i) for i in currcol])
          curr = (curr+1)%len(rnbw)
          if curr == 0: cycles+=1
    except Exception as e:
        dump.write("\n\nRuntime: "+str(time.time()-start)+" seconds")
        dump.write("\n\nThe program completed "+str(cycles)+" cycles.")
        dump.write("\n\n\nThe following is the terminating error info: \n"+str(e)+"\n")
        print "\nProgram has unexpectedly ended. Data logged to dump.dat."
        dump.close()


if fadeType.lower() == "on-off": fadeOff()
elif fadeType.lower() == "spectrum": fadeSpectrum()
elif fadeType.lower() == "random": fadeRandom()
