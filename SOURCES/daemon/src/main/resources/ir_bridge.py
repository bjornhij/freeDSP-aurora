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
            try:
                r = requests.put(url = "http://localhost:9090/volume/up")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

        if event.code == evdev.ecodes.KEY_FN_F2: # volup
            print("voldown")
            try:
                r = requests.put(url = "http://localhost:9090/volume/down")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

        if event.code == evdev.ecodes.KEY_FN_F4: # poweron
            try:
                r = requests.put(url = "http://localhost:9090/state/on")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

            print("poweron")

        if event.code == evdev.ecodes.KEY_FN_F5: # poweroff
            try:
                r = requests.put(url = "http://localhost:9090/state/off")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

            print("poweroff")

        if event.code == evdev.ecodes.KEY_FN_F6: # cd
            try:
                r = requests.put(url = "http://localhost:9090/input/usb")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

            print("usb")

        if event.code == evdev.ecodes.KEY_FN_F7: # dvd
            try:
                r = requests.put(url = "http://localhost:9090/input/optical_1")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

            print("optical_1")

        if event.code == evdev.ecodes.KEY_FN_F8: # dvr/bd
            try:
                r = requests.put(url = "http://localhost:9090/input/optical_2")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

            print("optical_2")

        if event.code == evdev.ecodes.KEY_FN_F9: # tv/sat
            try:
                r = requests.put(url = "http://localhost:9090/input/optical_3")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

            print("optical_3")

        if event.code == evdev.ecodes.KEY_FN_F10: # cd-r
            try:
                r = requests.put(url = "http://localhost:9090/input/analog_1")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

            print("optical_4")

        if event.code == evdev.ecodes.KEY_FN_F11: # video1
            try:
                r = requests.put(url = "http://localhost:9090/input/analog_2")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

            print("analog_1")

        if event.code == evdev.ecodes.KEY_FN_F12: # video2
            try:
                r = requests.put(url = "http://localhost:9090/input/analog_3")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

            print("analog_2")

        if event.code == evdev.ecodes.KEY_FN_ESC: # tuner
            try:
                r = requests.put(url = "http://localhost:9090/input/analog_4")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e

            print("analog_3")
