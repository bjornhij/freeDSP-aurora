from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI

from ncore_daemon.amp import Amp
from ncore_daemon.api import install_routes
from ncore_daemon.config import Settings, load_settings
from ncore_daemon.dsp import Dsp
from ncore_daemon.gpio import AmpGpio
from ncore_daemon.ir import run_ir_loop
from ncore_daemon.persist import StateStore
from ncore_daemon.screen import Screen

logger = logging.getLogger(__name__)


def build_amp(settings: Settings) -> Amp:
    dsp = Dsp(settings.serial_port, settings.serial_baud, dry_run=settings.dry_run)
    dsp.connect()
    gpio = AmpGpio(settings.gpio_bcm_pin, dry_run=settings.dry_run)
    screen = Screen(
        settings.backlight_path,
        max_brightness=settings.backlight_max,
        dry_run=settings.dry_run,
        hdmi_power=settings.display_hdmi_power,
    )
    store = StateStore(settings.state_path)
    return Amp(
        settings,
        dsp=dsp,
        gpio=gpio,
        screen=screen,
        store=store,
        webhook_url=settings.ha_webhook_url,
    )


def create_app(
    settings: Optional[Settings] = None,
    amp: Optional[Amp] = None,
    enable_ir: bool = True,
) -> FastAPI:
    settings = settings or load_settings()
    amp = amp or build_amp(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await app.state.amp.start()
        ir_task = None
        if enable_ir:
            ir_task = asyncio.create_task(run_ir_loop(app.state.amp, app.state.settings))
        try:
            yield
        finally:
            if ir_task is not None:
                ir_task.cancel()
                try:
                    await ir_task
                except asyncio.CancelledError:
                    pass
            app.state.amp.dsp.close()
            app.state.amp.gpio.close()

    app = FastAPI(title="ncore-daemon", lifespan=lifespan)
    app.state.settings = settings
    app.state.amp = amp
    install_routes(app)
    return app
