#!/usr/bin/python
import time
import RPi.GPIO as io
io.setmode(io.BCM)

openStop = 5
closeStop = 6
doorState = 'none'

io.setup(openStop, io.IN, pull_up_down=io.PUD_UP)
io.setup(closeStop, io.IN, pull_up_down=io.PUD_UP)

while True:
    if io.input(openStop):
        ts = False
    else:
        ts = True
    time.sleep(0.5)
    if io.input(closeStop):
        bs = False
    else:
        bs = True

    if ts == True:
        print('The Door is open')
        doorState = 'open'
    elif bs == True:
        print('The Door is closed')
        doorState = 'closed'
    else:
        if doorState == 'open':
            print('The Door is closing')
        else:
            print('The Door is Opening')
