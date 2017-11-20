import time
import _thread
import RPi.GPIO as GPIO
import pygame
from musicSyncer import musicSync


def firstSection(songObj):
    songObj.allPIN(0)
    time.sleep(3.8)
    # Start chest pin cycle
    _thread.start_new_thread(songObj.cycleGroupPack,
                             (songObj.chestPins, 6.3371, 0, 100, ))
    # Start Eight Pack pin on cycle
    _thread.start_new_thread(songObj.cycleGroupPack,
                             (songObj.eightPacPins, .79, .79, 30, ))
    time.sleep(6.24)
    # Start Eight Pack pin off cycle
    _thread.start_new_thread(songObj.cycleGroupPack,
                             (songObj.eightPacPins, .79, .79, 0, ))
    time.sleep(6.24)
    time.sleep(4.5)
    # Turn off chest pins
    _thread.start_new_thread(songObj.cycleGroupPack,
                             (songObj.chestPins, 0, 0, 0, ))
    print("End 1")


def secondSection(songObj):
    now = time.time() - songObj.timer
    print("start second section")
    print(now)
    pygame.mixer.music.set_pos(20.8)
    sequence = [.005, .007, .004, .007, .004, .004, .004, .007, .004, .007,
                .004, .005]
    # Start two pins on beat fade
    _thread.start_new_thread(songObj.beatFade,
                             (songObj.sidePins[0], 0, 6, sequence, ))
    _thread.start_new_thread(songObj.beatFade,
                             (songObj.rgbPins[2], 0, 6, sequence, ))
    # Start 8 pack cycle
    for i in range(1, 4):
        print("first ", i)
        _thread.start_new_thread(songObj.cycleGroupPack,
                                 (songObj.eightPacPins, .79, 0, 30, ))
        time.sleep(6.24)
        print("Second ", i)
        if i is 1:
            _thread.start_new_thread(songObj.beatFade,
                                     (songObj.sidePins[1], 100, 1, [.04], ))
        if i is not 3:
            _thread.start_new_thread(songObj.cycleGroupPack,
                                     (songObj.eightPacPins, .79, 0, 0, ))
            time.sleep(6.24)

    songObj.allPIN(0)



def main():
    # Define GPIO LED Output Pins
    eightPacPins = [5, 6, 13, 19, 26, 16, 20, 21]
    chestPins = [14, 7, 8]
    sidePins = [9, 11]
    rgbPins = [15, 18, 25]
    buttonPin = 12

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Set up GPIO LED control pins as output
    for i in eightPacPins:
        GPIO.setup(i, GPIO.OUT)
    for i in chestPins:
        GPIO.setup(i, GPIO.OUT)
    for i in sidePins:
        GPIO.setup(i, GPIO.OUT)
    for i in rgbPins:
        GPIO.setup(i, GPIO.OUT)

    # Set up input pin for physical activation button
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Create Music Sync Object
    songObj = musicSync(eightPacPins, chestPins, sidePins, rgbPins)
    # Turn off LEDs incase they were left on for some reason
    songObj.allPIN(0)

    # Load the music to be played
    pygame.mixer.init()
    pygame.mixer.music.load('/home/pi/jbot2.0/mp3/jbot2.ogg')
    # Volume values are between .1 and 1
    pygame.mixer.music.set_volume(1)

    while True:
        input_state = GPIO.input(buttonPin)
        print(GPIO.input)
        if input_state == True:
            print("here")
            # Stop the pusic if it happens to be playing
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
            # The song is divided up into sections to make figuring out the
            # timing of thigs much faster
            songObj.timer = time.time()
            #firstSection(songObj)
            secondSection(songObj)
            #thirdSection(songObj)
            #fourthSection(songObj)
            #fithSection(songObj)
            time.sleep(10)
        else:
            _thread.start_new_thread(songObj.idle, ())
            time.sleep(3)


if __name__ == '__main__':
    main()
