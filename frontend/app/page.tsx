"use client";

import { useState } from "react";

interface Asset {
  symbol: string;
  name: string;
  allocation: number;
  value: number;
  type: string;
}

interface BuyAllocation {
  asset_type: string;
  recommended_buy_amount: number;
  percentage_of_budget: number;
  action: string;
}

interface Transaction {
  id: string;
  type: "buy" | "deposit" | "dividend" | "withdrawal";
  amount: number;
  symbol: string;
  date: string;
}

export default function CapitalOSDashboard() {
  const [activeTab, setActiveTab] = useState<"overview" | "rebalance" | "ai" | "voice" | "goals">("overview");
  const [budget, setBudget] = useState<number>(1000);
  const [risk, setRisk] = useState<string>("moderate");
  const [country, setCountry] = useState<string>("UA");
  const [loadingAi, setLoadingAi] = useState<boolean>(false);
  const [loadingRebalance, setLoadingRebalance] = useState<boolean>(false);

  // Voice assistant state
  const [voiceQuery, setVoiceQuery] = useState<string>("");
  const [voiceResponse, setVoiceResponse] = useState<{
    transcript_received: string;
    intent: str;
    ai_response: string;
    suggested_action?: string;
  } | null>(null);

  // Rebalance result state
  const [rebalanceData, setRebalanceData] = useState<{
    current_total_value: number;
    monthly_budget: number;
    projected_total_value: number;
    risk_score: number;
    buy_allocations: BuyAllocation[];
    tax_efficient_note: string;
  } | null>({
    current_total_value: 50000,
    monthly_budget: 1000,
    projected_total_value: 51000,
    risk_score: 55,
    buy_allocations: [
      { asset_type: "ETF", recommended_buy_amount: 700, percentage_of_budget: 70, action: "Buy ETF assets to bring category closer to target (70%)" },
      { asset_type: "Yield", recommended_buy_amount: 200, percentage_of_budget: 20, action: "Buy Yield reserve assets for liquidity" },
      { asset_type: "Crypto", recommended_buy_amount: 100, percentage_of_budget: 10, action: "Top-up crypto reserve for capital growth" },
    ],
    tax_efficient_note: "Rebalancing performed strictly via fresh buy orders. No asset sales required, zero capital gains tax triggered."
  });

  const [aiResult, setAiResult] = useState<{
    summary: string;
    risk_assessment: string;
    recommended_actions: { category: string; action: string; priority: string; rationale: string }[];
    country_notes: string;
  } | null>({
    summary: "Balanced wealth operating strategy maintaining strong capital safety and steady global indexing.",
    risk_assessment: "Risk profile evaluated as [MODERATE]. Recommended investment horizon: 5+ years.",
    recommended_actions: [
      {
        category: "Broad Market Indexing",
        action: "Allocate 70% ($700/mo) into low-cost global ETFs (VWRA/S&P 500).",
        priority: "High",
        rationale: "Core wealth foundation providing broad diversification across global equities.",
      },
      {
        category: "Opportunistic Reserve",
        action: "Keep 30% ($300/mo) in high-yield reserves / government bonds.",
        priority: "Medium",
        rationale: "Liquidity safety buffer for market dips and income generation.",
      },
    ],
    country_notes: "Country module [UA]: Utilize tax-exempt government bonds (OVDP) and monitor foreign dividend tax filing requirements (9% + 1.5%).",
  });

  const [transactions, setTransactions] = useState<Transaction[]>([
    { id: "tx-1", type: "buy", amount: 700, symbol: "VWRA", date: "2026-08-01" },
    { id: "tx-2", type: "dividend", amount: 45.2, symbol: "S&P 500", date: "2026-07-28" },
    { id: "tx-3", type: "deposit", amount: 1000, symbol: "USD", date: "2026-07-25" },
  ]);

  const assets: Asset[] = [
    { symbol: "VWRA", name: "Vanguard FTSE All-World", allocation: 55, value: 27500, type: "ETF" },
    { symbol: "S&P 500", name: "iShares Core S&P 500", allocation: 25, value: 12500, type: "ETF" },
    { symbol: "BTC", name: "Bitcoin Reserve", allocation: 10, value: 5000, type: "Crypto" },
    { symbol: "CASH", name: "High-Yield Reserve", allocation: 10, value: 5000, type: "Yield" },
  ];

  const handleCalculateRebalance = async () => {
    setLoadingRebalance(true);
    try {
      const res = await fetch("http://localhost:8000/api/portfolios/rebalance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ current_assets: assets, monthly_budget: budget, risk_profile: risk }),
      });
      if (res.ok) {
        const data = await res.json();
        setRebalanceData(data);
      }
    } catch {
      // Local fallback
      setRebalanceData({
        current_total_value: 50000,
        monthly_budget: budget,
        projected_total_value: 50000 + budget,
        risk_score: risk === "conservative" ? 30 : risk === "moderate" ? 55 : 85,
        buy_allocations: [
          { asset_type: "ETF", recommended_buy_amount: Math.round(budget * 0.7), percentage_of_budget: 70, action: "Buy global index ETFs" },
          { asset_type: "Yield", recommended_buy_amount: Math.round(budget * 0.2), percentage_of_budget: 20, action: "Buy high-yield reserve assets" },
          { asset_type: "Crypto", recommended_buy_amount: Math.round(budget * 0.1), percentage_of_budget: 10, action: "Buy digital store of value" },
        ],
        tax_efficient_note: "Rebalancing performed strictly via fresh buy orders. Zero capital gains tax triggered."
      });
    } finally {
      setLoadingRebalance(false);
    }
  };

  const handleGenerateAdvice = async () => {
    setLoadingAi(true);
    try {
      const res = await fetch("http://localhost:8000/api/ai/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "demo-user",
          monthly_investment_budget: budget,
          risk_tolerance: risk,
          country_code: country,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setAiResult(data);
      }
    } catch {
      setAiResult({
        summary: `Tailored ${risk.toUpperCase()} wealth strategy for country [${country}] with $${budget}/mo allocation.`,
        risk_assessment: `Risk profile evaluated as [${risk.toUpperCase()}]. Target horizon: 5+ years.`,
        recommended_actions: [
          { category: "Core Indexing", action: `Allocate $${Math.round(budget * 0.75)}/mo into low-cost index ETFs.`, priority: "High", rationale: "Disciplined compounding strategy." },
          { category: "Strategic Reserve", action: `Allocate $${Math.round(budget * 0.25)}/mo into yield reserves.`, priority: "Medium", rationale: "Maintain cash-flow safety buffer." },
        ],
        country_notes: `Country rules [${country}]: Tax-efficient reinvestment active for local tax context.`,
      });
    } finally {
      setLoadingAi(false);
    }
  };

  const handleVoiceSubmit = async (queryText: string) => {
    const text = queryText || voiceQuery;
    if (!text) return;
    try {
      const res = await fetch("http://localhost:8000/api/voice/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript: text, language: "en" }),
      });
      if (res.ok) {
        const data = await res.json();
        setVoiceResponse(data);
      }
    } catch {
      setVoiceResponse({
        transcript_received: text,
        intent: "local_simulation",
        ai_response: `Voice check-in processed: "Portfolio is healthy at $50,000. Your monthly $${budget} investment target is active."`,
        suggested_action: "view_portfolio"
      });
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 font-sans selection:bg-blue-500 selection:text-white">
      {/* Top Navbar */}
      <header className="border-b border-slate-800/80 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-emerald-400 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
              C
            </div>
            <span className="font-extrabold text-xl tracking-tight text-white">CAPITAL OS</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">
              v1.1 PRO
            </span>
          </div>

          {/* Navigation Bar */}
          <nav className="flex items-center gap-1 bg-slate-950/60 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setActiveTab("overview")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === "overview" ? "bg-blue-600 text-white shadow-md shadow-blue-600/30" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Portfolio & Net Worth
            </button>
            <button
              onClick={() => setActiveTab("rebalance")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === "rebalance" ? "bg-blue-600 text-white shadow-md shadow-blue-600/30" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Rebalancer
            </button>
            <button
              onClick={() => setActiveTab("ai")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === "ai" ? "bg-blue-600 text-white shadow-md shadow-blue-600/30" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              AI Coach & Tax
            </button>
            <button
              onClick={() => setActiveTab("voice")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === "voice" ? "bg-blue-600 text-white shadow-md shadow-blue-600/30" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Voice & History
            </button>
            <button
              onClick={() => setActiveTab("goals")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === "goals" ? "bg-blue-600 text-white shadow-md shadow-blue-600/30" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Goals
            </button>
          </nav>

          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <div className="text-[10px] uppercase tracking-wider text-slate-400">Total Capital</div>
              <div className="text-sm font-extrabold text-emerald-400">$50,000.00</div>
            </div>
            <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-semibold text-slate-300">
              PRO
            </div>
          </div>
        </div>
      </header>

      {/* Main Layout Container */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* OVERVIEW TAB */}
        {activeTab === "overview" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur">
                <div className="text-xs text-slate-400 font-medium">Total Net Worth</div>
                <div className="text-3xl font-extrabold text-white mt-1">$50,000</div>
                <div className="text-xs text-emerald-400 mt-2 font-medium flex items-center gap-1">
                  <span>+14.2%</span> <span className="text-slate-500">all time</span>
                </div>
              </div>

              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur">
                <div className="text-xs text-slate-400 font-medium">Monthly Investment Target</div>
                <div className="text-3xl font-extrabold text-blue-400 mt-1">${budget}</div>
                <div className="text-xs text-slate-400 mt-2">Active Jurisdiction: <span className="text-white font-medium">{country}</span></div>
              </div>

              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur">
                <div className="text-xs text-slate-400 font-medium">Risk Allocation Profile</div>
                <div className="text-3xl font-extrabold text-indigo-400 mt-1 capitalize">{risk}</div>
                <div className="text-xs text-slate-400 mt-2">Risk Score: <span className="text-white font-medium">55 / 100</span></div>
              </div>

              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur">
                <div className="text-xs text-slate-400 font-medium">Financial Freedom 2030</div>
                <div className="text-3xl font-extrabold text-emerald-400 mt-1">$500,000</div>
                <div className="w-full bg-slate-800 h-2 rounded-full mt-3 overflow-hidden">
                  <div className="bg-gradient-to-r from-blue-500 to-emerald-400 h-full w-[10%]" />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl">
                <h3 className="text-lg font-bold text-white mb-4">Asset Breakdown & Holdings</h3>
                <div className="divide-y divide-slate-800">
                  {assets.map((asset) => (
                    <div key={asset.symbol} className="py-3.5 flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center justify-center font-bold text-blue-400">
                          {asset.symbol.slice(0, 3)}
                        </div>
                        <div>
                          <div className="font-semibold text-white">{asset.name}</div>
                          <div className="text-xs text-slate-400">{asset.type} • {asset.symbol}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-white">${asset.value.toLocaleString()}</div>
                        <div className="text-xs text-blue-400">{asset.allocation}% of portfolio</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
                <div>
                  <h3 className="text-lg font-bold text-white mb-2">AI Wealth Health Summary</h3>
                  <p className="text-sm text-slate-300 leading-relaxed mt-2">
                    {aiResult?.summary}
                  </p>
                </div>
                <button
                  onClick={() => setActiveTab("rebalance")}
                  className="w-full mt-6 py-3 px-4 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 font-semibold text-white shadow-lg shadow-blue-600/30 hover:brightness-110 transition text-center"
                >
                  Calculate Rebalance →
                </button>
              </div>
            </div>
          </div>
        )}

        {/* REBALANCER TAB */}
        {activeTab === "rebalance" && (
          <div className="space-y-6">
            <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl">
              <h2 className="text-2xl font-bold text-white mb-1">Tax-Efficient Buy-Only Rebalancer</h2>
              <p className="text-sm text-slate-400">Calculates exact monthly buy orders to keep your portfolio balanced without triggering capital gains taxes.</p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Monthly Deposit ($)</label>
                  <input
                    type="number"
                    value={budget}
                    onChange={(e) => setBudget(Number(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 font-medium"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Target Strategy</label>
                  <select
                    value={risk}
                    onChange={(e) => setRisk(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 font-medium"
                  >
                    <option value="conservative">Conservative (40% ETF, 40% Bond, 15% Yield, 5% Crypto)</option>
                    <option value="moderate">Moderate (70% ETF, 10% Bond, 10% Yield, 10% Crypto)</option>
                    <option value="aggressive">Aggressive (65% ETF, 5% Yield, 30% Crypto)</option>
                  </select>
                </div>
                <div className="flex items-end">
                  <button
                    onClick={handleCalculateRebalance}
                    disabled={loadingRebalance}
                    className="w-full py-2.5 px-4 rounded-xl bg-blue-600 font-semibold text-white hover:bg-blue-500 transition shadow-lg shadow-blue-600/30 disabled:opacity-50"
                  >
                    {loadingRebalance ? "Calculating..." : "Calculate Buy Orders"}
                  </button>
                </div>
              </div>
            </div>

            {rebalanceData && (
              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
                <div className="flex justify-between items-center pb-4 border-b border-slate-800">
                  <div>
                    <div className="text-xs uppercase tracking-wider font-bold text-blue-400">Monthly Allocation Plan</div>
                    <div className="text-2xl font-bold text-white mt-0.5">Projected Portfolio: ${rebalanceData.projected_total_value.toLocaleString()}</div>
                  </div>
                  <div className="text-right">
                    <span className="text-xs px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
                      Risk Score: {rebalanceData.risk_score} / 100
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {rebalanceData.buy_allocations.map((alloc, i) => (
                    <div key={i} className="bg-slate-950/80 border border-slate-800 rounded-xl p-5">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-bold text-white text-lg">{alloc.asset_type}</span>
                        <span className="text-xs font-bold text-blue-400">{alloc.percentage_of_budget}% of deposit</span>
                      </div>
                      <div className="text-3xl font-extrabold text-emerald-400">${alloc.recommended_buy_amount.toLocaleString()}</div>
                      <div className="text-xs text-slate-400 mt-2 leading-relaxed">{alloc.action}</div>
                    </div>
                  ))}
                </div>

                <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-800/40 text-xs text-emerald-300">
                  <span className="font-bold text-emerald-200">🛡️ Tax-Efficient Guarantee: </span>
                  {rebalanceData.tax_efficient_note}
                </div>
              </div>
            )}
          </div>
        )}

        {/* AI & TAX TAB */}
        {activeTab === "ai" && (
          <div className="space-y-6">
            <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl">
              <h2 className="text-2xl font-bold text-white mb-1">Explainable AI & Country Tax Module</h2>
              <p className="text-sm text-slate-400">Select your country of tax residence to load localized investment rules and broker guidance.</p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Tax Residency Country</label>
                  <select
                    value={country}
                    onChange={(e) => setCountry(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 font-medium"
                  >
                    <option value="UA">Ukraine (UA) — 9% Div + 1.5% Military Tax</option>
                    <option value="US">United States (US) — 15% Cap Gains / Roth IRA</option>
                    <option value="DE">Germany (DE) — 25% Abgeltungsteuer + Soli</option>
                    <option value="UK">United Kingdom (UK) — £20,000 Tax-Free ISA</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Risk Profile</label>
                  <select
                    value={risk}
                    onChange={(e) => setRisk(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 font-medium"
                  >
                    <option value="conservative">Conservative</option>
                    <option value="moderate">Moderate</option>
                    <option value="aggressive">Aggressive</option>
                  </select>
                </div>
                <div className="flex items-end">
                  <button
                    onClick={handleGenerateAdvice}
                    disabled={loadingAi}
                    className="w-full py-2.5 px-4 rounded-xl bg-blue-600 font-semibold text-white hover:bg-blue-500 transition shadow-lg shadow-blue-600/30 disabled:opacity-50"
                  >
                    {loadingAi ? "Analyzing..." : "Generate AI Advice"}
                  </button>
                </div>
              </div>
            </div>

            {aiResult && (
              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
                <div>
                  <div className="text-xs uppercase tracking-wider font-bold text-blue-400">Localized Strategy Overview</div>
                  <div className="text-xl font-bold text-white mt-1">{aiResult.summary}</div>
                  <div className="text-sm text-indigo-300 mt-1 font-medium">{aiResult.risk_assessment}</div>
                </div>

                <div>
                  <div className="text-sm font-bold text-slate-300 mb-3">Actionable Investment Directives</div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {aiResult.recommended_actions.map((rec, i) => (
                      <div key={i} className="bg-slate-950/80 border border-slate-800 rounded-xl p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
                            {rec.category}
                          </span>
                          <span className="text-xs font-bold text-amber-400">{rec.priority} Priority</span>
                        </div>
                        <div className="font-semibold text-white text-base">{rec.action}</div>
                        <div className="text-xs text-slate-400 mt-2 leading-relaxed">{rec.rationale}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-blue-950/30 border border-blue-800/40 text-xs text-blue-300">
                  <span className="font-bold text-blue-200">Legal & Country Tax Context ({country}): </span>
                  {aiResult.country_notes}
                </div>
              </div>
            )}
          </div>
        )}

        {/* VOICE & TRANSACTIONS TAB */}
        {activeTab === "voice" && (
          <div className="space-y-6">
            <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl">
              <h2 className="text-2xl font-bold text-white mb-1">Voice Assistant & Transactions Log</h2>
              <p className="text-sm text-slate-400">Ask questions by speech/text or inspect recent capital transactions.</p>

              <div className="mt-6 flex gap-3">
                <input
                  type="text"
                  placeholder="e.g. 'How much should I buy this month?' or 'Check my portfolio tax status'"
                  value={voiceQuery}
                  onChange={(e) => setVoiceQuery(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleVoiceSubmit(voiceQuery)}
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 font-medium text-sm"
                />
                <button
                  onClick={() => handleVoiceSubmit(voiceQuery)}
                  className="py-3 px-6 rounded-xl bg-blue-600 font-semibold text-white hover:bg-blue-500 transition shadow-lg shadow-blue-600/30"
                >
                  Ask Assistant
                </button>
              </div>

              <div className="flex gap-2 mt-3">
                <button
                  onClick={() => handleVoiceSubmit("How should I rebalance my portfolio?")}
                  className="text-xs px-3 py-1.5 rounded-lg bg-slate-800/80 text-slate-300 hover:text-white border border-slate-700 transition"
                >
                  💡 "How to rebalance?"
                </button>
                <button
                  onClick={() => handleVoiceSubmit("What is my current net worth?")}
                  className="text-xs px-3 py-1.5 rounded-lg bg-slate-800/80 text-slate-300 hover:text-white border border-slate-700 transition"
                >
                  💡 "What is my net worth?"
                </button>
              </div>

              {voiceResponse && (
                <div className="mt-6 p-5 bg-slate-950/90 border border-blue-500/30 rounded-xl space-y-2">
                  <div className="text-xs font-bold text-blue-400 uppercase tracking-wider">Voice Assistant Reply</div>
                  <div className="text-base font-semibold text-white">{voiceResponse.ai_response}</div>
                  <div className="text-xs text-slate-400">Intent Detected: <span className="font-mono text-indigo-300">{voiceResponse.intent}</span></div>
                </div>
              )}
            </div>

            {/* Transactions Log */}
            <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl">
              <h3 className="text-lg font-bold text-white mb-4">Recent Transaction History</h3>
              <div className="divide-y divide-slate-800">
                {transactions.map((tx) => (
                  <div key={tx.id} className="py-3.5 flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-white uppercase text-sm tracking-wide">{tx.type} • {tx.symbol}</div>
                      <div className="text-xs text-slate-400">{tx.date}</div>
                    </div>
                    <div className="font-bold text-emerald-400">${tx.amount.toFixed(2)}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* GOALS TAB */}
        {activeTab === "goals" && (
          <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-white">Long-Term Wealth Goals</h2>
              <p className="text-sm text-slate-400">Track milestones and maintain monthly investing habits.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-5">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-bold text-lg text-white">Financial Freedom 2030</h4>
                    <p className="text-xs text-slate-400 mt-0.5">Target: $500,000.00 by Dec 2030</p>
                  </div>
                  <span className="text-xs font-bold text-emerald-400 bg-emerald-950/50 px-2.5 py-1 rounded-lg border border-emerald-800/40">
                    On Track
                  </span>
                </div>

                <div className="mt-4">
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>Progress ($50,000 / $500,000)</span>
                    <span className="font-bold text-white">10%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                    <div className="bg-gradient-to-r from-blue-500 to-emerald-400 h-full w-[10%]" />
                  </div>
                </div>
              </div>

              <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-5">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-bold text-lg text-white">6-Month Emergency Buffer</h4>
                    <p className="text-xs text-slate-400 mt-0.5">Target: $12,000.00 cash reserve</p>
                  </div>
                  <span className="text-xs font-bold text-blue-400 bg-blue-950/50 px-2.5 py-1 rounded-lg border border-blue-800/40">
                    Completed (100%)
                  </span>
                </div>

                <div className="mt-4">
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>Progress ($12,000 / $12,000)</span>
                    <span className="font-bold text-emerald-400">100%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                    <div className="bg-emerald-400 h-full w-full" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
