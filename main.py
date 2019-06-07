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

class Timer():

    def __init__(self, testing=False):
        """ Create the timer class
        """
        # How long should we run for, when do we warn and go critical?
        if testing:
            self.time = 10
            self.warn = 5
            self.crit = 1
        else:
            self.time = 8*60
            self.warn = 2*60
            self.crit = 1*60
        self._color_okay = (0, 255, 0)
        self._color_warn = (255, 255, 0)
        self._color_crit = (255, 0, 0)
        # Some internal state trackers
        self.start_time = time.monotonic()
        self.is_running = False
        # Time trackers
        self.elapsed = 0
        self.remaining = self.time

    def start(self):
        """ Start or restart the timer
        """
        self.start_time = time.monotonic()
        self.is_running = True
        # Time trackers
        self.elapsed = 0
        self.remaining = self.time

    def stop(self):
        """ Stop the timer
        """
        self.is_running = False
        # Time trackers
        self.elapsed = 0
        self.remaining = self.time

    def get_color(self):
        if self.remaining == 0:
            # color = tuple(int(c * ) for c in self._color_crit)
            # print(color)
            blinks_per_second = 5
            enable = (int(mytimer.elapsed*blinks_per_second) % 2)
            color = tuple(c * enable for c in self._color_crit)
        elif self.remaining < self.crit:
            color = self._color_crit
        elif self.remaining < self.warn:
            color = self._color_warn
        else:
            color = self._color_okay
        return color

    def is_critical(self):
        return self.remaining < self.crit

    def update(self):
        """ Set the current state
        Call this function from the main while loop
        """
        if self.is_running:
            self.elapsed = time.monotonic() - self.start_time
            self.remaining = self.time - self.elapsed
            if self.remaining < 0:
                self.remaining = 0

neopixels[0] = (0, 255, 0)
neopixels[1] = (0, 0, 0)
neopixels.show()

######################### MAIN LOOP ##############################

mytimer = Timer()
while True:
    mytimer.update()

    if mytimer.is_running:
        dot[0] = (0, 0, 255)
    else:
        dot[0] = (255, 0, 0)

    buzzer.value = False
    if not button0.value:
        mytimer.start()
        dot[0] = (255, 255, 255)
    if not button1.value:
        mytimer.stop()
        dot[0] = (255, 255, 255)
    if not button2.value:
        buzzer.value = True
    print((mytimer.remaining, mytimer.elapsed, ))

    color = mytimer.get_color()
    neopixels[0] = color
    neopixels[1] = color
    neopixels.show()

    # if mytimer.is_critical():
    #     buzzer.value = True

    time.sleep(0.1)
