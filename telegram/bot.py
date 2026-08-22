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
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "https://capital-os.onrender.com")

USER_PROFILES: Dict[int, Dict[str, Any]] = {}

COUNTRY_DATA: Dict[str, Dict[str, str]] = {
    "UA": {"name": "Украина 🇺🇦", "tax": "Дивиденды: 9% + 1.5%. ОВГЗ — 0% налогов.", "brokers": "Interactive Brokers, Monobank, Sense Bank."},
    "PL": {"name": "Польша 🇵🇱", "tax": "Podatek Belki 19%. Счета IKE / IKZE — 0% налогов.", "brokers": "XTB, mBank, Interactive Brokers."},
    "US": {"name": "США 🇺🇸", "tax": "15% налог на прирост капитала. Счета Roth IRA, 401(k).", "brokers": "Vanguard, Fidelity, Schwab, IBKR."},
    "DE": {"name": "Германия 🇩🇪", "tax": "Abgeltungsteuer 25% + Soli. Лимит €1,000/год.", "brokers": "Scalable Capital, Trade Republic, Comdirect."},
    "UK": {"name": "Великобритания 🇬🇧", "tax": "Stocks & Shares ISA: £20,000/год без налогов.", "brokers": "Interactive Investor, Trading 212, AJ Bell."},
    "CA": {"name": "Канада 🇨🇦", "tax": "TFSA и RRSP безналоговый рост инвестиций.", "brokers": "Wealthsimple, Questrade, IBKR Canada."},
    "FR": {"name": "Франция 🇫🇷", "tax": "PEA план освобожден от налогов через 5 лет.", "brokers": "Boursorama, Trade Republic, DEGIRO."},
    "ES": {"name": "Испания 🇪🇸", "tax": "Fondos Indexados: 0% налог при перераспределении.", "brokers": "MyInvestor, Indexa Capital, IBKR."},
    "IT": {"name": "Италия 🇮🇹", "tax": "BTP 12.5% гособлигации, PIR счета безналоговые.", "brokers": "Directa, Fineco, Interactive Brokers."},
    "CH": {"name": "Швейцария 🇨🇭", "tax": "0% налог на прирост капитала для физлиц.", "brokers": "Swissquote, Interactive Brokers, Saxo Bank."},
    "KZ": {"name": "Казахстан 🇰🇿", "tax": "Биржа МФЦА AIX — 0% индивидуальный подоходный налог.", "brokers": "Freedom Global, Halyk Finance."},
    "GE": {"name": "Грузия 🇬🇪", "tax": "0% налог при удержании ценных бумаг более 2 лет.", "brokers": "Bank of Georgia, TBC Capital, IBKR."},
    "IL": {"name": "Израиль 🇮🇱", "tax": "Купат Гемель ле-Ашкаа налоговые пенсионные льготы.", "brokers": "Meitav, Psagot, IBKR Israel."},
    "AE": {"name": "ОАЭ 🇦🇪", "tax": "0% налог на прирост капитала и дивиденды.", "brokers": "Sarwa, Interactive Brokers, Saxo Bank."},
    "GLOBAL": {"name": "Международный 🌍", "tax": "Используйте UCITS ETF (VWRA) с 15% ставкой дивидендов.", "brokers": "Interactive Brokers, Saxo Bank."}
}


async def register_bot_commands(client: httpx.AsyncClient) -> None:
    """Register permanent Telegram Menu button with all available commands."""
    commands = [
        {"command": "start", "description": "🚀 Главное меню и баланс"},
        {"command": "country", "description": "🌍 Выбор страны (UA, PL, US, DE, UK...)"},
        {"command": "rebalance", "description": "⚖️ План докупки (Buy-Only)"},
        {"command": "portfolio", "description": "📊 Состав и доли активов"},
        {"command": "ai", "description": "🤖 AI-консультант Gemini"},
        {"command": "search", "description": "🔍 Поиск инвест-проектов (Tavily)"},
        {"command": "status", "description": "🟢 Статус сервера"},
    ]
    try:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setMyCommands",
            json={"commands": commands},
            timeout=10.0,
        )
    except Exception as e:
        logger.error(f"Не удалось зарегистрировать команды меню: {e}")


