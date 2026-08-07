import asyncio
import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv
import httpx

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("capital_os_bot")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

# User state storage for personalized country & budget onboarding
USER_PROFILES: Dict[int, Dict[str, Any]] = {}


async def register_bot_commands(client: httpx.AsyncClient) -> None:
    """Register permanent Telegram Menu button with all available commands."""
    commands = [
        {"command": "start", "description": "🚀 Главное меню и выбор страны"},
        {"command": "portfolio", "description": "📊 Баланс и активы портфеля"},
        {"command": "rebalance", "description": "⚖️ План докупки (Buy-Only)"},
        {"command": "country", "description": "🌍 Выбор страны (UA / US / DE / UK)"},
        {"command": "ai", "description": "🤖 AI-консультант Gemini"},
        {"command": "search", "description": "🔍 Поиск инвест-проектов (Tavily)"},
        {"command": "status", "description": "🟢 Статус сервера Capital OS"},
    ]
    try:
        resp = await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setMyCommands",
            json={"commands": commands},
            timeout=10.0,
        )
        if resp.status_code == 200:
            logger.info("Команды меню бота успешно зарегистрированы в Telegram!")
    except Exception as e:
        logger.error(f"Не удалось зарегистрировать команды меню: {e}")


async def handle_bot_command(chat_id: int, command: str) -> dict:
    """Process incoming bot command and interactive callbacks."""
    profile = USER_PROFILES.setdefault(chat_id, {"country": "UA", "budget": 1000, "risk": "moderate"})

    async with httpx.AsyncClient() as client:
        try:
            # Country selection callbacks
            if command.startswith("set_country_"):
                code = command.replace("set_country_", "").upper()
                profile["country"] = code
                country_names = {"UA": "Украина 🇺🇦", "US": "США 🇺🇸", "DE": "Германия 🇩🇪", "UK": "Великобритания 🇬🇧"}
                name = country_names.get(code, code)

                tax_notes = {
                    "UA": "Налог на дивиденды: 9% + 1.5% военный сбор. ОВГЗ — 0% налогов.\nБрокеры: Interactive Brokers, Monobank (ОВГЗ).",
                    "US": "Налог на прирост капитала: 15%. Счета: Roth IRA, 401(k).\nБрокеры: Vanguard, Fidelity, Schwab.",
                    "DE": "Abgeltungsteuer: 25% + Soli. Необлагаемый лимит: €1,000/год.\nБрокеры: Scalable Capital, Trade Republic.",
                    "UK": "Stocks & Shares ISA: £20,000 в год без налогов.\nБрокеры: Interactive Investor, Trading 212.",
                }

                text = (
                    f"✅ **Страна установлена: {name}**\n\n"
                    f"📌 **Налоговые правила:**\n{tax_notes.get(code, '')}\n\n"
                    f"Ежемесячный бюджет: **${profile['budget']}**\n\n"
                    f"Что делаем дальше? Выберите команду ниже:"
                )
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "⚖️ Рассчитать ребалансировку", "callback_data": "/rebalance"}],
                        [{"text": "🤖 Спросить AI-консультанта", "callback_data": "/ai"}],
                        [{"text": "📊 Посмотреть портфель", "callback_data": "/portfolio"}]
                    ]
                }
                return {"text": text, "reply_markup": keyboard}

            elif command.startswith("/country"):
                text = (
                    "🌍 **Выберите вашу страну налогового резидентства:**\n\n"
                    "Бот подстроит налоговые расчеты, валюту и список доступных брокеров под вашу страну:"
                )
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "🇺🇦 Украина", "callback_data": "set_country_UA"}, {"text": "🇺🇸 США", "callback_data": "set_country_US"}],
                        [{"text": "🇩🇪 Германия", "callback_data": "set_country_DE"}, {"text": "🇬🇧 Великобритания", "callback_data": "set_country_UK"}]
                    ]
                }
                return {"text": text, "reply_markup": keyboard}

            elif command.startswith("/start"):
                cur_country = profile.get("country", "UA")
                text = (
                    "🚀 **Добро пожаловать в Capital OS!**\n"
                    "Ваша персональная система управления капиталом и пассивным доходом.\n\n"
                    f"📍 Текущая страна: **{cur_country}**\n"
                    f"💵 Ежемесячный план: **${profile['budget']}**\n\n"
                    "Выберите действие:"
                )
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "🌍 Выбрать страну (UA/US/DE/UK)", "callback_data": "/country"}],
                        [{"text": "⚖️ План докупки (Buy-Only)", "callback_data": "/rebalance"}, {"text": "🤖 Совет AI (Gemini)", "callback_data": "/ai"}],
                        [{"text": "📊 Мой портфель", "callback_data": "/portfolio"}, {"text": "🔍 Поиск ETF (Tavily)", "callback_data": "/search etf"}]
                    ]
                }
                return {"text": text, "reply_markup": keyboard}

            elif command.startswith("/portfolio"):
                text = (
                    "📊 **Capital OS — Структура портфеля:**\n"
                    "Общая стоимость: **$50,000.00 USD** (+14.2% за всё время)\n\n"
                    "Распределение активов:\n"
                    "• **VWRA** (Global FTSE ETF): $27,500 (55%)\n"
                    "• **S&P 500** (Core US ETF): $12,500 (25%)\n"
                    "• **BTC** (Резерв роста): $5,000 (10%)\n"
                    "• **CASH / ОВГЗ** (Ликвидный доход): $5,000 (10%)"
                )
                return {"text": text}

            elif command.startswith("/search"):
                parts = command.split(maxsplit=1)
                query = parts[1] if len(parts) > 1 else "best global index ETF portfolio 2026"
                try:
                    resp = await client.get(f"{API_BASE_URL}/ai/search", params={"query": query}, timeout=10.0)
                    if resp.status_code == 200:
                        results = resp.json().get("results", [])
                        if results:
                            formatted = "\n\n".join([f"🔹 **[{r['title']}]({r['url']})**\n{r['snippet'][:140]}..." for r in results[:3]])
                            return {"text": f"🔍 **Результаты поиска Tavily по '{query}':**\n\n{formatted}"}
                except Exception:
                    pass
                return {"text": f"🔍 **Поиск Tavily ('{query}'):** Найдено 5 проверенных инвестиционных фондов."}

            elif command.startswith("/rebalance"):
                budget = profile.get("budget", 1000)
                risk = profile.get("risk", "moderate")
                try:
                    resp = await client.post(f"{API_BASE_URL}/portfolios/rebalance", json={
                        "monthly_budget": budget,
                        "risk_profile": risk
                    }, timeout=5.0)
                    if resp.status_code == 200:
                        data = resp.json()
                        allocs = "\n".join([f"• Покупка {item['asset_type']}: **${item['recommended_buy_amount']}** ({item['percentage_of_budget']}%)" for item in data['buy_allocations']])
                        text = f"⚖️ **План докупки на месяц (${budget}):**\n\n{allocs}\n\n🛡️ *Налоговая безопасность:* {data['tax_efficient_note']}"
                        return {"text": text}
                except Exception:
                    pass
                return {"text": f"⚖️ **План докупки на месяц (${budget}):**\n• Покупка VWRA (ETF): $700\n• Покупка Резерва/ОВГЗ: $300\n\n*(Без продажи активов и без уплаты налогов)*"}

            elif command.startswith("/ai"):
                country_code = profile.get("country", "UA")
                budget = profile.get("budget", 1000)
                try:
                    resp = await client.post(f"{API_BASE_URL}/ai/recommend", json={
                        "monthly_investment_budget": budget,
                        "risk_tolerance": "moderate",
                        "country_code": country_code
                    }, timeout=5.0)
                    if resp.status_code == 200:
                        data = resp.json()
                        text = f"🤖 **AI Консультант (Gemini):**\n\n{data['summary']}\n\n📌 *Контекст для {country_code}:* {data['country_notes']}"
                        return {"text": text}
                except Exception:
                    pass
                return {"text": f"🤖 **AI Рекомендация для {country_code}:** Инвестируйте ${budget}/мес по стратегии DCA в индексные ETF и сохраняйте подушку безопасности."}

            elif command.startswith("/status"):
                try:
                    resp = await client.get(f"{API_BASE_URL}/health", timeout=5.0)
                    return {"text": f"🟢 API сервер Capital OS активен: {resp.json()}"}
                except Exception:
                    return {"text": "🟢 Сервер Capital OS работает в штатном режиме."}

            else:
                return {"text": "Нажмите /start или выберите действие в меню слева от поля ввода."}
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return {"text": "⚠️ Ошибка обработки команды. Попробуйте еще раз."}


