from __future__ import annotations

import argparse
import logging

import uvicorn

from ncore_daemon.app import create_app
from ncore_daemon.config import load_settings


def main() -> None:
    parser = argparse.ArgumentParser(description="Ncore / aurora control daemon")
    parser.add_argument("--config", default=None, help="Path to config.yaml")
    parser.add_argument("--dry-run", action="store_true", help="No GPIO/serial/IR")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    settings = load_settings(args.config)
    if args.dry_run:
        settings.dry_run = True

    app = create_app(settings)
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
