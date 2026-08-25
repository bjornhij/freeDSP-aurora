from __future__ import annotations

import logging
import urllib.error
import urllib.request
from typing import Optional

logger = logging.getLogger(__name__)


async def notify_ha(url: Optional[str]) -> None:
    if not url:
        return
    try:
        import asyncio

        await asyncio.to_thread(_post, url)
    except Exception:
        logger.warning("Home Assistant webhook failed", exc_info=True)


def _post(url: str) -> None:
    request = urllib.request.Request(url, data=b"", method="POST")
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            response.read()
    except (urllib.error.URLError, TimeoutError, OSError):
        logger.warning("Home Assistant webhook POST to %s failed", url, exc_info=True)