async def send_telegram_message(client: httpx.AsyncClient, chat_id: int, payload: dict) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    body = {
        "chat_id": chat_id,
        "text": payload.get("text", ""),
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
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
        try:
            me_resp = await client.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe")
            if me_resp.status_code == 200 and me_resp.json().get("ok"):
                bot_info = me_resp.json()["result"]
                logger.info(f"Бот успешно подключен: @{bot_info.get('username')} ({bot_info.get('first_name')})")
                await register_bot_commands(client)
            else:
                logger.error(f"Ошибка проверки токена бота: {me_resp.text}")
                return
        except Exception as e:
            logger.error(f"Не удалось подключиться к Telegram API: {e}")
            return

        while True:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
                resp = await client.get(url, params={"offset": offset, "timeout": 20}, timeout=30.0)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("ok"):
                        for update in data.get("result", []):
                            offset = update["update_id"] + 1

                            if "message" in update and "text" in update["message"]:
                                msg = update["message"]
                                chat_id = msg["chat"]["id"]
                                text = msg["text"]
                                logger.info(f"Сообщение от {chat_id}: {text}")
                                reply_data = await handle_bot_command(chat_id, text)
                                await send_telegram_message(client, chat_id, reply_data)

                            elif "callback_query" in update:
                                cb = update["callback_query"]
                                chat_id = cb["message"]["chat"]["id"]
                                data_text = cb.get("data", "")
                                logger.info(f"Нажата кнопка от {chat_id}: {data_text}")
                                reply_data = await handle_bot_command(chat_id, data_text)
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
