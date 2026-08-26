#!/usr/bin/env bash
# Fullscreen Chromium to Home Assistant (server is not on this Pi).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="$ROOT/config.yaml"
URL="http://homeassistant.local:8123"

if [[ -x "$ROOT/.venv/bin/python" && -f "$CONFIG" ]]; then
  URL="$(
    cd "$ROOT"
    "$ROOT/.venv/bin/python" -c \
      "from ncore_daemon.config import load_settings; print(load_settings('config.yaml').ha_kiosk_url or '')"
  )"
  URL="${URL:-http://homeassistant.local:8123}"
fi

CHROMIUM="$(command -v chromium || true)"
if [[ -z "$CHROMIUM" ]]; then
  CHROMIUM="$(command -v chromium-browser || true)"
fi
if [[ -z "$CHROMIUM" ]]; then
  echo "chromium is not installed" >&2
  exit 1
fi

# Wait until HA (or at least the network) answers so the first paint is not an error page.
for _ in $(seq 1 60); do
  if curl -sf -o /dev/null --max-time 2 "$URL"; then
    break
  fi
  sleep 2
done

# X11 screensaver off; ignored on Wayland.
xset s off -dpms 2>/dev/null || true

exec "$CHROMIUM" \
  --kiosk \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-restore-session-state \
  --no-first-run \
  --check-for-update-interval=31536000 \
  --password-store=basic \
  --app="$URL"
