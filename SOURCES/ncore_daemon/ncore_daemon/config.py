from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="NCORE_",
        env_file=".env",
        extra="ignore",
    )

    host: str = "0.0.0.0"
    port: int = 9090
    dry_run: bool = False

    serial_port: str = "/dev/ttyUSB0"
    serial_baud: int = 115200

    gpio_bcm_pin: int = 3

    backlight_path: str = "/sys/class/backlight/rpi_backlight/brightness"
    backlight_max: int = 80

    ir_device_name: str = ""
    ir_device_path: str = "/dev/input/event2"
    ir_repeat_delay_ms: int = 500
    ir_repeat_period_ms: int = 150

    ha_webhook_url: str = ""
    state_path: str = "state.json"

    max_volume: int = 80
    power_on_volume: int = 9
    power_on_restore_cap: int = 20
    volume_step_interval_ms: int = 150
    power_on_settle_ms: int = 50


def load_settings(path: Optional[str] = None) -> Settings:
    data: dict[str, Any] = {}
    config_path = Path(path) if path else Path("config.yaml")
    if config_path.is_file():
        loaded = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        if not isinstance(loaded, dict):
            raise ValueError(f"Config {config_path} must be a mapping")
        data = loaded
    return Settings(**data)
