from ncore_daemon.volume import (
    clamp_volume,
    ha_level_to_volume,
    linear_to_db,
    restore_volume,
    volume_to_ha_level,
)


def test_linear_to_db_matches_java_truncation():
    assert linear_to_db(1) == -80
    assert linear_to_db(9) == int(__import__("math").log10(0.09) * 40.0)
    assert linear_to_db(20) == int(__import__("math").log10(0.20) * 40.0)
    assert linear_to_db(50) == int(__import__("math").log10(0.50) * 40.0)
    assert linear_to_db(80) == int(__import__("math").log10(0.80) * 40.0)


def test_volume_zero_sends_same_floor_as_one():
    assert linear_to_db(0) == linear_to_db(1) == -80


def test_clamp_to_max_volume():
    assert clamp_volume(100, 80) == 80
    assert clamp_volume(-3, 80) == 0
    assert clamp_volume(20, 80) == 20


def test_restore_cap_never_blindly_restores_high_volume():
    assert restore_volume(70, power_on_volume=9, restore_cap=20, max_volume=80) == 20
    assert restore_volume(15, power_on_volume=9, restore_cap=20, max_volume=80) == 15
    assert restore_volume(None, power_on_volume=9, restore_cap=20, max_volume=80) == 9


def test_ha_level_maps_full_scale_to_max_volume_not_100():
    assert ha_level_to_volume(1.0, 80) == 80
    assert ha_level_to_volume(0.0, 80) == 0
    assert ha_level_to_volume(0.5, 80) == 40
    assert abs(volume_to_ha_level(80, 80) - 1.0) < 1e-9
    assert volume_to_ha_level(0, 80) == 0.0
