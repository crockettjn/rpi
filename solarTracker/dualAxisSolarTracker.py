#!/usr/bin/python
import time
import RPi.GPIO as GPIO


def main():
    GPIO.setmode(GPIO.BOARD)
    # init lists with pin numbers
    relayPinList = [31, 33, 35, 37]
    ldrPinList = [7, 11, 95, 96]

    # loop through relay pins and set mode and state to 'low'
    for i in relayPinList:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)
    # Main Loop,  Catch when script is interupted, cleanup correctly
    try:
        while True:
            north = rc_time(ldrPinList[1])
            south = rc_time(ldrPinList[2])
            east = rc_time(ldrPinList[3])
            west = rc_time(ldrPinList[4])

            tilt('ns', north, south, relayPinList[1], relayPinList[1])
            tilt('ew', east, west, relayPinList[3], relayPinList[4])

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


def log(message):
    print(message)
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    f = open('solarTracker.log', 'w')
    f.write(ts, message)
    f.close()


def toggleRelay(pin):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(2)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(2)


def rc_time(pin):
    count = 0
    # Output on the pin for
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    # Change the pin back to input
    GPIO.setup(pin, GPIO.IN)
    # Count until the pin goes high
    while (GPIO.input(pin) == GPIO.LOW):
        count += 1
    return float(count)


def tilt(direction, cord1, cord2, pin1, pin2):
    difference = (cord1 / cord2) * 100
    if difference > 115 or difference < 85:
        log('The Difference is {}, adjusting'.format(difference))
        if cord1 > cord2:
            log('Tilting North') if direction is 'ns' else log('Tilting East')
            toggleRelay(pin1)
        else:
            log('Tilting South') if direction is 'ns' else log('Tilting West')
            toggleRelay(pin2)
    else:
        log('The difference is {}, no adjustment needed'.format(difference))

if __name__ == '__main__':
    main()
