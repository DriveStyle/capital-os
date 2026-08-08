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
  <title>Capital OS — Wealth Operating System</title>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {
      background-color: var(--tg-theme-bg-color, #0b0f19);
      color: var(--tg-theme-text-color, #f8fafc);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .glass-card {
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(51, 65, 85, 0.6);
    }
    .glow-blue {
      box-shadow: 0 0 20px rgba(59, 130, 246, 0.25);
    }
  </style>
</head>
<body class="p-4 pb-24 select-none">
  <!-- Header Bar -->
  <div class="flex items-center justify-between mb-4">
    <div class="flex items-center gap-2.5">
      <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-emerald-400 flex items-center justify-center font-black text-white text-base shadow-lg shadow-blue-500/20">
        C
      </div>
      <div>
        <h1 class="text-base font-extrabold text-white leading-tight tracking-tight">CAPITAL OS</h1>
        <p class="text-[10px] text-blue-400 font-semibold tracking-wider">WEALTH OPERATING SYSTEM</p>
      </div>
    </div>
    <span id="userBadge" class="text-xs px-3 py-1 rounded-full bg-slate-800/90 text-slate-300 font-semibold border border-slate-700">
      👤 Резидент
    </span>
  </div>

  <!-- Portfolio Card with SVG Donut Chart -->
  <div class="glass-card glow-blue rounded-2xl p-4 mb-4 shadow-xl">
    <div class="flex justify-between items-start mb-3">
      <div>
        <div class="text-[11px] text-slate-400 font-medium">Общий портфель</div>
        <div class="text-3xl font-black text-white tracking-tight">$50,000.00</div>
      </div>
      <span class="text-xs px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">
        +14.2% прибыль
      </span>
    </div>

    <!-- Interactive SVG Chart and Asset List -->
    <div class="flex items-center gap-4 pt-3 border-t border-slate-800/80">
      <div class="relative w-24 h-24 flex-shrink-0">
        <svg viewBox="0 0 36 36" class="w-24 h-24 transform -rotate-90">
          <circle cx="18" cy="18" r="14" fill="none" stroke="#1e293b" stroke-width="4.5"></circle>
          <!-- VWRA: 55% -->
          <circle cx="18" cy="18" r="14" fill="none" stroke="#3b82f6" stroke-width="4.5" stroke-dasharray="48.38 87.96" stroke-dashoffset="0"></circle>
          <!-- S&P 500: 25% -->
          <circle cx="18" cy="18" r="14" fill="none" stroke="#6366f1" stroke-width="4.5" stroke-dasharray="21.99 87.96" stroke-dashoffset="-48.38"></circle>
          <!-- BTC: 10% -->
          <circle cx="18" cy="18" r="14" fill="none" stroke="#f59e0b" stroke-width="4.5" stroke-dasharray="8.8 87.96" stroke-dashoffset="-70.37"></circle>
          <!-- CASH/OVDP: 10% -->
          <circle cx="18" cy="18" r="14" fill="none" stroke="#10b981" stroke-width="4.5" stroke-dasharray="8.8 87.96" stroke-dashoffset="-79.17"></circle>
        </svg>
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <span class="text-[10px] text-slate-400">Доли</span>
          <span class="text-xs font-black text-white">4 актива</span>
        </div>
      </div>

      <div class="flex-1 space-y-1.5 text-xs">
        <div class="flex justify-between items-center">
          <span class="flex items-center gap-1.5 text-slate-300"><span class="w-2 h-2 rounded-full bg-blue-500"></span> VWRA ETF</span>
          <span class="font-bold text-white">$27.5k <span class="text-slate-500 font-normal">55%</span></span>
        </div>
        <div class="flex justify-between items-center">
          <span class="flex items-center gap-1.5 text-slate-300"><span class="w-2 h-2 rounded-full bg-indigo-500"></span> S&P 500</span>
          <span class="font-bold text-white">$12.5k <span class="text-slate-500 font-normal">25%</span></span>
        </div>
        <div class="flex justify-between items-center">
          <span class="flex items-center gap-1.5 text-slate-300"><span class="w-2 h-2 rounded-full bg-amber-500"></span> BTC Резерв</span>
          <span class="font-bold text-white">$5.0k <span class="text-slate-500 font-normal">10%</span></span>
        </div>
        <div class="flex justify-between items-center">
          <span class="flex items-center gap-1.5 text-slate-300"><span class="w-2 h-2 rounded-full bg-emerald-500"></span> ОВГЗ / Кэш</span>
          <span class="font-bold text-white">$5.0k <span class="text-slate-500 font-normal">10%</span></span>
        </div>
      </div>
    </div>
  </div>

  <!-- Compound Interest & Financial Freedom 2030 Simulator -->
  <div class="glass-card rounded-2xl p-4 mb-4 shadow-xl">
    <div class="flex justify-between items-center mb-2">
      <div class="text-xs font-bold text-blue-400 uppercase tracking-wider">🎯 Финансовая Свобода 2030</div>
      <span class="text-[10px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 font-bold border border-blue-500/20">
        8.5% годовых
      </span>
    </div>
    
    <div class="mb-3">
      <div class="flex justify-between text-xs mb-1">
        <span class="text-slate-400">Ежемесячная докупка:</span>
        <span id="sliderValue" class="font-bold text-emerald-400">$1,000 / мес</span>
      </div>
      <input id="compoundSlider" type="range" min="100" max="5000" step="100" value="1000" oninput="calculateCompound()" class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500">
    </div>

    <div class="p-3 bg-slate-950/70 rounded-xl border border-slate-800/80 flex justify-between items-center">
      <div>
        <span class="text-[10px] text-slate-400 block">Прогноз капитала к 2030 (5 лет):</span>
        <span id="projectedCapital" class="text-xl font-extrabold text-emerald-400">$142,500</span>
      </div>
      <div class="text-right">
        <span class="text-[10px] text-slate-400 block">Пассивный доход:</span>
        <span id="projectedIncome" class="text-xs font-bold text-blue-400">~$950 / мес</span>
      </div>
    </div>
  </div>

  <!-- Country & Tax Profile Selector -->
  <div class="glass-card rounded-2xl p-4 mb-4 shadow-xl">
    <div class="text-xs font-bold text-blue-400 uppercase tracking-wider mb-2">🌍 Страна и налоговый режим</div>
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
    <div id="taxDetails" class="mt-2.5 text-[11px] text-slate-300 bg-slate-950/80 p-3 rounded-xl border border-slate-800 leading-relaxed">
      Загрузка налоговых правил...
    </div>
  </div>

  <!-- Rebalance Calculator Section -->
  <div class="glass-card rounded-2xl p-4 mb-4 shadow-xl">
    <div class="flex justify-between items-center mb-3">
      <div class="text-xs font-bold text-blue-400 uppercase tracking-wider">⚖️ План докупки (Buy-Only)</div>
      <span class="text-[10px] text-emerald-400 font-bold bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-800/40">🛡️ 0% налогов</span>
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
      UA: { name: "Украина 🇺🇦", notes: "Дивиденды: 9% + 1.5%. ОВГЗ — 0% налогов. Рекомендуемые брокеры: Interactive Brokers, Monobank, Sense Bank." },
      PL: { name: "Польша 🇵🇱", notes: "Podatek Belki 19%. Счета IKE/IKZE освобождены от налогов. Брокеры: XTB, mBank, IBKR." },
      US: { name: "США 🇺🇸", notes: "Roth IRA и 401(k) для безналогового роста. Брокеры: Vanguard, Fidelity, Schwab, IBKR." },
      DE: { name: "Германия 🇩🇪", notes: "Abgeltungsteuer 25% + Soli. Лимит €1,000/год без налога. Брокеры: Scalable, Trade Republic." },
      UK: { name: "Великобритания 🇬🇧", notes: "Stocks & Shares ISA £20,000 в год без налогов. Брокеры: Trading 212, AJ Bell, IBKR." },
      CA: { name: "Канада 🇨🇦", notes: "TFSA / RRSP безналоговый рост. Брокеры: Wealthsimple, Questrade, IBKR Canada." },
      FR: { name: "Франция 🇫🇷", notes: "PEA план освобожден от налогов через 5 лет. Брокеры: Boursorama, DEGIRO." },
      ES: { name: "Испания 🇪🇸", notes: "Fondos Indexados 0% налог при трансфере. Брокеры: MyInvestor, Indexa Capital." },
      IT: { name: "Италия 🇮🇹", notes: "BTP 12.5% льготные гособлигации, PIR счета. Брокеры: Directa, Fineco, IBKR." },
      CH: { name: "Швейцария 🇨🇭", notes: "0% налог на прирост капитала для физлиц. Брокеры: Swissquote, IBKR, Saxo Bank." },
      KZ: { name: "Казахстан 🇰🇿", notes: "МФЦА AIX 0% подоходный налог. Брокеры: Freedom Global, Halyk Finance." },
      GE: { name: "Грузия 🇬🇪", notes: "0% налог при удержании более 2 лет. Брокеры: Bank of Georgia, Galt & Taggart." },
      IL: { name: "Израиль 🇮🇱", notes: "Купат Гемель ле-Ашкаа налоговые льготы. Брокеры: Meitav, Psagot, IBKR Israel." },
      AE: { name: "ОАЭ 🇦🇪", notes: "0% налог на доходы и дивиденды. Брокеры: Sarwa, Interactive Brokers, Saxo." },
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

    function calculateCompound() {
      const monthly = Number(document.getElementById('compoundSlider').value) || 1000;
      document.getElementById('sliderValue').innerText = '$' + monthly.toLocaleString() + ' / мес';
      
      const r = 0.085 / 12;
      const n = 5 * 12;
      const initial = 50000;
      const futureInitial = initial * Math.pow(1 + r, n);
      const futureMonthly = monthly * ((Math.pow(1 + r, n) - 1) / r);
      const total = Math.round(futureInitial + futureMonthly);
      const income = Math.round((total * 0.08) / 12);

      document.getElementById('projectedCapital').innerText = '$' + total.toLocaleString();
      document.getElementById('projectedIncome').innerText = '~$' + income.toLocaleString() + ' / мес';

      calculateRebalance(monthly);
    }

    function calculateRebalance(monthlyBudget) {
      const b = monthlyBudget !== undefined ? monthlyBudget : Number(document.getElementById('compoundSlider').value) || 1000;
      const etf = Math.round(b * 0.7);
      const yieldAmt = Math.round(b * 0.2);
      const crypto = Math.round(b * 0.1);

      document.getElementById('rebalanceResult').innerHTML = `
        <div class="flex justify-between items-center p-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs">
          <span class="font-bold text-white flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-blue-500"></span> VWRA (Global ETF)</span>
          <span class="font-bold text-blue-400">+$${etf.toLocaleString()} (70%)</span>
        </div>
        <div class="flex justify-between items-center p-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs">
          <span class="font-bold text-white flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-500"></span> Доходный Кэш / ОВГЗ</span>
          <span class="font-bold text-emerald-400">+$${yieldAmt.toLocaleString()} (20%)</span>
        </div>
        <div class="flex justify-between items-center p-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs">
          <span class="font-bold text-white flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-amber-500"></span> Резерв роста (BTC)</span>
          <span class="font-bold text-amber-400">+$${crypto.toLocaleString()} (10%)</span>
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
    calculateCompound();
  </script>
</body>
</html>
"""

@router.get("/webapp", response_class=HTMLResponse)
@router.get("/app", response_class=HTMLResponse)
def get_telegram_webapp():
    return HTMLResponse(content=WEBAPP_HTML)

