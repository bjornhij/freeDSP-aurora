# Ncore / aurora daemon

Python-brug tussen de freeDSP aurora (serieel), Hypex Ncore (GPIO), het scherm, en Home Assistant. Geen Volumio, geen Docker. Home Assistant draait **elders**; deze Pi 4 toont de UI fullscreen en bedient de amp.

## Kale installatie (Raspberry Pi 4)

### 1. Imager

Raspberry Pi Imager, **Raspberry Pi OS (64-bit) met desktop** (niet Lite — Chromium-kiosk heeft een GUI nodig):

- hostname: `hypex-amp`
- SSH aan
- gebruiker: `ncore` (niet `volumio`)
- wifi of ethernet

Eerste boot:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo raspi-config
```

In raspi-config: **System Options → Auto Login** (desktop). **I2C niet aanzetten** als AMPON op BCM 3 blijft: dat is I2C1 SCL (`GPIO3`).

### 2. Code en service

Kopieer deze map naar `/home/ncore/ncore_daemon` (git clone van de repo en `cd SOURCES/ncore_daemon`, of rsync).

```bash
cd /home/ncore/ncore_daemon
chmod +x scripts/install.sh scripts/ha-kiosk.sh
./scripts/install.sh
```

Dat zet een venv, `config.yaml`, systemd `ncore-daemon` en Chromium-kiosk autostart. Log daarna opnieuw in zodat de groepen `gpio`, `dialout`, `input` en `video` gelden.

### 3. Scherm herkennen

Op een draaiende Pi (ook de oude):

```bash
cat /proc/device-tree/model; echo
ls /sys/class/backlight/
ls /sys/class/drm/
grep -hE 'dtoverlay|display|hdmi|dsi|lcd' /boot/firmware/config.txt /boot/config.txt 2>/dev/null
```

- Map `rpi_backlight` = official 7" DSI. **Dit is de huidige hypex-amp** (Pi 4B 1.2). Amp aan zet backlight op 80, amp uit op 0.
- `hdmi_force_hotplug=1` kan naast DSI in config.txt staan (tweede HDMI of oude workaround). Ontbreekt `rpi_backlight`, dan HDMI via `vcgencmd display_power`.
- Geen `/sys/class/drm/` op oude Volumio/legacy-graphics is normaal; op verse Pi OS desktop bestaat die map wél.

### 4. Hardware in `config.yaml`

**Serial (aurora)** — niet het Mac-pad `/dev/tty.MALS`:

```bash
ls /dev/serial/by-id /dev/ttyUSB* 2>/dev/null
```

Zet `serial_port` op de `by-id`-symlink (blijft gelijk na reboot).

**IR:**

```bash
python3 - <<'PY'
from evdev import InputDevice, list_devices
for path in list_devices():
    d = InputDevice(path)
    print(path, d.name)
PY
```

Zet `ir_device_name` op een uniek stuk van die naam. USB-IR verschijnt vanzelf; GPIO-IR: `dtoverlay=gpio-ir` in `/boot/firmware/config.txt`.

**GPIO:** BCM 3, HIGH = amp uit. Eerste keer `dry_run: true` of speakers los tot de pin klopt.

**Home Assistant:**

```yaml
ha_kiosk_url: "http://homeassistant.local:8123"
ha_webhook_url: "http://homeassistant.local:8123/api/webhook/ncore_updated"
```

Kiosk-login eenmalig in Chromium. Als het scherm leeg blijft op Wayland: raspi-config → Advanced → Wayland → **X11**, reboot.

```bash
sudo systemctl restart ncore-daemon
curl -s http://127.0.0.1:9090/status
```

`serial_ok` / `gpio_ok` / `ir_ok` moeten kloppen. Debug-UI: `http://hypex-amp.local:9090/`.

## Home Assistant (op de server)

Kopieer `homeassistant/ncore_amp.yaml` naar `configuration.yaml`. Webhook-id: `ncore_updated`. Entiteit: `media_player.ncore_amp` (aan/uit, volume, bron — geen muziekstreaming).

### Kiosk-login (eenmaal, of nooit)

Chromium bewaart de sessie in `~/.config/chromium`. Eerste keer: aparte HA-user `kiosk` (geen admin), inloggen, **Keep me logged in**.

Zonder login-scherm: trusted networks + één user voor het Pi-IP. Alleen `allow_bypass_login` zonder `trusted_users` logt automatisch in als er **één** HA-user is; bij meerdere users krijg je een keuzelijst. Koppel het IP daarom aan het kiosk-user-id:

```yaml
homeassistant:
  auth_providers:
    - type: trusted_networks
      trusted_networks:
        - 192.168.1.50/32
      trusted_users:
        192.168.1.50:
          - 0123456789abcdef0123456789abcdef
      allow_bypass_login: true
    - type: homeassistant
```

User-id: Instellingen → Personen → user openen; id staat in de URL (`/config/users/<id>`). `homeassistant` als tweede provider laten staan, anders kun je vanaf andere IP’s niet meer met wachtwoord inloggen. Daarna HA herstarten.

Niet het Chromium-profiel wissen en niet als admin in de kiosk inloggen.

## Volume-bescherming

- Harde cap `max_volume` (80). HA 100% = die cap.
- Boot: amp uit, DSP naar `power_on_volume` (9).
- Power-on: `min(laatste volume, power_on_restore_cap)` (20) naar de DSP, **daarna** GPIO aan.
- Power-off: eerst mute op de DSP, dan GPIO uit (en scherm uit).
- Omhoog alleen in stappen van 1 (`volume_step_interval_ms` 150). IR-repeat 150 ms.
- Volume 0 stuurt wel mute naar de DSP.

## Dry-run / tests (Mac)

```bash
python3 -m ncore_daemon --dry-run
pip install -r requirements-dev.txt
python -m pytest
```
