from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class Screen:
    def __init__(
        self,
        path: str,
        max_brightness: int = 80,
        dry_run: bool = False,
        hdmi_power: bool = True,
    ):
        self.path = Path(path)
        self.max_brightness = max_brightness
        self.dry_run = dry_run
        self.hdmi_power = hdmi_power
        self.brightness = 0

    def set_on(self) -> None:
        self._write_backlight(self.max_brightness)
        self._set_hdmi_power(True)

    def set_off(self) -> None:
        self._write_backlight(0)
        self._set_hdmi_power(False)

    def _backlight_available(self) -> bool:
        return self.path.exists()

    def _write_backlight(self, value: int) -> None:
        self.brightness = value
        if self.dry_run:
            logger.info("Screen dry-run brightness %s", value)
            return
        if not self._backlight_available():
            logger.info("No backlight at %s", self.path)
            return
        try:
            self.path.write_text(str(value), encoding="ascii")
        except OSError:
            logger.exception("Failed to set backlight %s", self.path)

    def _set_hdmi_power(self, on: bool) -> None:
        if self.dry_run or not self.hdmi_power:
            return
        if self._backlight_available():
            return
        try:
            subprocess.run(
                ["vcgencmd", "display_power", "1" if on else "0"],
                check=False,
                capture_output=True,
                timeout=3,
            )
            logger.info("HDMI display_power %s", "on" if on else "off")
        except (OSError, subprocess.TimeoutExpired):
            logger.warning("vcgencmd display_power failed", exc_info=True)
