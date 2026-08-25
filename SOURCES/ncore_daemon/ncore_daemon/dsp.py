from __future__ import annotations

import asyncio
import logging

from ncore_daemon.sources import format_message, source_commands

logger = logging.getLogger(__name__)


class Dsp:
    def __init__(self, port: str, baud: int, dry_run: bool = False):
        self.port = port
        self.baud = baud
        self.dry_run = dry_run
        self.serial_ok = False
        self.sent: list[str] = []
        self._serial = None
        self._lock = asyncio.Lock()

    def connect(self) -> None:
        if self.dry_run:
            self.serial_ok = True
            logger.info("DSP dry-run: not opening %s", self.port)
            return
        try:
            import serial  # type: ignore

            self._serial = serial.Serial(self.port, self.baud, timeout=1)
            self.serial_ok = True
            logger.info("Opened DSP serial %s @ %s", self.port, self.baud)
        except Exception:
            self._serial = None
            self.serial_ok = False
            logger.exception("Failed to open DSP serial %s", self.port)

    def close(self) -> None:
        if self._serial is not None:
            try:
                self._serial.close()
            except Exception:
                logger.exception("Error closing serial port")
            self._serial = None

    async def send(self, handler: str, data: str) -> None:
        message = format_message(handler, data)
        async with self._lock:
            self.sent.append(message.rstrip("\n"))
            if self.dry_run:
                logger.info("DSP dry-run send: %s", message.rstrip())
                self.serial_ok = True
                return
            if self._serial is None:
                self.serial_ok = False
                raise RuntimeError("DSP serial is not connected")
            try:
                await asyncio.to_thread(self._write, message)
                self.serial_ok = True
            except Exception:
                self.serial_ok = False
                logger.exception("DSP serial write failed")
                raise

    def _write(self, message: str) -> None:
        self._serial.write(message.encode("ascii"))
        self._serial.flush()

    async def set_master_volume(self, db: int) -> None:
        await self.send("/mvol", str(int(db)))

    async def set_source(self, source: str) -> None:
        for handler, data in source_commands(source):
            await self.send(handler, data)

    async def reset(self) -> None:
        await self.send("/reset", "true")
