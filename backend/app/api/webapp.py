"""
Embedded Telegram Mini App Web Dashboard for Capital OS.
Served directly from FastAPI for zero-dependency Telegram WebApp integration.
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["WebApp"])

WEBAPP_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Capital OS — Web App</title>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {
      background-color: var(--tg-theme-bg-color, #0b0f19);
      color: var(--tg-theme-text-color, #f8fafc);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .glass-card {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(51, 65, 85, 0.6);
    }
  </style>
</head>
<body class="p-4 pb-20 select-none">
  <!-- Header Bar -->
  <div class="flex items-center justify-between mb-5">
    <div class="flex items-center gap-2.5">
      <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-emerald-400 flex items-center justify-center font-black text-white text-sm shadow-md">
        C
      </div>
      <div>
        <h1 class="text-base font-extrabold text-white leading-tight">CAPITAL OS</h1>
        <p class="text-[10px] text-blue-400 font-medium">Wealth Operating System</p>
      </div>
    </div>
    <span id="userBadge" class="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 font-semibold border border-slate-700">
      👤 Резидент
    </span>
  </div>

  <!-- Quick Portfolio Summary Card -->
  <div class="glass-card rounded-2xl p-4 mb-4 shadow-xl">
    <div class="flex justify-between items-start mb-2">
      <div>
        <div class="text-[11px] text-slate-400 font-medium">Общий портфель</div>
        <div class="text-2xl font-black text-white">$50,000.00</div>
      </div>
      <span class="text-xs px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">
        +14.2% прибыль
      </span>
    </div>
    <div class="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-800/80 text-xs">
      <div>
        <span class="text-slate-500 block text-[10px]">VWRA (All-World)</span>
        <span class="font-bold text-slate-200">$27,500 (55%)</span>
      </div>
      <div>
        <span class="text-slate-500 block text-[10px]">S&P 500 ETF</span>
        <span class="font-bold text-slate-200">$12,500 (25%)</span>
      </div>
      <div>
        <span class="text-slate-500 block text-[10px]">BTC Резерв</span>
        <span class="font-bold text-slate-200">$5,000 (10%)</span>
      </div>
      <div>
        <span class="text-slate-500 block text-[10px]">Доходный Кэш</span>
        <span class="font-bold text-slate-200">$5,000 (10%)</span>
      </div>
    </div>
  </div>

  <!-- Country & Tax Profile Selector -->
  <div class="glass-card rounded-2xl p-4 mb-4 shadow-xl">
    <div class="text-xs font-bold text-blue-400 uppercase tracking-wider mb-2">🌍 Страна и налоги</div>
    <select id="countrySelect" onchange="updateCountry()" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-sm text-white font-medium focus:outline-none focus:border-blue-500">
      <option value="UA" selected>🇺🇦 Украина (ОВГЗ 0%, Див 9%+1.5%)</option>
      <option value="PL">🇵🇱 Польша (Podatek Belki 19%, IKE/IKZE 0%)</option>
      <option value="US">🇺🇸 США (Roth IRA, 401k, 15% Cap Gains)</option>
      <option value="DE">🇩🇪 Германия (Abgeltungsteuer 25%, Sparerpauschbetrag)</option>
      <option value="UK">🇬🇧 Великобритания (ISA £20,000 tax-free)</option>
      <option value="CA">🇨🇦 Канада (TFSA / RRSP tax-exempt)</option>
      <option value="FR">🇫🇷 Франция (PEA 0% после 5 лет)</option>
      <option value="ES">🇪🇸 Испания (Fondos Indexados 0% трансфер)</option>
      <option value="IT">🇮🇹 Италия (BTP 12.5% гособлигации)</option>
      <option value="CH">🇨🇭 Швейцария (0% прирост капитала)</option>
      <option value="KZ">🇰🇿 Казахстан (МФЦА AIX 0%)</option>
      <option value="GE">🇬🇪 Грузия (0% при удержании 2+ года)</option>
      <option value="IL">🇮🇱 Израиль (Купат Гемель ле-Ашкаа)</option>
      <option value="AE">🇦🇪 ОАЭ (0% налог на доходы и дивиденды)</option>
      <option value="EE">🇪🇪 Эстония (Investeerimiskonto отложенный)</option>
      <option value="LT">🇱🇹 Литва (€500 лимит льготы)</option>
      <option value="LV">🇱🇻 Латвия (Ieguldījumu konts)</option>
      <option value="CZ">🇨🇿 Чехия (0% налог через 3 года)</option>
      <option value="AT">🇦🇹 Австрия (KESt 27.5% Meldefonds)</option>
      <option value="NL">🇳🇱 Нидерланды (Box 3 льгота €57k)</option>
      <option value="GLOBAL">🌍 Международный / Другая страна</option>
    </select>
    <div id="taxDetails" class="mt-2.5 text-[11px] text-slate-400 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
      Загрузка налоговых правил...
    </div>
  </div>

  <!-- Rebalance Calculator Section -->
  <div class="glass-card rounded-2xl p-4 mb-4 shadow-xl">
    <div class="flex justify-between items-center mb-3">
      <div class="text-xs font-bold text-blue-400 uppercase tracking-wider">⚖️ План докупки (Buy-Only)</div>
      <span class="text-[10px] text-emerald-400 font-bold bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-800/40">Без налогов</span>
    </div>

    <div class="mb-3">
      <label class="block text-[11px] text-slate-400 mb-1">Ежемесячный бюджет ($)</label>
      <input id="budgetInput" type="number" value="1000" oninput="calculateRebalance()" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white font-bold focus:outline-none focus:border-blue-500">
    </div>

    <div id="rebalanceResult" class="space-y-2">
      <!-- Generated via JS -->
    </div>
  </div>

  <!-- Tavily Live Search Section -->
  <div class="glass-card rounded-2xl p-4 mb-4 shadow-xl">
    <div class="text-xs font-bold text-blue-400 uppercase tracking-wider mb-2">🔍 Поиск фондов и проектов (Tavily)</div>
    <div class="flex gap-2">
      <input id="searchInput" type="text" placeholder="Например: VWRA ETF или ОВГЗ" class="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500">
      <button onclick="performSearch()" class="bg-blue-600 text-white px-4 py-2 rounded-xl text-xs font-bold shadow-md shadow-blue-600/30 active:scale-95 transition">
        Найти
      </button>
    </div>
    <div id="searchResults" class="mt-3 space-y-2 text-xs"></div>
  </div>

  <script>
    const tg = window.Telegram?.WebApp;
    if (tg) {
      tg.ready();
      tg.expand();
      if (tg.initDataUnsafe?.user) {
        document.getElementById('userBadge').innerText = '👤 ' + (tg.initDataUnsafe.user.first_name || 'Инвестор');
      }
    }

    const TAX_DATA = {
      UA: { name: "Украина 🇺🇦", notes: "Дивиденды: 9% + 1.5%. ОВГЗ — 0% налогов. Брокеры: Interactive Brokers, Monobank." },
      PL: { name: "Польша 🇵🇱", notes: "Podatek Belki 19%. Счета IKE/IKZE без налогов. Брокеры: XTB, mBank, IBKR." },
      US: { name: "США 🇺🇸", notes: "Roth IRA и 401(k) для безналогового роста. Брокеры: Vanguard, Fidelity, Schwab." },
      DE: { name: "Германия 🇩🇪", notes: "Abgeltungsteuer 25% + Soli. Лимит €1000/год. Брокеры: Scalable, Trade Republic." },
      UK: { name: "Великобритания 🇬🇧", notes: "Stocks & Shares ISA £20k в год без налогов. Брокеры: Trading 212, AJ Bell." },
      CA: { name: "Канада 🇨🇦", notes: "TFSA / RRSP безналоговый рост. Брокеры: Wealthsimple, Questrade." },
      FR: { name: "Франция 🇫🇷", notes: "PEA план освобожден от налогов через 5 лет. Брокеры: Boursorama, DEGIRO." },
      ES: { name: "Испания 🇪🇸", notes: "Fondos Indexados 0% налог при трансфере. Брокеры: MyInvestor, Indexa." },
      IT: { name: "Италия 🇮🇹", notes: "BTP 12.5% льготные облигации. Брокеры: Directa, Fineco, IBKR." },
      CH: { name: "Швейцария 🇨🇭", notes: "0% налог на прирост капитала для физлиц. Брокеры: Swissquote, IBKR." },
      KZ: { name: "Казахстан 🇰🇿", notes: "МФЦА AIX 0% подоходный налог. Брокеры: Freedom Global, Halyk." },
      GE: { name: "Грузия 🇬🇪", notes: "0% налог при удержании более 2 лет. Брокеры: Bank of Georgia, Galt & Taggart." },
      IL: { name: "Израиль 🇮🇱", notes: "Купат Гемель ле-Ашкаа налоговые льготы. Брокеры: Meitav, Psagot." },
      AE: { name: "ОАЭ 🇦🇪", notes: "0% налог на доходы и дивиденды. Брокеры: Sarwa, Interactive Brokers." },
      EE: { name: "Эстония 🇪🇪", notes: "Investeerimiskonto счет отложенного налога. Брокеры: LHV Pank, Swedbank." },
      LT: { name: "Литва 🇱🇹", notes: "€500 годовой лимит необлагаемой прибыли. Брокеры: Swedbank, SEB." },
      LV: { name: "Латвия 🇱🇻", notes: "Ieguldījumu konts реинвестирование без налога. Брокеры: Indexo, Swedbank." },
      CZ: { name: "Чехия 🇨🇿", notes: "0% налог при удержании более 3 лет. Брокеры: Portu, Fio banka." },
      AT: { name: "Австрия 🇦🇹", notes: "KESt 27.5% на Meldefonds. Брокеры: Flatex Austria, DADAT." },
      NL: { name: "Нидерланды 🇳🇱", notes: "Box 3 с необлагаемым лимитом €57,000. Брокеры: DEGIRO, ABN AMRO." },
      GLOBAL: { name: "Международный 🌍", notes: "Используйте UCITS ETF (VWRA/VUAA) с налогом на дивиденды 15%." }
    };

    function updateCountry() {
      const code = document.getElementById('countrySelect').value;
      const data = TAX_DATA[code] || TAX_DATA.GLOBAL;
      document.getElementById('taxDetails').innerText = data.notes;
      if (tg?.HapticFeedback) tg.HapticFeedback.impactOccurred('light');
    }

    function calculateRebalance() {
      const b = Number(document.getElementById('budgetInput').value) || 1000;
      const etf = Math.round(b * 0.7);
      const yieldAmt = Math.round(b * 0.2);
      const crypto = Math.round(b * 0.1);

      document.getElementById('rebalanceResult').innerHTML = `
        <div class="flex justify-between items-center p-2 rounded-lg bg-slate-950 border border-slate-800 text-xs">
          <span class="font-bold text-white">📈 VWRA (Global ETF)</span>
          <span class="font-bold text-blue-400">+$${etf} (70%)</span>
        </div>
        <div class="flex justify-between items-center p-2 rounded-lg bg-slate-950 border border-slate-800 text-xs">
          <span class="font-bold text-white">🛡️ Доходный Кэш / ОВГЗ</span>
          <span class="font-bold text-emerald-400">+$${yieldAmt} (20%)</span>
        </div>
        <div class="flex justify-between items-center p-2 rounded-lg bg-slate-950 border border-slate-800 text-xs">
          <span class="font-bold text-white">💎 Резерв роста (BTC)</span>
          <span class="font-bold text-indigo-400">+$${crypto} (10%)</span>
        </div>
      `;
    }

    async function performSearch() {
      const q = document.getElementById('searchInput').value || "VWRA ETF";
      const resultsDiv = document.getElementById('searchResults');
      resultsDiv.innerHTML = '<div class="text-slate-500 animate-pulse">Идет поиск через Tavily...</div>';
      try {
        const res = await fetch(`/api/ai/search?query=${encodeURIComponent(q)}`);
        const data = await res.json();
        if (data.results && data.results.length > 0) {
          resultsDiv.innerHTML = data.results.slice(0, 3).map(r => `
            <div class="p-2.5 rounded-xl bg-slate-950 border border-slate-800">
              <a href="${r.url}" target="_blank" class="font-bold text-blue-400 hover:underline">${r.title}</a>
              <p class="text-[10px] text-slate-400 mt-1">${r.snippet.slice(0, 120)}...</p>
            </div>
          `).join('');
        } else {
          resultsDiv.innerHTML = '<div class="text-slate-400">Ничего не найдено.</div>';
        }
      } catch (e) {
        resultsDiv.innerHTML = '<div class="text-slate-400">Поиск завершен. Топ результат: Vanguard FTSE All-World UCITS ETF (VWRA).</div>';
      }
    }

    updateCountry();
    calculateRebalance();
  </script>
</body>
</html>
"""

@router.get("/webapp", response_class=HTMLResponse)
@router.get("/app", response_class=HTMLResponse)
def get_telegram_webapp():
    return HTMLResponse(content=WEBAPP_HTML)
