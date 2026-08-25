import asyncio

import pytest

from ncore_daemon.volume import linear_to_db
from tests.conftest import db_for, make_amp, volumes_sent


@pytest.mark.asyncio
async def test_boot_gpio_off_before_dsp_volume():
    amp = make_amp(store_data={"volume": 70, "source": "analog_1"})
    await amp.start()
    assert amp.events[0] == ("gpio", False)
    assert amp.events[1] == ("dsp_volume", db_for(9))
    assert amp.fake_gpio.amp_on is False
    assert amp.state == "off"
    assert amp.volume == 20
    assert amp.source == "analog_1"


@pytest.mark.asyncio
async def test_power_on_writes_capped_volume_before_gpio_on():
    amp = make_amp(store_data={"volume": 70, "source": "usb"})
    await amp.start()
    ok = await amp.power_on()
    assert ok is True
    assert ("gpio", True) in amp.events
    gpio_on_at = amp.events.index(("gpio", True))
    restore_at = max(
        i for i, ev in enumerate(amp.events[:gpio_on_at]) if ev[0] == "dsp_volume"
    )
    assert amp.events[restore_at] == ("dsp_volume", db_for(20))
    assert restore_at < gpio_on_at
    assert amp.volume == 20
    assert amp.fake_gpio.amp_on is True


@pytest.mark.asyncio
async def test_power_on_aborts_if_dsp_volume_write_fails():
    amp = make_amp()
    await amp.start()
    amp.fake_dsp.fail_volume = True
    ok = await amp.power_on()
    assert ok is False
    assert amp.fake_gpio.amp_on is False
    assert amp.state == "off"
    assert amp.serial_ok is False
    assert ("gpio", True) not in amp.events


@pytest.mark.asyncio
async def test_power_off_mutes_dsp_before_gpio_off():
    amp = make_amp()
    await amp.start()
    await amp.power_on()
    await amp.set_volume(18)
    await amp.wait_idle()
    await amp.power_off()
    gpio_off_indices = [i for i, ev in enumerate(amp.events) if ev == ("gpio", False)]
    last_off = gpio_off_indices[-1]
    assert amp.events[last_off - 1] == ("dsp_volume", linear_to_db(0))
    assert amp.state == "off"
    assert amp.volume == 18


@pytest.mark.asyncio
async def test_volume_zero_is_sent_to_dsp():
    amp = make_amp()
    await amp.start()
    await amp.power_on()
    await amp.set_volume(10)
    await amp.wait_idle()
    await amp.set_volume(0)
    await amp.wait_idle()
    assert volumes_sent(amp.events)[-1] == linear_to_db(0)
    assert amp.volume == 0


@pytest.mark.asyncio
async def test_volume_above_max_is_clamped():
    amp = make_amp()
    await amp.start()
    await amp.power_on()
    await amp.set_volume(999)
    await amp.wait_idle()
    assert amp.volume == 80
    assert volumes_sent(amp.events)[-1] == db_for(80)


@pytest.mark.asyncio
async def test_ramp_up_sends_each_step_not_a_jump():
    amp = make_amp(settings={"volume_step_interval_ms": 0})
    await amp.start()
    await amp.power_on()
    await amp.set_volume(12)
    await amp.wait_idle()
    before = len(volumes_sent(amp.events))
    await amp.set_volume(16)
    await amp.wait_idle()
    sent = volumes_sent(amp.events)[before:]
    assert sent == [db_for(n) for n in (13, 14, 15, 16)]


@pytest.mark.asyncio
async def test_volume_down_is_instant():
    amp = make_amp(settings={"volume_step_interval_ms": 0})
    await amp.start()
    await amp.power_on()
    await amp.set_volume(16)
    await amp.wait_idle()
    before = len(volumes_sent(amp.events))
    await amp.set_volume(5)
    await amp.wait_idle()
    sent = volumes_sent(amp.events)[before:]
    assert sent == [db_for(5)]
    assert amp.volume == 5


@pytest.mark.asyncio
async def test_ir_volume_up_respects_step_interval():
    amp = make_amp(settings={"volume_step_interval_ms": 200})
    await amp.start()
    await amp.power_on()
    await amp.set_volume(10)
    await amp.wait_idle()
    for _ in range(10):
        await amp.volume_up()
    assert amp.volume == 10
    await asyncio.sleep(0.05)
    assert amp.volume == 10
    await asyncio.sleep(0.2)
    await amp.wait_idle()
    assert amp.volume >= 11
    assert amp.volume <= 20


@pytest.mark.asyncio
async def test_lower_setpoint_stops_ramp():
    amp = make_amp(settings={"volume_step_interval_ms": 200})
    await amp.start()
    await amp.power_on()
    await amp.set_volume(10)
    await amp.wait_idle()
    await amp.set_volume(40)
    await amp.set_volume(6)
    await amp.wait_idle()
    assert amp.volume == 6
    assert volumes_sent(amp.events)[-1] == db_for(6)


@pytest.mark.asyncio
async def test_ir_action_changes_source():
    amp = make_amp()
    await amp.start()
    await amp.handle_ir_action("source:optical_1")
    assert amp.source == "optical_1"
    assert ("source", "optical_1") in amp.events


@pytest.mark.asyncio
async def test_reset_mutes_and_turns_amp_off():
    amp = make_amp()
    await amp.start()
    await amp.power_on()
    await amp.reset_dsp()
    assert amp.state == "off"
    assert amp.fake_gpio.amp_on is False
    assert amp.events[-1] == ("reset", True)
    assert ("dsp_volume", linear_to_db(0)) in amp.events
