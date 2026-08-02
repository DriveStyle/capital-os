import asyncio
import os
import logging
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("capital_os_bot")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "mock_bot_token")


async def main() -> None:
    logger.info("Initializing Capital OS Telegram Bot & Mini App listener...")
    if TELEGRAM_BOT_TOKEN == "mock_bot_token":
        logger.info("No live TELEGRAM_BOT_TOKEN provided. Running in dry-run simulation mode.")
        print("[BOT] Capital OS Telegram Bot Ready.")
        print("[BOT] Listening for commands: /start, /portfolio, /ai_advice, /goals")
        return

    logger.info("Connecting to Telegram API...")


if __name__ == "__main__":
    asyncio.run(main())