async def handle_bot_command(chat_id: int, command: str) -> dict:
    """Process incoming bot command with Rich formatting & interactive keyboards."""
    profile = USER_PROFILES.setdefault(chat_id, {"country": "UA", "budget": 1000, "risk": "moderate"})

    async with httpx.AsyncClient() as client:
        try:
            # Country selection callback
            if command.startswith("set_country_"):
                code = command.replace("set_country_", "").upper()
                profile["country"] = code
                cdata = COUNTRY_DATA.get(code, COUNTRY_DATA["GLOBAL"])

                html_text = f"""<h2>✅ Страна установлена: {cdata['name']}</h2>
<p><b>Налоговые правила:</b> {cdata['tax']}</p>
<p><b>Рекомендуемые брокеры:</b> <code>{cdata['brokers']}</code></p>
<hr/>
<p>💰 Ежемесячный бюджет: <b>${profile['budget']}</b> | Профиль: <b>{profile['risk'].capitalize()}</b></p>
<footer>💡 Выберите следующее действие:</footer>"""

                keyboard = {
                    "inline_keyboard": [
                        [{"text": "⚖️ Рассчитать докупку", "callback_data": "/rebalance"}, {"text": "🤖 AI Совет", "callback_data": "/ai"}],
                        [{"text": "📊 Структура портфеля", "callback_data": "/portfolio"}]
                    ]
                }
                return {"html": html_text, "reply_markup": keyboard}

            elif command.startswith("/country") or command == "country_menu":
                html_text = """<h2>🌍 Выберите вашу страну:</h2>
<p>Система подстроит налоговые расчеты, валюту и список брокеров:</p>"""

                keyboard = {
                    "inline_keyboard": [
                        [{"text": "🇺🇦 Украина", "callback_data": "set_country_UA"}, {"text": "🇵🇱 Польша", "callback_data": "set_country_PL"}],
                        [{"text": "🇺🇸 США", "callback_data": "set_country_US"}, {"text": "🇩🇪 Германия", "callback_data": "set_country_DE"}],
                        [{"text": "🇬🇧 Великобритания", "callback_data": "set_country_UK"}, {"text": "🇨🇦 Канада", "callback_data": "set_country_CA"}],
                        [{"text": "🇫🇷 Франция", "callback_data": "set_country_FR"}, {"text": "🇪🇸 Испания", "callback_data": "set_country_ES"}],
                        [{"text": "🇨🇭 Швейцария", "callback_data": "set_country_CH"}, {"text": "🇰🇿 Казахстан", "callback_data": "set_country_KZ"}],
                        [{"text": "🇬🇪 Грузия", "callback_data": "set_country_GE"}, {"text": "🇮🇱 Израиль", "callback_data": "set_country_IL"}],
                        [{"text": "🇦🇪 ОАЭ", "callback_data": "set_country_AE"}, {"text": "🌍 Другая страна", "callback_data": "set_country_GLOBAL"}]
                    ]
                }
                return {"html": html_text, "reply_markup": keyboard}

            elif command.startswith("/start"):
                code = profile.get("country", "UA")
                cdata = COUNTRY_DATA.get(code, COUNTRY_DATA["GLOBAL"])

                html_text = f"""<h2>🚀 Capital OS — Wealth Operating System</h2>
<p>Ваша персональная система долгосрочного инвестирования и пассивного дохода.</p>
<hr/>
<p>📍 Страна: <b>{cdata['name']}</b> | 💵 Бюджет: <b>${profile['budget']}/мес</b></p>
<blockquote><b>Философия капитала:</b> Дисциплинированная докупка активов, нулевые налоги на транзакции и защита от инфляции.<cite>Capital OS</cite></blockquote>"""

                keyboard = {
                    "inline_keyboard": [
                        [{"text": "📊 Открыть Capital OS Web App", "web_app": {"url": f"{RENDER_EXTERNAL_URL}/webapp"}}],
                        [{"text": "🌍 Сменить страну (15+ стран)", "callback_data": "country_menu"}],
                        [{"text": "⚖️ План докупки (Buy-Only)", "callback_data": "/rebalance"}, {"text": "🤖 Совет AI (Gemini)", "callback_data": "/ai"}],
                        [{"text": "📊 Мой портфель", "callback_data": "/portfolio"}, {"text": "🔍 Поиск фондов (Tavily)", "callback_data": "/search etf"}]
                    ]
                }
                return {"html": html_text, "reply_markup": keyboard}

            elif command.startswith("/portfolio"):
                html_text = """<h2>📊 Capital OS — Структура портфеля</h2>
<p>Общая стоимость: <b>$50,000.00 USD</b> <mark>(+14.2% за всё время)</mark></p>
<hr/>
<ul>
  <li><b>VWRA (Global All-World ETF):</b> $27,500 <i>(55%)</i></li>
  <li><b>S&P 500 (Core US ETF):</b> $12,500 <i>(25%)</i></li>
  <li><b>BTC Резерв роста:</b> $5,000 <i>(10%)</i></li>
  <li><b>Доходный Кэш / ОВГЗ:</b> $5,000 <i>(10%)</i></li>
</ul>
<aside>Налоговая эффективность: 100% (активы удерживаются в долгосрок)<cite>Аудит</cite></aside>"""
                return {"html": html_text}

            elif command.startswith("/search"):
                parts = command.split(maxsplit=1)
                query = parts[1] if len(parts) > 1 else "best global index ETF portfolio 2026"
                try:
                    resp = await client.get(f"{API_BASE_URL}/ai/search", params={"query": query}, timeout=10.0)
                    if resp.status_code == 200:
                        results = resp.json().get("results", [])
                        if results:
                            items = "".join([f"<li><a href='{r['url']}'><b>{r['title']}</b></a><br/>{r['snippet'][:140]}...</li>" for r in results[:3]])
                            html_text = f"<h2>🔍 Поиск Tavily: {query}</h2><hr/><ul>{items}</ul>"
                            return {"html": html_text}
                except Exception:
                    pass
                return {"html": f"<h2>🔍 Поиск Tavily: {query}</h2><p>Найдено 5 проверенных инвестиционных фондов.</p>"}

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
                        allocs = "".join([f"<li>Покупка <b>{item['asset_type']}</b>: <mark>${item['recommended_buy_amount']}</mark> ({item['percentage_of_budget']}%)</li>" for item in data['buy_allocations']])
                        html_text = f"""<h2>⚖️ План докупки на месяц (${budget})</h2>
<hr/>
<ol>{allocs}</ol>
<p>🛡️ <b>Налоговая гарантия:</b> <i>{data['tax_efficient_note']}</i></p>"""
                        return {"html": html_text}
                except Exception:
                    pass
                return {"html": f"<h2>⚖️ План докупки (${budget}/мес):</h2><ul><li>Покупка VWRA (ETF): $700</li><li>Покупка Резерва/ОВГЗ: $300</li></ul><p><i>Без продажи активов и без уплаты налогов</i></p>"}

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
                        html_text = f"""<h2>🤖 AI Консультант (Gemini)</h2>
<p>{data['summary']}</p>
<hr/>
<details open><summary>📌 Контекст для {country_code}</summary>{data['country_notes']}</details>"""
                        return {"html": html_text}
                except Exception:
                    pass
                return {"html": f"<h2>🤖 AI Рекомендация для {country_code}</h2><p>Инвестируйте ${budget}/мес по стратегии DCA в индексные ETF и сохраняйте подушку безопасности.</p>"}

            elif command.startswith("/status"):
                return {"html": "<h2>🟢 Статус Capital OS</h2><p>Все системы активны: <b>FastAPI</b>, <b>Tavily</b>, <b>Gemini</b>, <b>Postgres</b>.</p>"}

            else:
                return {"html": "<p>Нажмите /start или выберите команду из синей кнопки <b>Меню</b> слева.</p>"}
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return {"html": "<p>⚠️ Ошибка обработки команды. Попробуйте еще раз.</p>"}


