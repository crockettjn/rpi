#!/usr/bin/python
import time
import RPi.GPIO as GPIO


def main():
    GPIO.setmode(GPIO.BOARD)
    # init lists with pin numbers
    relayPin = 23

    # loop through relay pins and set mode and state to 'low'
    GPIO.setup(relayPin, GPIO.OUT)
    GPIO.output(relayPin, GPIO.HIGH)
    # Main Loop,  Catch when script is interupted, cleanup correctly

    toggleRelay(relayPin)

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


if __name__ == '__main__':
    main()
