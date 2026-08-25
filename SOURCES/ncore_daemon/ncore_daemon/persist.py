from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class StateStore:
    def __init__(self, path: str):
        self.path = Path(path)

    def load(self) -> dict[str, Any]:
        if not self.path.is_file():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            logger.exception("Failed to read %s", self.path)
            return {}
        return data if isinstance(data, dict) else {}

    def save(self, volume: Optional[int], source: str) -> None:
        payload = {"volume": volume, "source": source}
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
        except OSError:
            logger.exception("Failed to write %s", self.path)