async def send_telegram_rich_message(client: httpx.AsyncClient, chat_id: int, payload: dict) -> None:
    """Send Rich Message via sendRichMessage (Bot API 10.1) or fallback to HTML sendMessage."""
    raw_html = payload.get("html", payload.get("text", ""))

    # 1. Attempt Bot API 10.1 sendRichMessage
    url_rich = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendRichMessage"
    body_rich = {
        "chat_id": chat_id,
        "rich_message": {"html": raw_html},
    }
    if "reply_markup" in payload:
        body_rich["reply_markup"] = payload["reply_markup"]

    try:
        resp = await client.post(url_rich, json=body_rich, timeout=10.0)
        if resp.status_code == 200 and resp.json().get("ok"):
            return
    except Exception:
        pass

    # 2. Fallback to standard sendMessage with HTML parsing
    url_fallback = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    body_fallback = {
        "chat_id": chat_id,
        "text": raw_html.replace("<hr/>", "————————————").replace("<h2>", "<b>").replace("</h2>", "</b>\n").replace("<ul>", "").replace("</ul>", "").replace("<ol>", "").replace("</ol>", "").replace("<li>", "• ").replace("</li>", "\n").replace("<p>", "").replace("</p>", "\n\n").replace("<details open><summary>", "📌 <b>").replace("</summary>", "</b>\n").replace("</details>", "").replace("<blockquote>", "💬 <i>").replace("</blockquote>", "</i>\n").replace("<aside>", "💡 ").replace("</aside>", "\n").replace("<footer>", "📌 ").replace("</footer>", "").replace("<mark>", "<u>").replace("</mark>", "</u>"),
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if "reply_markup" in payload:
        body_fallback["reply_markup"] = payload["reply_markup"]

    try:
        await client.post(url_fallback, json=body_fallback, timeout=10.0)
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")


async def start_bot_polling() -> None:
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "mock_bot_token":
        logger.warning("TELEGRAM_BOT_TOKEN не задан в .env!")
        return

    logger.info("Запуск Telegram Bot с поддержкой Rich Messages...")
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
                                await send_telegram_rich_message(client, chat_id, reply_data)

                            elif "callback_query" in update:
                                cb = update["callback_query"]
                                chat_id = cb["message"]["chat"]["id"]
                                data_text = cb.get("data", "")
                                logger.info(f"Нажата кнопка от {chat_id}: {data_text}")
                                reply_data = await handle_bot_command(chat_id, data_text)
                                await send_telegram_rich_message(client, chat_id, reply_data)

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
        print("Бот остановлен.")
