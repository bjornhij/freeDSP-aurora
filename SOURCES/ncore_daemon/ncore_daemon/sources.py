from __future__ import annotations

from typing import Sequence

SOURCE_LIST: tuple[str, ...] = (
    "usb",
    "optical_1",
    "optical_2",
    "optical_3",
    "optical_4",
    "analog_1",
    "analog_2",
    "analog_3",
    "analog_4",
)

_OPTICAL_INPUT = (
    ("/input", "idx|0|sel|0x00040000"),
    ("/input", "idx|1|sel|0x00040001"),
)

# (handler, data) pairs matching Dsp.java sendData()
_SOURCE_COMMANDS: dict[str, tuple[tuple[str, str], ...]] = {
    "usb": (
        ("/input", "idx|0|sel|0x00010000"),
        ("/input", "idx|1|sel|0x00010001"),
    ),
    "analog_1": (
        ("/input", "idx|0|sel|0x00000000"),
        ("/input", "idx|1|sel|0x00000001"),
    ),
    "analog_2": (
        ("/input", "idx|0|sel|0x00000002"),
        ("/input", "idx|1|sel|0x00000003"),
    ),
    "analog_3": (
        ("/input", "idx|0|sel|0x00000004"),
        ("/input", "idx|1|sel|0x00000005"),
    ),
    "analog_4": (
        ("/input", "idx|0|sel|0x00000006"),
        ("/input", "idx|1|sel|0x00000007"),
    ),
    "optical_1": (("/addoncfg", "0x82|0x01|0x00"),) + _OPTICAL_INPUT,
    "optical_2": (("/addoncfg", "0x82|0x01|0x01"),) + _OPTICAL_INPUT,
    "optical_3": (("/addoncfg", "0x82|0x01|0x02"),) + _OPTICAL_INPUT,
    "optical_4": (("/addoncfg", "0x82|0x01|0x03"),) + _OPTICAL_INPUT,
}


def format_message(handler: str, data: str) -> str:
    return f"{handler}|{data}\n"


def source_commands(source: str) -> Sequence[tuple[str, str]]:
    try:
        return _SOURCE_COMMANDS[source]
    except KeyError as exc:
        raise ValueError(f"Unknown source: {source}") from exc
