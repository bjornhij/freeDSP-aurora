import evdev
import requests

device = evdev.InputDevice('/dev/input/event2')
device.grab()
device.repeat = evdev.device.KbdInfo(repeat = 1, delay = 500)

print(device)

for event in device.read_loop():

    if event.value == 2:
        if event.code == evdev.ecodes.KEY_FN_F1: # volup
            print("volup")
            r = requests.put(url = "http://localhost:9090/volume/up")

        if event.code == evdev.ecodes.KEY_FN_F2: # volup
            print("voldown")
            r = requests.put(url = "http://localhost:9090/volume/down")

