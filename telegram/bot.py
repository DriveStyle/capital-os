import asyncio
import os
import logging
from dotenv import load_dotenv
import httpx

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("capital_os_bot")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://capital-os-demo.vercel.app")


async def handle_bot_command(command: str) -> dict:
    """Process incoming bot command and interact with Capital OS backend API."""
    async with httpx.AsyncClient() as client:
        try:
            if command.startswith("/start"):
                text = (
                    "🚀 **Capital OS — Личная финансовая операционная система!**\n\n"
                    "Доступные команды:\n"
                    "• /portfolio — Баланс и распределение активов\n"
                    "• /rebalance — План ребалансировки (Buy-Only)\n"
                    "• /ai — Советы AI-консультанта\n"
                    "• /status — Проверка API сервера"
                )
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "📊 Открыть Capital OS App", "web_app": {"url": MINI_APP_URL}}],
                        [{"text": "⚖️ Ребалансировка", "callback_data": "/rebalance"}, {"text": "🤖 AI Совет", "callback_data": "/ai"}]
                    ]
                }
                return {"text": text, "reply_markup": keyboard}

            elif command.startswith("/portfolio"):
                text = (
                    "📊 **Capital OS Портфель:**\n"
                    "Общая стоимость: **$50,000.00 USD** (+14.2% за всё время)\n\n"
                    "Активы:\n"
                    "• VWRA (Global ETF): $27,500 (55%)\n"
                    "• S&P 500 (US ETF): $12,500 (25%)\n"
                    "• BTC (Crypto): $5,000 (10%)\n"
                    "• CASH (Резерв): $5,000 (10%)"
                )
                return {"text": text}

            elif command.startswith("/rebalance"):
                try:
                    resp = await client.post(f"{API_BASE_URL}/portfolios/rebalance", json={
                        "monthly_budget": 1000,
                        "risk_profile": "moderate"
                    }, timeout=5.0)
                    if resp.status_code == 200:
                        data = resp.json()
                        allocs = "\n".join([f"• Покупка {item['asset_type']}: **${item['recommended_buy_amount']}** ({item['percentage_of_budget']}%)" for item in data['buy_allocations']])
                        text = f"⚖️ **План ребалансировки ($1,000/мес):**\n\n{allocs}\n\n💡 *Налоговый бонус:* {data['tax_efficient_note']}"
                        return {"text": text}
                except Exception:
                    pass
                return {"text": "⚖️ **План ребалансировки ($1,000/мес):**\n• Покупка VWRA (ETF): $700\n• Покупка Резерва (Yield): $300\n\n*(Без продажи активов и без налогов)*"}

            elif command.startswith("/ai"):
                try:
                    resp = await client.post(f"{API_BASE_URL}/ai/recommend", json={
                        "monthly_investment_budget": 1000,
                        "risk_tolerance": "moderate",
                        "country_code": "UA"
                    }, timeout=5.0)
                    if resp.status_code == 200:
                        data = resp.json()
                        text = f"🤖 **AI Консультант:**\n\n{data['summary']}\n\n📌 *Налоговый контекст:* {data['country_notes']}"
                        return {"text": text}
                except Exception:
                    pass
                return {"text": "🤖 **AI Рекомендация:** Соблюдайте ежемесячную стратегию усреднения (DCA) 70% Индексные ETF / 30% Резерв."}

            elif command.startswith("/status"):
                try:
                    resp = await client.get(f"{API_BASE_URL}/health", timeout=5.0)
                    return {"text": f"🟢 API сервер Capital OS активен: {resp.json()}"}
                except Exception:
                    return {"text": "🔴 Backend локальный сервер недоступен."}
            else:
                return {"text": "Неизвестная команда. Нажмите /start для вызова меню."}
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return {"text": "⚠️ Ошибка обработки команды."}


async def send_telegram_message(client: httpx.AsyncClient, chat_id: int, payload: dict) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    body = {
        "chat_id": chat_id,
        "text": payload.get("text", ""),
        "parse_mode": "Markdown",
    }
    if "reply_markup" in payload:
        body["reply_markup"] = payload["reply_markup"]

    try:
        await client.post(url, json=body, timeout=10.0)
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")


async def start_bot_polling() -> None:
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "mock_bot_token":
        logger.warning("TELEGRAM_BOT_TOKEN не задан в .env! Задайте токен для live-бота.")
        return

    logger.info("Запуск Telegram Bot Long Polling...")
    offset = 0
    async with httpx.AsyncClient() as client:
        # Check bot identity
        try:
            me_resp = await client.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe")
            if me_resp.status_code == 200 and me_resp.json().get("ok"):
                bot_info = me_resp.json()["result"]
                logger.info(f"Бот успешно подключен: @{bot_info.get('username')} ({bot_info.get('first_name')})")
            else:
                logger.error(f"Ошибка проверки токена бота: {me_resp.text}")
                return
        except Exception as e:
            logger.error(f"Не удалось подключиться к Telegram API: {e}")
            return

        # Continuous Long-Polling Loop
        while True:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
                resp = await client.get(url, params={"offset": offset, "timeout": 20}, timeout=30.0)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("ok"):
                        for update in data.get("result", []):
                            offset = update["update_id"] + 1

                            # Process text message or callback query
                            if "message" in update and "text" in update["message"]:
                                msg = update["message"]
                                chat_id = msg["chat"]["id"]
                                text = msg["text"]
                                logger.info(f"Сообщение от {chat_id}: {text}")
                                reply_data = await handle_bot_command(text)
                                await send_telegram_message(client, chat_id, reply_data)

                            elif "callback_query" in update:
                                cb = update["callback_query"]
                                chat_id = cb["message"]["chat"]["id"]
                                data_text = cb.get("data", "")
                                reply_data = await handle_bot_command(data_text)
                                await send_telegram_message(client, chat_id, reply_data)

            except asyncio.CancelledError:
                logger.info("Остановка бота.")
                break
            except Exception as e:
                logger.error(f"Ошибка в цикле polling: {e}")
                await asyncio.sleep(3)


if __name__ == "__main__":
    try:
        asyncio.run(start_bot_polling())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем.")
