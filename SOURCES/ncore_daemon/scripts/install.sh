#!/usr/bin/env bash
# Install ncore-daemon + optional Home Assistant Chromium kiosk on Raspberry Pi OS.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INSTALL_USER="${SUDO_USER:-$(id -un)}"
INSTALL_HOME="$(getent passwd "$INSTALL_USER" | cut -d: -f6)"
if [[ -z "$INSTALL_HOME" ]]; then
  echo "Cannot resolve home for $INSTALL_USER" >&2
  exit 1
fi

run_root() {
  if [[ "$(id -u)" -eq 0 ]]; then
    "$@"
  else
    sudo "$@"
  fi
}

as_user() {
  if [[ "$(id -un)" == "$INSTALL_USER" ]]; then
    "$@"
  else
    sudo -u "$INSTALL_USER" "$@"
  fi
}

echo "Installing for user $INSTALL_USER ($INSTALL_HOME)"
echo "Project root: $ROOT"

run_root apt-get update
run_root apt-get install -y python3-venv python3-pip python3-lgpio chromium curl
run_root usermod -aG gpio,dialout,input,video "$INSTALL_USER"

as_user python3 -m venv "$ROOT/.venv"
as_user "$ROOT/.venv/bin/pip" install --upgrade pip
as_user "$ROOT/.venv/bin/pip" install -r "$ROOT/requirements.txt" -r "$ROOT/requirements-pi.txt"

if [[ ! -f "$ROOT/config.yaml" ]]; then
  as_user cp "$ROOT/config.example.yaml" "$ROOT/config.yaml"
  echo "Created $ROOT/config.yaml — edit serial_port, ir_device_name, ha_kiosk_url, ha_webhook_url"
fi

UNIT_SRC="$ROOT/systemd/ncore-daemon.service"
UNIT_DST="/etc/systemd/system/ncore-daemon.service"
TMP_UNIT="$(mktemp)"
sed \
  -e "s|^User=.*|User=${INSTALL_USER}|" \
  -e "s|^Group=.*|Group=${INSTALL_USER}|" \
  -e "s|^WorkingDirectory=.*|WorkingDirectory=${ROOT}|" \
  -e "s|^ExecStart=.*|ExecStart=${ROOT}/.venv/bin/python -m ncore_daemon --config ${ROOT}/config.yaml|" \
  "$UNIT_SRC" > "$TMP_UNIT"
run_root cp "$TMP_UNIT" "$UNIT_DST"
rm -f "$TMP_UNIT"
run_root systemctl daemon-reload
run_root systemctl enable --now ncore-daemon.service

AUTOSTART_DIR="$INSTALL_HOME/.config/autostart"
as_user mkdir -p "$AUTOSTART_DIR"
DESKTOP="$AUTOSTART_DIR/ha-kiosk.desktop"
as_user tee "$DESKTOP" >/dev/null <<EOF
[Desktop Entry]
Type=Application
Name=Home Assistant kiosk
Comment=Fullscreen Home Assistant UI
Exec=${ROOT}/scripts/ha-kiosk.sh
X-GNOME-Autostart-enabled=true
Terminal=false
EOF
run_root chmod +x "$ROOT/scripts/ha-kiosk.sh"

echo
echo "Daemon: sudo systemctl status ncore-daemon"
echo "Log in again so gpio/dialout/input/video groups apply."
echo "Desktop autologin: sudo raspi-config → System Options → Auto Login"
echo "If Chromium kiosk is blank on Wayland: raspi-config → Advanced → Wayland → X11, then reboot."
echo "Do not enable I2C (dtparam=i2c_arm) while AMPON is BCM 3."
