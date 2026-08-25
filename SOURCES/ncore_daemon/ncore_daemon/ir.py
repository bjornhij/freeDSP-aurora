from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# linux/input-event-codes.h KEY_FN_*
KEY_FN_ESC = 465
KEY_FN_F1 = 466
KEY_FN_F2 = 467
KEY_FN_F3 = 468
KEY_FN_F4 = 469
KEY_FN_F5 = 470
KEY_FN_F6 = 471
KEY_FN_F7 = 472
KEY_FN_F8 = 473
KEY_FN_F9 = 474
KEY_FN_F10 = 475
KEY_FN_F11 = 476
KEY_FN_F12 = 477

EV_KEY = 1
KEY_HOLD = 2

# Actions follow the live ir_bridge.py PUT URLs, not the print/comment labels.
IR_KEY_ACTIONS: dict[str, str] = {
    "KEY_FN_F1": "volume_up",
    "KEY_FN_F2": "volume_down",
    "KEY_FN_F4": "power_on",
    "KEY_FN_F5": "power_off",
    "KEY_FN_F6": "source:usb",
    "KEY_FN_F7": "source:optical_1",
    "KEY_FN_F8": "source:optical_2",
    "KEY_FN_F9": "source:optical_3",
    "KEY_FN_F10": "source:analog_1",
    "KEY_FN_F11": "source:analog_2",
    "KEY_FN_F12": "source:analog_3",
    "KEY_FN_ESC": "source:analog_4",
}

IR_CODE_ACTIONS: dict[int, str] = {
    KEY_FN_F1: "volume_up",
    KEY_FN_F2: "volume_down",
    KEY_FN_F4: "power_on",
    KEY_FN_F5: "power_off",
    KEY_FN_F6: "source:usb",
    KEY_FN_F7: "source:optical_1",
    KEY_FN_F8: "source:optical_2",
    KEY_FN_F9: "source:optical_3",
    KEY_FN_F10: "source:analog_1",
    KEY_FN_F11: "source:analog_2",
    KEY_FN_F12: "source:analog_3",
    KEY_FN_ESC: "source:analog_4",
}


def action_for_event(code: int, value: int, event_type: int = EV_KEY) -> Optional[str]:
    if event_type != EV_KEY or value != KEY_HOLD:
        return None
    return IR_CODE_ACTIONS.get(code)


def action_for_key_name(name: str) -> Optional[str]:
    return IR_KEY_ACTIONS.get(name)


def find_ir_device(name_substr: str, fallback_path: str):
    try:
        from evdev import InputDevice, list_devices
    except ImportError:
        logger.warning("evdev is not installed; IR disabled")
        return None

    if name_substr:
        needle = name_substr.lower()
        for path in list_devices():
            try:
                device = InputDevice(path)
            except OSError:
                continue
            if needle in (device.name or "").lower():
                logger.info("IR device match %s (%s)", device.path, device.name)
                return device
        logger.warning("No IR device name matching %r, trying %s", name_substr, fallback_path)

    try:
        return InputDevice(fallback_path)
    except OSError:
        logger.warning("IR device %s not available", fallback_path)
        return None


def _set_repeat(device, delay_ms: int, period_ms: int) -> None:
    try:
        device.repeat = (delay_ms, period_ms)
        return
    except Exception:
        pass
    try:
        from evdev.device import KbdInfo

        device.repeat = KbdInfo(repeat=period_ms, delay=delay_ms)
        return
    except Exception:
        logger.warning("Could not set IR repeat timing", exc_info=True)


async def run_ir_loop(amp, settings) -> None:
    if settings.dry_run:
        amp.ir_ok = False
        logger.info("IR disabled (dry-run)")
        return

    device = find_ir_device(settings.ir_device_name, settings.ir_device_path)
    if device is None:
        amp.ir_ok = False
        return

    try:
        device.grab()
        _set_repeat(device, settings.ir_repeat_delay_ms, settings.ir_repeat_period_ms)
        amp.ir_ok = True
        logger.info("IR listening on %s (%s)", getattr(device, "path", "?"), device.name)
        async for event in device.async_read_loop():
            action = action_for_event(event.code, event.value, event.type)
            if not action:
                continue
            logger.info("IR %s", action)
            try:
                await amp.handle_ir_action(action)
            except Exception:
                logger.exception("IR action %s failed", action)
    except Exception:
        amp.ir_ok = False
        logger.exception("IR loop stopped")
    finally:
        amp.ir_ok = False
        try:
            device.ungrab()
        except Exception:
            pass
        try:
            device.close()
        except Exception:
            pass
