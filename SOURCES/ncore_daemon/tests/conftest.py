from __future__ import annotations

from ncore_daemon.amp import Amp
from ncore_daemon.config import Settings
from ncore_daemon.screen import Screen
from ncore_daemon.volume import linear_to_db


class MemoryStore:
    def __init__(self, data=None):
        self.data = dict(data or {})

    def load(self):
        return dict(self.data)

    def save(self, volume, source):
        self.data = {"volume": volume, "source": source}


class FakeDsp:
    def __init__(self, events):
        self.events = events
        self.serial_ok = True
        self.fail_volume = False
        self.sent = []

    async def set_master_volume(self, db):
        self.events.append(("dsp_volume", db))
        if self.fail_volume:
            self.serial_ok = False
            raise RuntimeError("serial fail")
        self.serial_ok = True

    async def set_source(self, source):
        self.events.append(("source", source))
        self.serial_ok = True

    async def reset(self):
        self.events.append(("reset", True))
        self.serial_ok = True

    def close(self):
        pass


class FakeGpio:
    def __init__(self, events):
        self.events = events
        self.gpio_ok = True
        self.amp_on = False

    def set_amp(self, on):
        self.events.append(("gpio", on))
        self.amp_on = on

    def close(self):
        pass


def make_amp(**overrides) -> Amp:
    events = overrides.pop("events", None)
    if events is None:
        events = []
    settings_kwargs = {
        "dry_run": True,
        "max_volume": 80,
        "power_on_volume": 9,
        "power_on_restore_cap": 20,
        "volume_step_interval_ms": 0,
        "power_on_settle_ms": 0,
        "state_path": "state.json",
    }
    settings_kwargs.update(overrides.pop("settings", {}))
    store_data = overrides.pop("store_data", None)
    settings = Settings(**settings_kwargs)
    dsp = FakeDsp(events)
    gpio = FakeGpio(events)
    screen = Screen("/tmp/unused", dry_run=True)
    store = MemoryStore(store_data)
    amp = Amp(settings, dsp=dsp, gpio=gpio, screen=screen, store=store)
    amp.events = events
    amp.fake_dsp = dsp
    amp.fake_gpio = gpio
    amp.store = store
    return amp


def volumes_sent(events):
    return [item[1] for item in events if item[0] == "dsp_volume"]


def db_for(volume: int) -> int:
    return linear_to_db(volume)
