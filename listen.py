import configparser, os
from playsound import playsound
from pynput.keyboard import Key, Listener, KeyCode
import time, subprocess as sp

SOUNDPREFIX = 'sounds/'
DELAY = 0.2

config = configparser.ConfigParser()
config.read('keybinds.ini')
print()

def playsound(sound, _):
    sp.Popen(['aplay',sound])


def on_press(key: KeyCode):
    
    # print a spacer
    print()
    global last_sound_time
    # don't play sound if last sound more recent than DELAY
    if (time.time() - last_sound_time) < DELAY:
        return
    print()
    # stop listening if escape pressed
    if key == Key.esc:
        return False
    # make sure key is valid
    try:
        sound = config['KEYBOARD'][key.char]
    except AttributeError:
        return
    except KeyError:
        print(f'{key.char} not defined!')
        return
    # check if sound has been assigned in config
    if not sound:
        print(f'Sound not assigned for {key.char}!')
        return
    # warn and cancel if sound does not exist
    if not os.path.exists(SOUNDPREFIX + sound):
        print(f'Sound {sound} not found!')
        return
    print(sound)
    # play sound asnychronously
    playsound(SOUNDPREFIX + sound, False)
    # record time to prevent spam
    last_sound_time = time.time()
last_sound_time = 0

# Collect events until released
with Listener(on_press=on_press) as listener:
    listener.join()