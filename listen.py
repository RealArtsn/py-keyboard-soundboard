import configparser, os
from playsound import playsound
from pynput.keyboard import Key, Listener, KeyCode

SOUNDPREFIX = 'sounds/'

config = configparser.ConfigParser()
config.read('keybinds.ini')


def on_press(key: KeyCode):
    # print a spacer
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

# Collect events until released
with Listener(on_press=on_press) as listener:
    listener.join()