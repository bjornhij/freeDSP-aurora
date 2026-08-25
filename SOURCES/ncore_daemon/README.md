# Ncore / aurora daemon

Python-brug tussen de freeDSP aurora (serieel), Hypex Ncore (GPIO) en Home Assistant. Geen Volumio-API. De Java-daemon blijft staan tot deze service draait.

## Installatie op de Pi

```bash
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip
cd ~
git clone <deze-repo>   # of kopieer SOURCES/ncore_daemon
cd ncore_daemon
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-pi.txt   # gpiozero + evdev, alleen op de Pi
cp config.example.yaml config.yaml
# serial_port, gpio_bcm_pin, ir_device_name, ha_webhook_url aanpassen
```

Serial device op de Pi (niet het Mac-pad `/dev/tty.MALS`):

```bash
ls /dev/ttyUSB* /dev/ttyAMA* /dev/serial* 2>/dev/null
```

GPIO: Java Pi4J `GPIO_09` is WiringPi 9 = **BCM 3**. Controleer je bedrading voordat je de amp aanzet.

IR-naam achterhalen (niet hard `event2` vertrouwen):

```bash
python3 - <<'PY'
from evdev import InputDevice, list_devices
for path in list_devices():
    d = InputDevice(path)
    print(path, d.name)
PY
```

Zet `ir_device_name` op een uniek deel van die naam. Fallback blijft `ir_device_path`.

Stop de oude Java-daemon en `ir_bridge.py` voordat je start: twee processen kunnen niet allebei `grab()` op dezelfde IR doen.

```bash
sudo cp systemd/ncore-daemon.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ncore-daemon
```

De unit zit in de groepen `gpio`, `dialout`, `input` en `video` (backlight). User `volumio` aanpassen als je onder een andere account draait.

Dry-run op een Mac (geen GPIO/serial/IR):

```bash
python3 -m ncore_daemon --dry-run
```

API: `http://hypex-amp.local:9090/` (debug-HTML) en `GET /status`.

## Home Assistant

Kopieer `homeassistant/ncore_amp.yaml` naar `configuration.yaml`. Webhook-id is `ncore_updated`. Op de Pi:

```yaml
ha_webhook_url: "http://homeassistant.local:8123/api/webhook/ncore_updated"
```

De entiteit is `media_player.ncore_amp` (receiver: aan/uit, volume, bron). Geen muziekstreaming.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

- Harde cap `max_volume` (80). HA 100% = die cap.
- Boot: amp uit, DSP naar `power_on_volume` (9).
- Power-on: `min(laatste volume, power_on_restore_cap)` (20) naar de DSP, **daarna** GPIO aan. Mislukt de DSP-write, blijft de amp uit.
- Power-off: eerst mute op de DSP, dan GPIO uit.
- Omhoog alleen in stappen van 1 met `volume_step_interval_ms` (150). IR-repeat is 150 ms, niet 1 ms.
- Volume 0 stuurt wel mute naar de DSP.
