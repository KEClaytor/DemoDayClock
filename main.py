# Trinket IO demo
# Welcome to CircuitPython 3.1.1 :)

import time
import board
import neopixel

from digitalio import DigitalInOut, Direction, Pull

import adafruit_dotstar as dotstar

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Digital input with pullup on D2
button0 = DigitalInOut(board.D0)
button0.direction = Direction.INPUT
button0.pull = Pull.UP

button1 = DigitalInOut(board.D1)
button1.direction = Direction.INPUT
button1.pull = Pull.UP

button2 = DigitalInOut(board.D2)
button2.direction = Direction.INPUT
button2.pull = Pull.UP

buzzer = DigitalInOut(board.D3)
buzzer.direction = Direction.OUTPUT
buzzer.value = False

# NeoPixel strip (of 16 LEDs) connected on D4
NUMPIXELS = 2
neopixels = neopixel.NeoPixel(board.D4, NUMPIXELS, brightness=0.05, auto_write=False)

######################### HELPERS ##############################

# Helper to convert analog input to voltage
def getVoltage(pin):
    return (pin.value * 3.3) / 65536

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        color = (0, 0, 0)
    if (pos > 255):
        color = (0, 0, 0)
    if (pos < 85):
        color = (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        color = (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        color = (0, int(pos*3), int(255 - pos*3))
    # color = (c/3 for c in color)
    return color

# also make the neopixels swirl around
#for p in range(NUMPIXELS):
    #idx = int ((p * 256 / NUMPIXELS))
    #neopixels[p] = wheel(idx & 255)
neopixels[0] = (236, 38, 255)
neopixels[1] = (255, 235, 20)
neopixels.show()

######################### MAIN LOOP ##############################

i = 0
r, g, b = 0, 0, 0
while True:
    # spin internal LED around! autoshow is on
    dot[0] = wheel(i & 255)

    i = (i+1) % 256  # run from 0 to 255

    value = 0
    buzzer.value = False
    if not button0.value:
        value += 1
        g += 20 % 255
        buzzer.value = True
    if not button1.value:
        value += 2
        r += 20 % 255
        buzzer.value = True
    if not button2.value:
        value += -3
        b += 20 % 255
        buzzer.value = True
    print((value,))

    # neopixels[0] = (r, b, b)
    # neopixels[1] = (r, g, b)
    # neopixels.show()

    time.sleep(0.1) # make bigger to slow down
