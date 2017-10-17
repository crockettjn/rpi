import RPi.GPIO as GPIO
import time


class musicSync:

    def __init__(self, relayPins, otherPins, fadePins):
        self.relayPins = relayPins
        self.otherPins = otherPins
        self.fadePins = fadePins
        self.freq = 100
        self.tog = 'LOW'

    def toggle(self):
        if self.tog == 'LOW':
            GPIO.output(self.fadePins[1], GPIO.HIGH)
            self.tog = 'HIGH'
        else:
            GPIO.output(self.fadePins[1], GPIO.LOW)
            self.tog = 'LOW'

    def allOtherOff(self):
        for i in self.otherPins:
            GPIO.output(i, GPIO.LOW)
        for i in self.fadePins:
            GPIO.output(i, GPIO.LOW)

    def allOtherOn(self):
        for i in self.otherPins:
            GPIO.output(i, GPIO.HIGH)

    def allRelayOff(self):
        for i in self.relayPins:
            GPIO.output(i, GPIO.HIGH)

    def cycleRelayOnWorker(self, preSleep=0):
        time.sleep(preSleep)
        for i in self.relayPins:
            GPIO.output(i, GPIO.LOW)
            time.sleep(.79)

    def other2Worker(self):
        time.sleep(.8)
        GPIO.output(self.otherPins[0], GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.otherPins[0], GPIO.LOW)
        GPIO.output(self.otherPins[1], GPIO.HIGH)
        time.sleep(.3)
        GPIO.output(self.otherPins[1], GPIO.LOW)
        GPIO.output(self.otherPins[2], GPIO.HIGH)
        time.sleep(1.2)
        GPIO.output(self.otherPins[2], GPIO.LOW)
        GPIO.output(self.otherPins[0], GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.otherPins[0], GPIO.LOW)
        GPIO.output(self.otherPins[1], GPIO.HIGH)
        time.sleep(.2)
        GPIO.output(self.otherPins[1], GPIO.LOW)
        GPIO.output(self.otherPins[2], GPIO.HIGH)
        time.sleep(.2)
        GPIO.output(self.otherPins[2], GPIO.LOW)
        GPIO.output(self.otherPins[0], GPIO.HIGH)
        time.sleep(2.3)
        GPIO.output(self.otherPins[0], GPIO.LOW)
        GPIO.output(self.otherPins[1], GPIO.HIGH)
        time.sleep(.2)
        GPIO.output(self.otherPins[1], GPIO.LOW)
        GPIO.output(self.otherPins[2], GPIO.HIGH)
        time.sleep(1.7)
        GPIO.output(self.otherPins[2], GPIO.LOW)
        GPIO.output(self.otherPins[0], GPIO.HIGH)

    def cycleRelayOffWorker(self, preSleep=0):
        time.sleep(preSleep)
        for i in self.relayPins:
            GPIO.output(i, GPIO.HIGH)
            time.sleep(.79)

    def otherFadeWorker(self):
        PIN1 = GPIO.PWM(self.otherPins[0], self.freq)
        PIN2 = GPIO.PWM(self.otherPins[1], self.freq)
        PIN3 = GPIO.PWM(self.otherPins[2], self.freq)
        PIN1.start(0)
        PIN2.start(0)
        PIN3.start(0)
        for x in range(1, 100):
            PIN1.ChangeDutyCycle(101-x)
            PIN2.ChangeDutyCycle(101-x)
            PIN3.ChangeDutyCycle(101-x)
            time.sleep(.02)

    def fade1Worker(self, repeat):
        PIN = GPIO.PWM(self.fadePins[0], self.freq)

        def beatDuration(sleep):
            for x in range(1, 100):
                PIN.ChangeDutyCycle(101-x)
                time.sleep(sleep)
        PIN.start(0)
        # for i in range(0, 6):
        #    print(i)
        beatDuration(.011)
        beatDuration(.004)
        beatDuration(.009)
        beatDuration(.004)
        beatDuration(.004)
        beatDuration(.004)
        beatDuration(.007)
        beatDuration(.004)
        beatDuration(.007)
        beatDuration(.004)
        beatDuration(.005)
        # print("here")
        beatDuration(.004)
        beatDuration(.007)
        beatDuration(.004)
        beatDuration(.007)
        beatDuration(.004)
        beatDuration(.004)
        beatDuration(.004)
        beatDuration(.007)
        beatDuration(.004)
        beatDuration(.007)
        beatDuration(.004)
        beatDuration(.005)
        # print('here')
        for x in range(1, repeat):
            beatDuration(.005)
            beatDuration(.007)
            beatDuration(.004)
            beatDuration(.007)
            beatDuration(.004)
            beatDuration(.004)
            beatDuration(.004)
            beatDuration(.007)
            beatDuration(.004)
            beatDuration(.007)
            beatDuration(.004)
            beatDuration(.005)

    def shortThreadWorker(self, stat=False):
        if stat:
            GPIO.output(self.otherPins[1], GPIO.LOW)
        else:
            GPIO.output(self.otherPins[1], GPIO.HIGH)

    def fastRelayCycleOn(self, sleep=.195):
        for i in self.relayPins:
            GPIO.output(i, GPIO.LOW)
            time.sleep(sleep)

    def fastRelayCycleOff(self, sleep=.195):
        for i in self.relayPins:
            GPIO.output(i, GPIO.HIGH)
            time.sleep(sleep)

    def s3short(self):
        stime = .4
        for i in range(1, 5):
            GPIO.output(self.fadePins[0], GPIO.HIGH)
            time.sleep(stime)
            GPIO.output(self.fadePins[0], GPIO.LOW)
            time.sleep(stime)

    def dualCycle(self):
        stime = .2
        for i in range(1, 9):
            GPIO.output(self.fadePins[0], GPIO.HIGH)
            GPIO.output(self.fadePins[1], GPIO.LOW)
            time.sleep(stime)
            GPIO.output(self.fadePins[0], GPIO.LOW)
            GPIO.output(self.fadePins[1], GPIO.HIGH)
            time.sleep(stime)

    def beat(self):
        BLUE = GPIO.PWM(self.otherPins[2], self.freq)

        def beatDuration(sleep):
            for x in range(1, 100):
                BLUE.ChangeDutyCycle(101-x)
                time.sleep(sleep)
        BLUE.start(100)
        for i in range(0, 6):
            beatDuration(.011)
            beatDuration(.008)
            beatDuration(.011)
            beatDuration(.006)
            beatDuration(.006)
            beatDuration(.008)
            beatDuration(.00125)
            beatDuration(.006)
            beatDuration(.005)

    def longSpanWorker(self):
        YELLOW = GPIO.PWM(self.otherPins[0], self.freq)
        YELLOW.start(100)
        for x in range(1, 100):
            YELLOW.ChangeDutyCycle(101-x)
            time.sleep(0.06)
