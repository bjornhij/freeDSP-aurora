from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class AmpGpio:
    """Hypex AMPON: pin HIGH = off, pin LOW = on (Java Pi4J GPIO_09)."""

    def __init__(self, bcm_pin: int, dry_run: bool = False):
        self.bcm_pin = bcm_pin
        self.dry_run = dry_run
        self.gpio_ok = True
        self.amp_on = False
        self.history: list[bool] = []
        self._device = None

        if dry_run:
            logger.info("GPIO dry-run on BCM %s (HIGH=off, LOW=on)", bcm_pin)
            return

        try:
            from gpiozero import DigitalOutputDevice

            # Start HIGH so the amp is off before anything else runs.
            self._device = DigitalOutputDevice(
                bcm_pin, active_high=True, initial_value=True
            )
            self.gpio_ok = True
        except Exception:
            self._device = None
            self.gpio_ok = False
            logger.exception("Failed to claim GPIO BCM %s", bcm_pin)

    def set_amp(self, on: bool) -> None:
        self.history.append(on)
        if self.dry_run:
            self.amp_on = on
            self.gpio_ok = True
            logger.info("GPIO dry-run amp %s", "on" if on else "off")
            return
        if self._device is None:
            self.gpio_ok = False
            raise RuntimeError("GPIO is not available")
        try:
            if on:
                self._device.off()  # LOW
            else:
                self._device.on()  # HIGH
            self.amp_on = on
            self.gpio_ok = True
        except Exception:
            self.gpio_ok = False
            logger.exception("GPIO write failed")
            raise

    def close(self) -> None:
        if self._device is not None:
            try:
                self._device.on()
                self._device.close()
            except Exception:
                logger.exception("Error closing GPIO")
            self._device = None
