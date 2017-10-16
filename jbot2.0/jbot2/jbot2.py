import time
import pygame
import RPi.GPIO as GPIO
import sys
import _thread
from jbotClass import musicSync

def firstSection(songObj):
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        time.sleep(3.8)
        GPIO.output(songObj.otherPins[0], GPIO.HIGH)
        _thread.start_new_thread(songObj.cycleRelayOnWorker,(.79, ))
        time.sleep(6.3371)
        GPIO.output(songObj.otherPins[1], GPIO.HIGH)
        _thread.start_new_thread(songObj.cycleRelayOffWorker,(.79, ))
        time.sleep(6.3371)
        GPIO.output(songObj.otherPins[2], GPIO.HIGH)
        time.sleep(3.9)
        pygame.mixer.music.stop()

def secondSection(songObj):
    pygame.mixer.music.rewind()
    pygame.mixer.music.play()
    #pygame.mixer.music.set_pos(21.083037)
    pygame.mixer.music.set_pos(21)
    _thread.start_new_thread(songObj.fade1Worker,())
    while pygame.mixer.music.get_busy() == True:
        count = 1
        for i in range(0, 5):
            print(count)
            count += 1
            for i in songObj.relayPins:
                if songObj.relayPins.index(i) == 0 or songObj.relayPins.index(i)== 8:
                    songObj.allOtherOff()
                    if count > 3:
                        GPIO.output(songObj.fadePins[1], GPIO.HIGH)
                elif songObj.relayPins.index(i)== 4:
                    songObj.allOtherOn()
                    if count > 3:
                        GPIO.output(songObj.fadePins[1], GPIO.LOW)
                time.sleep(.78)
                if count % 2 == 0:
                    GPIO.output(i, GPIO.LOW)
                else:
                    GPIO.output(i, GPIO.HIGH)
        songObj.allRelayOff()
        songObj.allOtherOff()
        time.sleep(6.3)
        pygame.mixer.music.stop()

def thirdSection(songObj):
    pygame.mixer.music.rewind()
    pygame.mixer.music.play()
    pygame.mixer.music.set_pos(59.7)
    while pygame.mixer.music.get_busy() == True:
        _thread.start_new_thread(songObj.beat,())
        for i in range(1, 13):
            if i % 2 != 0:
                _thread.start_new_thread(songObj.longSpanWorker,())
            print(i)
            if i >= 5 and i < 9:
                _thread.start_new_thread(songObj.s3short,())
            if i >= 9:
                _thread.start_new_thread(songObj.dualCycle,())
            songObj.fastRelayCycleOn()
            songObj.fastRelayCycleOff()
            if i > 3 and i < 8:
                if i % 2 != 0:
                    _thread.start_new_thread(songObj.shortThreadWorker,(True,))
                else:
                    _thread.start_new_thread(songObj.shortThreadWorker,())
        sys.exit(1)

def main():
    relayPins = [5, 6, 13, 19, 26, 16, 20, 21]
    otherPins = [23, 24, 25]
    fadePins = [18, 12]
    song = musicSync(relayPins, otherPins, fadePins)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i in song.relayPins:
        GPIO.setup(i, GPIO.OUT)
    for i in song.otherPins:
        GPIO.setup(i, GPIO.OUT)
    for i in song.fadePins:
        GPIO.setup(i, GPIO.OUT)

    song.allRelayOff()
    song.allOtherOff()

    pygame.mixer.init()
    pygame.mixer.music.load('mp3/jbot2.mp3')

    firstSection(song)
    secondSection(song)
    thirdSection(song)

if __name__ == "__main__":
    main()
