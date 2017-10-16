import time
import pygame
import RPi.GPIO as GPIO
import sys
import _thread

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
freq = 100
relay = [5, 6, 13, 19, 26, 16, 20, 21]
for i in relay:
    GPIO.setup(i, GPIO.OUT)
other = [23, 24, 25, 18, 12]
for i in other:
    GPIO.setup(i, GPIO.OUT)

def allOtherOff():
    for i in other:
        GPIO.output(i, GPIO.LOW)

def allOtherOn():
    for i in other:
        GPIO.output(i, GPIO.HIGH)

def allRelayOff():
    for i in relay:
        GPIO.output(i, GPIO.HIGH)

allRelayOff()
allOtherOff()

def cycleRelayOn():
    for i in relay:
        time.sleep(.79)
        GPIO.output(i, GPIO.LOW)

def cycleRelayOff():
    for i in relay:
        time.sleep(.79)
        GPIO.output(i, GPIO.HIGH)

def start1():
    time.sleep(3.8)
    GPIO.output(other[0], GPIO.HIGH)
    cycleRelayOn()
    GPIO.output(other[1], GPIO.HIGH)
    cycleRelayOff()
    GPIO.output(other[2], GPIO.HIGH)
    time.sleep(3.8)
    time.sleep(.79)
    count = 1
    for i in range(0, 5):
        #print(count)
        count += 1
        for i in relay:
            if relay.index(i) == 0 or relay.index(i)== 8:
                allOtherOff()
            elif relay.index(i)== 4:
                allOtherOn()
            time.sleep(.78)
            if count % 2 == 0:
                GPIO.output(i, GPIO.LOW)
            else:
                GPIO.output(i, GPIO.HIGH)

pygame.mixer.init()
pygame.mixer.music.load('mp3/jbot2.mp3')

def firstSection():
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        start1()
        allRelayOff()
        allOtherOff()
        time.sleep(6.7)
        pygame.mixer.music.stop()

def shortThread(stat = False):
    if stat:
        print("TRUE")
        GPIO.output(other[1], GPIO.LOW)
    else:
        print("FALSE")
        GPIO.output(other[1], GPIO.HIGH)

def fastRelayCycleOn(sleep = .195):
    for i in relay:
        GPIO.output(i, GPIO.LOW)
        time.sleep(sleep)

def fastRelayCycleOff(sleep = .195):
    for i in relay:
        GPIO.output(i, GPIO.HIGH)
        time.sleep(sleep)

def beat():
    BLUE = GPIO.PWM(other[2], freq)
    def beatDuration(sleep):
        for x in range(1,100):
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

def longSpan():
    YELLOW = GPIO.PWM(other[0], freq)
    YELLOW.start(100)
    for x in range(1, 100):
        YELLOW.ChangeDutyCycle(101-x)
        time.sleep(0.06)

def secondSection():
    pygame.mixer.music.play()
    pygame.mixer.music.rewind()
    pygame.mixer.music.set_pos(59)
    while pygame.mixer.music.get_busy() == True:
        _thread.start_new_thread(beat,())
        for i in range(1, 13):
            if i % 2 != 0:
                _thread.start_new_thread(longSpan,())
            print(i)
            fastRelayCycleOn()
            fastRelayCycleOff()
            if i > 3 and i < 8:
                if i % 2 != 0:
                    _thread.start_new_thread(shortThread,(True,))
                else:
                    _thread.start_new_thread(shortThread,())
        sys.exit(1)

def main():
    firstSection()
    secondSection()

if __name__ == "__main__":
    main()
