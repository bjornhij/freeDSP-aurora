from ncore_daemon.sources import SOURCE_LIST, format_message, source_commands


def test_source_list_order():
    assert "usb" in SOURCE_LIST
    assert "optical_4" in SOURCE_LIST
    assert "analog_4" in SOURCE_LIST


def test_usb_and_analog_commands_match_java():
    assert list(source_commands("usb")) == [
        ("/input", "idx|0|sel|0x00010000"),
        ("/input", "idx|1|sel|0x00010001"),
    ]
    assert list(source_commands("analog_1")) == [
        ("/input", "idx|0|sel|0x00000000"),
        ("/input", "idx|1|sel|0x00000001"),
    ]
    assert list(source_commands("analog_4")) == [
        ("/input", "idx|0|sel|0x00000006"),
        ("/input", "idx|1|sel|0x00000007"),
    ]


def test_optical_sends_addoncfg_then_adat_input():
    cmds = list(source_commands("optical_2"))
    assert cmds[0] == ("/addoncfg", "0x82|0x01|0x01")
    assert cmds[1:] == [
        ("/input", "idx|0|sel|0x00040000"),
        ("/input", "idx|1|sel|0x00040001"),
    ]
    assert list(source_commands("optical_4"))[0] == ("/addoncfg", "0x82|0x01|0x03")


def test_serial_message_format():
    assert format_message("/mvol", "-42") == "/mvol|-42\n"


def test_unknown_source_raises():
    try:
        source_commands("hdmi")
    except ValueError:
        return
    raise AssertionError("expected ValueError")
