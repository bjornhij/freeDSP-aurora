from ncore_daemon.ir import (
    KEY_FN_ESC,
    KEY_FN_F1,
    KEY_FN_F2,
    KEY_FN_F3,
    KEY_FN_F10,
    action_for_event,
    action_for_key_name,
)


def test_keymap_follows_put_urls_not_print_labels():
    assert action_for_key_name("KEY_FN_F1") == "volume_up"
    assert action_for_key_name("KEY_FN_F2") == "volume_down"
    assert action_for_key_name("KEY_FN_F4") == "power_on"
    assert action_for_key_name("KEY_FN_F5") == "power_off"
    assert action_for_key_name("KEY_FN_F6") == "source:usb"
    assert action_for_key_name("KEY_FN_F7") == "source:optical_1"
    assert action_for_key_name("KEY_FN_F8") == "source:optical_2"
    assert action_for_key_name("KEY_FN_F9") == "source:optical_3"
    assert action_for_key_name("KEY_FN_F10") == "source:analog_1"
    assert action_for_key_name("KEY_FN_F11") == "source:analog_2"
    assert action_for_key_name("KEY_FN_F12") == "source:analog_3"
    assert action_for_key_name("KEY_FN_ESC") == "source:analog_4"
    assert action_for_key_name("KEY_FN_F3") is None


def test_only_hold_value_two_is_handled():
    assert action_for_event(KEY_FN_F1, value=2) == "volume_up"
    assert action_for_event(KEY_FN_F1, value=1) is None
    assert action_for_event(KEY_FN_F1, value=0) is None
    assert action_for_event(KEY_FN_F10, value=2) == "source:analog_1"
    assert action_for_event(KEY_FN_ESC, value=2) == "source:analog_4"
    assert action_for_event(KEY_FN_F3, value=2) is None
    assert action_for_event(KEY_FN_F2, value=2, event_type=0) is None
