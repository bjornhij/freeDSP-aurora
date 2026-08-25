from __future__ import annotations

import math
from typing import Optional


def linear_to_db(volume: int) -> int:
    """Match Java: (int)(Math.log10(volume / 100.0) * 40.0).

    Volume 0 uses the same floor as volume 1 (-80 dB) so mute is actually sent.
    """
    linear = 1 if volume <= 0 else volume
    return int(math.log10(linear / 100.0) * 40.0)


def clamp_volume(volume: int, max_volume: int) -> int:
    return max(0, min(int(volume), int(max_volume)))


def restore_volume(
    last: Optional[int],
    power_on_volume: int,
    restore_cap: int,
    max_volume: int,
) -> int:
    base = power_on_volume if last is None else last
    return clamp_volume(min(base, restore_cap), max_volume)


def ha_level_to_volume(level: float, max_volume: int) -> int:
    return clamp_volume(round(float(level) * max_volume), max_volume)


def volume_to_ha_level(volume: int, max_volume: int) -> float:
    if max_volume <= 0:
        return 0.0
    return clamp_volume(volume, max_volume) / float(max_volume)
