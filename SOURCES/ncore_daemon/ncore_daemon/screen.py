from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Screen:
    def __init__(self, path: str, max_brightness: int = 80, dry_run: bool = False):
        self.path = Path(path)
        self.max_brightness = max_brightness
        self.dry_run = dry_run
        self.brightness = 0

    def set_on(self) -> None:
        self._write(self.max_brightness)

    def set_off(self) -> None:
        self._write(0)

    def _write(self, value: int) -> None:
        self.brightness = value
        if self.dry_run:
            logger.info("Screen dry-run brightness %s", value)
            return
        try:
            self.path.write_text(str(value), encoding="ascii")
        except OSError:
            logger.exception("Failed to set backlight %s", self.path)
