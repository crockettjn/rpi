import time
import pygame
import RPi.GPIO as GPIO
import _thread
from jbotClass import musicSync


def firstSection(songObj):
    time.sleep(3.8)
    GPIO.output(songObj.otherPins[0], GPIO.HIGH)
    _thread.start_new_thread(songObj.cycleRelayOnWorker, (.79, ))
    time.sleep(6.3371)
    GPIO.output(songObj.otherPins[1], GPIO.HIGH)
    _thread.start_new_thread(songObj.cycleRelayOffWorker, (.79, ))
    time.sleep(6.3371)
    GPIO.output(songObj.otherPins[2], GPIO.HIGH)
    time.sleep(4.5)


def secondSection(songObj):
    print('SecondSection')
    pygame.mixer.music.set_pos(21.083037)
    # pygame.mixer.music.set_pos(21)
    _thread.start_new_thread(songObj.fade1Worker, (4, ))
    count = 1
    for i in range(0, 5):
        print(count)
        count += 1
        for i in songObj.relayPins:
            if (songObj.relayPins.index(i) == 0
               or songObj.relayPins.index(i) == 8):
                songObj.allOtherOff()
                if count > 3:
                    GPIO.output(songObj.fadePins[1], GPIO.HIGH)
            elif songObj.relayPins.index(i) == 4:
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
    time.sleep(7)


def thirdSection(songObj):
    print('ThirdSection')
    pygame.mixer.music.set_pos(59)
    _thread.start_new_thread(songObj.beat, ())
    for i in range(1, 13):
        if i % 2 != 0:
            _thread.start_new_thread(songObj.longSpanWorker, ())
        print(i)
        if i >= 5 and i < 9:
            _thread.start_new_thread(songObj.s3short, ())
        if i >= 9:
            _thread.start_new_thread(songObj.dualCycle, ())
        songObj.fastRelayCycleOn()
        songObj.fastRelayCycleOff()
        if i > 3 and i < 8:
            if i % 2 != 0:
                _thread.start_new_thread(songObj.shortThreadWorker, (True,))
            else:
                _thread.start_new_thread(songObj.shortThreadWorker, ())


def fourthSection(songObj):
    print('FourthSection')
    pygame.mixer.music.set_pos(96.71)
    # pygame.mixer.music.set_pos(109.71)
    _thread.start_new_thread(songObj.fade1Worker, (9, ))
    time.sleep(12.2)
    _thread.start_new_thread(songObj.other2Worker, ())
    count = 1
    time.sleep(.3)
    for i in range(0, 6):
        count += 1
        counter1 = 1
        counter2 = 2
        for i in songObj.relayPins:
            if count % 2 == 0:
                GPIO.output(i, GPIO.LOW)
                print(str(count), str(counter1) + " Even")
                if count == 2 and (counter1 == 1 or counter1 == 5):
                    songObj.togglePin(songObj.fadePins[1])
                elif (count == 4 or count == 6) and counter1 == 5:
                    songObj.togglePin(songObj.fadePins[1])
                if (count == 4 or count == 6) and counter1 == 1:
                    _thread.start_new_thread(songObj.otherFadeWorker, ())
                counter1 += 1
            else:
                GPIO.output(i, GPIO.HIGH)
                print(count, counter2)
                if ((count == 3 or count == 5 or count == 7)
                   and (counter2 == 2 or counter2 == 6)):
                    songObj.togglePin(songObj.fadePins[1])
                counter2 += 1
            time.sleep(.78)
    songObj.allRelayOff()
    songObj.allOtherOff()

    _thread.start_new_thread(songObj.fastBeat, (.02, ))
    time.sleep(3)
    _thread.start_new_thread(songObj.fastBeat, (.02, ))
    time.sleep(3.1)
    _thread.start_new_thread(songObj.fastBeat, (.01, ))
    time.sleep(1.5)
    _thread.start_new_thread(songObj.fastBeat, (.01, ))
    time.sleep(1.6)
    _thread.start_new_thread(songObj.fastBeat, (.008, ))
    time.sleep(1)
    _thread.start_new_thread(songObj.fastBeat, (.008, ))
    time.sleep(.9)
    _thread.start_new_thread(songObj.fastBeat, (.003, )) #7
    time.sleep(.31)
    _thread.start_new_thread(songObj.fastBeat, (.002, ))
    time.sleep(.22)
    _thread.start_new_thread(songObj.fastBeat, (.002, ))
    time.sleep(.22)
    _thread.start_new_thread(songObj.fastBeat, (.002, ))
    time.sleep(.22)
    _thread.start_new_thread(songObj.fastBeat, (.002, ))
    time.sleep(.22)
    _thread.start_new_thread(songObj.fastBeat, (.002, ))



    time.sleep(600)

def fithSection(songObj):
    print('FithSection')
    #pygame.mixer.music.set_pos(146.73)

def main():
    # Define GPIO pins for LED control
    relayPins = [5, 6, 13, 19, 26, 16, 20, 21]
    otherPins = [23, 24, 25]
    fadePins = [18, 12]
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Set up GPIO LED control pins as output
    for i in relayPins:
        GPIO.setup(i, GPIO.OUT)
    for i in otherPins:
        GPIO.setup(i, GPIO.OUT)
    for i in fadePins:
        GPIO.setup(i, GPIO.OUT)
    song = musicSync(relayPins, otherPins, fadePins)
    song.allRelayOff()
    song.allOtherOff()

    pygame.mixer.init()
    pygame.mixer.music.load('mp3/jbot2.mp3')
    pygame.mixer.music.play()
    print(time.time())

    #firstSection(song)
    #secondSection(song)
    #thirdSection(song)
    fourthSection(song)
    fithSection(song)

    print(time.time())


if __name__ == "__main__":
    main()
