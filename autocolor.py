# Ryan Pope (Popestr)
# Copyright 2019

# autocolor.py: This script is designed to be automatically run by bash on Pi startup.
# It sends a color signal to the GPIO pins based on the color saved in the startup JSON file.

# see color.py for function documentation.

import pigpio, json
global pi
pi = pigpio.pi();

red_pin = 17
blue_pin = 23
green_pin = 27

savedColors = open("saved.data", "r")
currsv = open("current.data", "w")

c = json.loads(savedColors.read())

def makeColor(red, green, blue, a):
    r = int(red*a)
    g = int(green*a)
    b = int(blue*a)

    pi.set_PWM_dutycycle(red_pin,r)
    pi.set_PWM_dutycycle(green_pin,g)
    pi.set_PWM_dutycycle(blue_pin,b)
    currsv.write(json.dumps([r,g,b]))
    currsv.close()

makeColor(c[0], c[1], c[2], 1)
