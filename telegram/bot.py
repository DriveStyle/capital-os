import asyncio
import os
import logging
from dotenv import load_dotenv
import httpx

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("capital_os_bot")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "mock_bot_token")


async def check_bot_status() -> dict:
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "mock_bot_token":
        logger.warning("No TELEGRAM_BOT_TOKEN set in .env")
        return {"ok": False, "description": "No bot token configured"}

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=10.0)
            data = resp.json()
            if data.get("ok"):
                bot_info = data.get("result", {})
                logger.info(f"Bot connected successfully: @{bot_info.get('username')} ({bot_info.get('first_name')})")
                return data
            else:
                logger.error(f"Telegram API Error: {data.get('description')}")
                return data
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return {"ok": False, "error": str(e)}


async def main() -> None:
    logger.info("Initializing Capital OS Telegram Bot handler...")
    res = await check_bot_status()
    if res.get("ok"):
        bot = res["result"]
        print(f"\n[SUCCESS] Telegram Bot Online!")
        print(f"Bot Name: {bot.get('first_name')}")
        print(f"Username: @{bot.get('username')}")
        print(f"Bot ID: {bot.get('id')}\n")
    else:
        print(f"\n[ERROR] Failed to connect: {res}\n")


if __name__ == "__main__":
    asyncio.run(main())
