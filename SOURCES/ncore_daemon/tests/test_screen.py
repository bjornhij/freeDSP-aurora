from ncore_daemon.screen import Screen


def test_dry_run_set_on_off_does_not_touch_missing_path(tmp_path):
    path = tmp_path / "missing" / "brightness"
    screen = Screen(str(path), dry_run=True, hdmi_power=True)
    screen.set_on()
    assert screen.brightness == 80
    screen.set_off()
    assert screen.brightness == 0


def test_backlight_write_when_file_exists(tmp_path):
    path = tmp_path / "brightness"
    path.write_text("0", encoding="ascii")
    screen = Screen(str(path), max_brightness=80, dry_run=False, hdmi_power=False)
    screen.set_on()
    assert path.read_text(encoding="ascii") == "80"
    screen.set_off()
    assert path.read_text(encoding="ascii") == "0"
