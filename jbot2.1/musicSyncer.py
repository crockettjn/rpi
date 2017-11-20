import time
from random import randint
import RPi.GPIO as GPIO


class musicSync:
    def __init__(self, eightPacPins, chestPins, sidePins, rgbPins):
        self.eightPacPins = self.pmwSetup(eightPacPins)
        self.chestPins = self.pmwSetup(chestPins)
        self.sidePins = self.pmwSetup(sidePins)
        self.rgbPins = self.pmwSetup(rgbPins)
        self.timer = None

    def pmwSetup(self, pinVar):
        pinpmw = {}
        count = 0
        for i in pinVar:
            pinpmw[count] = GPIO.PWM(i, 100)
            count += 1
        return pinpmw

    def allPIN(self, powerlvl):
        self.cycleGroupPack(self.eightPacPins, 0, 0, 0)
        self.cycleGroupPack(self.chestPins, 0, 0, 0)
        self.cycleGroupPack(self.sidePins, 0, 0, 0)
        self.cycleGroupPack(self.rgbPins, 0, 0, 0)

    def idle(self, powerlvl=30, sleep=.03):
        powerlvl = 30
        sleep = .03
        num = randint(0, 7)
        self.eightPacPins[num].start(0)
        for x in range(1, powerlvl):
            self.eightPacPins[num].ChangeDutyCycle(1+x)
            time.sleep(sleep)
        for x in range(1, powerlvl):
            self.eightPacPins[num].ChangeDutyCycle(powerlvl-x)
            time.sleep(sleep)
            self.eightPacPins[num].start(0)

    def cycleGroupPack(self, group, sleep, preSleep, powerlvl):
        time.sleep(preSleep)
        for key, value in group.items():
            value.start(powerlvl)
            time.sleep(sleep)

    def singlePinChangeState(self, pinObj, powerlvl):
        pinObj.start(powerlvl)

    def beatFade(self, pinObj, start, repeat, sequence):

        def beatDuration(sleep, pinObj):
            for x in range(1, 100):
                pinObj.ChangeDutyCycle(101-x)
                time.sleep(sleep)
        pinObj.start(start)
        for r in range(1, repeat):
            for i in sequence:
                beatDuration(i, pinObj)
        pinObj.start(0)
