from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Optional

from ncore_daemon.sources import SOURCE_LIST
from ncore_daemon.volume import (
    clamp_volume,
    linear_to_db,
    restore_volume,
    volume_to_ha_level,
)
from ncore_daemon.webhook import notify_ha

logger = logging.getLogger(__name__)


class Amp:
    def __init__(self, settings, dsp, gpio, screen, store, webhook_url: str = ""):
        self.settings = settings
        self.dsp = dsp
        self.gpio = gpio
        self.screen = screen
        self.store = store
        self.webhook_url = webhook_url

        self.state = "off"
        self.volume = settings.power_on_volume
        self.source = "usb"
        self.ir_ok = False

        self._target = settings.power_on_volume
        self._ramp_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()
        self._last_increase = 0.0

    @property
    def serial_ok(self) -> bool:
        return bool(self.dsp.serial_ok)

    @property
    def gpio_ok(self) -> bool:
        return bool(self.gpio.gpio_ok)

    def status(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "volume": self.volume,
            "volume_level": volume_to_ha_level(self.volume, self.settings.max_volume),
            "source": self.source,
            "source_list": list(SOURCE_LIST),
            "serial_ok": self.serial_ok,
            "gpio_ok": self.gpio_ok,
            "ir_ok": self.ir_ok,
            "max_volume": self.settings.max_volume,
        }

    async def start(self) -> None:
        try:
            self.gpio.set_amp(False)
        except Exception:
            logger.exception("GPIO off at boot failed")
        self.state = "off"
        self.screen.set_off()

        stored = self.store.load()
        stored_source = stored.get("source")
        if stored_source in SOURCE_LIST:
            self.source = stored_source
        last = stored.get("volume")
        if not isinstance(last, int):
            last = None
        self.volume = restore_volume(
            last,
            self.settings.power_on_volume,
            self.settings.power_on_restore_cap,
            self.settings.max_volume,
        )
        self._target = self.volume

        try:
            await self.dsp.set_master_volume(linear_to_db(self.settings.power_on_volume))
            await self.dsp.set_source(self.source)
        except Exception:
            logger.exception("DSP init failed; amp stays off")

        await self._notify()

    async def power_on(self) -> bool:
        async with self._lock:
            if self.state == "on":
                return True
            restore = restore_volume(
                self.volume,
                self.settings.power_on_volume,
                self.settings.power_on_restore_cap,
                self.settings.max_volume,
            )
            self._target = restore
            try:
                await self._apply_volume_unlocked(restore, persist=True)
            except Exception:
                logger.exception("DSP volume write failed; amp not enabled")
                return False
            settle = self.settings.power_on_settle_ms / 1000.0
            if settle > 0:
                await asyncio.sleep(settle)
            try:
                self.gpio.set_amp(True)
            except Exception:
                logger.exception("GPIO on failed; amp not enabled")
                return False
            self.screen.set_on()
            self.state = "on"
        await self._notify()
        return True

    async def power_off(self) -> None:
        async with self._lock:
            self._target = self.volume
            try:
                await self.dsp.set_master_volume(linear_to_db(0))
            except Exception:
                logger.exception("DSP mute on power-off failed")
            try:
                self.gpio.set_amp(False)
            except Exception:
                logger.exception("GPIO off failed")
            self.screen.set_off()
            self.state = "off"
        await self._notify()

    async def set_volume(self, requested: int) -> int:
        if requested > self.settings.max_volume:
            logger.warning(
                "Volume %s clamped to max_volume %s",
                requested,
                self.settings.max_volume,
            )
        target = clamp_volume(requested, self.settings.max_volume)

        async with self._lock:
            self._target = target
            if self.state != "on":
                self.volume = target
                self.store.save(self.volume, self.source)
                await self._notify()
                return self.volume
            if target <= self.volume:
                await self._apply_volume_unlocked(target, persist=True)
                return self.volume
            if self._ramp_task is None or self._ramp_task.done():
                self._ramp_task = asyncio.create_task(self._ramp_up())
        return target

    async def volume_up(self) -> int:
        async with self._lock:
            nxt = min(max(self._target, self.volume) + 1, self.settings.max_volume)
        return await self.set_volume(nxt)

    async def volume_down(self) -> int:
        async with self._lock:
            nxt = max(self.volume - 1, 0)
        return await self.set_volume(nxt)

    async def set_source(self, source: str) -> None:
        if source not in SOURCE_LIST:
            raise ValueError(f"Unknown source: {source}")
        async with self._lock:
            await self.dsp.set_source(source)
            self.source = source
            self.store.save(self.volume, self.source)
        await self._notify()

    async def reset_dsp(self) -> None:
        async with self._lock:
            self._target = self.volume
            try:
                await self.dsp.set_master_volume(linear_to_db(0))
            except Exception:
                logger.exception("DSP mute before reset failed")
            try:
                self.gpio.set_amp(False)
            except Exception:
                logger.exception("GPIO off before reset failed")
            self.screen.set_off()
            self.state = "off"
            await self.dsp.reset()
        await self._notify()

    async def handle_ir_action(self, action: str) -> None:
        if action == "volume_up":
            await self.volume_up()
        elif action == "volume_down":
            await self.volume_down()
        elif action == "power_on":
            await self.power_on()
        elif action == "power_off":
            await self.power_off()
        elif action.startswith("source:"):
            await self.set_source(action.split(":", 1)[1])
        else:
            logger.warning("Unknown IR action %s", action)

    async def wait_idle(self) -> None:
        task = self._ramp_task
        if task is not None and not task.done():
            await task

    async def _ramp_up(self) -> None:
        interval = self.settings.volume_step_interval_ms / 1000.0
        task = asyncio.current_task()
        try:
            while True:
                async with self._lock:
                    if self.volume >= self._target or self.state != "on":
                        return
                    wait = interval - (time.monotonic() - self._last_increase)
                if wait > 0:
                    await asyncio.sleep(wait)
                async with self._lock:
                    if self.volume >= self._target or self.state != "on":
                        return
                    await self._apply_volume_unlocked(self.volume + 1, persist=True)
        except asyncio.CancelledError:
            raise
        finally:
            if self._ramp_task is task:
                self._ramp_task = None

    async def _apply_volume_unlocked(self, volume: int, persist: bool) -> None:
        volume = clamp_volume(volume, self.settings.max_volume)
        await self.dsp.set_master_volume(linear_to_db(volume))
        self.volume = volume
        self._last_increase = time.monotonic()
        if persist:
            self.store.save(self.volume, self.source)
        self._schedule_notify()

    async def _notify(self) -> None:
        self._schedule_notify()

    def _schedule_notify(self) -> None:
        if not self.webhook_url:
            return
        try:
            asyncio.get_running_loop().create_task(notify_ha(self.webhook_url))
        except RuntimeError:
            pass
