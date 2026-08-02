"use client";

import { useState } from "react";

interface Asset {
  symbol: string;
  name: string;
  allocation: number;
  value: number;
  type: string;
}

interface Recommendation {
  category: string;
  action: string;
  priority: "High" | "Medium" | "Low";
  rationale: string;
}

export default function CapitalOSDashboard() {
  const [activeTab, setActiveTab] = useState<"overview" | "ai" | "goals">("overview");
  const [budget, setBudget] = useState<number>(1000);
  const [risk, setRisk] = useState<string>("moderate");
  const [country, setCountry] = useState<string>("UA");
  const [loadingAi, setLoadingAi] = useState<boolean>(false);

  const [aiResult, setAiResult] = useState<{
    summary: string;
    risk_assessment: string;
    recommended_actions: Recommendation[];
    country_notes: string;
  } | null>({
    summary: "Balanced wealth operating strategy for UA maintaining strong capital safety and steady indexing.",
    risk_assessment: "Risk profile evaluated as [MODERATE]. Recommended investment horizon: 5+ years.",
    recommended_actions: [
      {
        category: "Broad Market Indexing",
        action: "Allocate 80% ($800/mo) into low-cost global ETFs (e.g. VWRA/S&P 500).",
        priority: "High",
        rationale: "Core wealth foundation providing broad diversification across top global equities.",
      },
      {
        category: "Opportunistic Cash Reserve",
        action: "Keep 20% ($200/mo) in reserve yield account.",
        priority: "Medium",
        rationale: "Liquidity safety buffer for market opportunities and high-yield interest.",
      },
    ],
    country_notes: "Country module [UA]: Ensure tax reporting compliance on foreign dividend income and utilize local tax-exempt investment accounts.",
  });

  const assets: Asset[] = [
    { symbol: "VWRA", name: "Vanguard FTSE All-World", allocation: 55, value: 27500, type: "ETF" },
    { symbol: "S&P 500", name: "iShares Core S&P 500", allocation: 25, value: 12500, type: "ETF" },
    { symbol: "BTC", name: "Bitcoin Reserve", allocation: 10, value: 5000, type: "Crypto" },
    { symbol: "CASH", name: "High-Yield Reserve", allocation: 10, value: 5000, type: "Yield" },
  ];

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
      // Fallback local simulation if backend server offline
      setAiResult({
        summary: `Tailored ${risk.toUpperCase()} wealth strategy for country [${country}] with $${budget}/mo allocation.`,
        risk_assessment: `Risk profile evaluated as [${risk.toUpperCase()}]. Target horizon: 5+ years.`,
        recommended_actions: [
          {
            category: "Core Allocation",
            action: `Allocate ${(budget * 0.75).toLocaleString()}/mo into broad market index ETFs.`,
            priority: "High",
            rationale: "Disciplined long-term compounding strategy.",
          },
          {
            category: "Strategic Reserve",
            action: `Allocate ${(budget * 0.25).toLocaleString()}/mo into high-yield reserves.`,
            priority: "Medium",
            rationale: "Maintain safety buffer and cash-flow agility.",
          },
        ],
        country_notes: `Country rules [${country}]: Tax-efficient dividend reinvestment active.`,
      });
    } finally {
      setLoadingAi(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 font-sans selection:bg-blue-500 selection:text-white">
      {/* Header Bar */}
      <header className="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-emerald-400 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
              C
            </div>
            <span className="font-bold text-xl tracking-tight text-white">CAPITAL OS</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">
              v1.0 MVP
            </span>
          </div>

          <nav className="flex items-center gap-1 bg-slate-950/50 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setActiveTab("overview")}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition ${
                activeTab === "overview"
                  ? "bg-blue-600 text-white shadow-md shadow-blue-600/30"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Portfolio & Net Worth
            </button>
            <button
              onClick={() => setActiveTab("ai")}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition ${
                activeTab === "ai"
                  ? "bg-blue-600 text-white shadow-md shadow-blue-600/30"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              AI Wealth Coach
            </button>
            <button
              onClick={() => setActiveTab("goals")}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition ${
                activeTab === "goals"
                  ? "bg-blue-600 text-white shadow-md shadow-blue-600/30"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Goals & Habits
            </button>
          </nav>

          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <div className="text-xs text-slate-400">Total Net Worth</div>
              <div className="text-sm font-bold text-emerald-400">$50,000.00</div>
            </div>
            <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-semibold text-slate-300">
              PRO
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* OVERVIEW TAB */}
        {activeTab === "overview" && (
          <div className="space-y-6">
            {/* Top KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur">
                <div className="text-xs text-slate-400 font-medium">Total Portfolio Value</div>
                <div className="text-3xl font-extrabold text-white mt-1">$50,000</div>
                <div className="text-xs text-emerald-400 mt-2 font-medium flex items-center gap-1">
                  <span>+14.2%</span> <span className="text-slate-500">all time</span>
                </div>
              </div>

              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur">
                <div className="text-xs text-slate-400 font-medium">Monthly Investment Target</div>
                <div className="text-3xl font-extrabold text-blue-400 mt-1">${budget}</div>
                <div className="text-xs text-slate-400 mt-2">Country Context: <span className="text-white font-medium">{country}</span></div>
              </div>

              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur">
                <div className="text-xs text-slate-400 font-medium">Risk Allocation Profile</div>
                <div className="text-3xl font-extrabold text-indigo-400 mt-1 capitalize">{risk}</div>
                <div className="text-xs text-slate-400 mt-2">Target Horizon: <span className="text-white font-medium">5-10 Yrs</span></div>
              </div>

              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-xl backdrop-blur">
                <div className="text-xs text-slate-400 font-medium">Financial Freedom Goal</div>
                <div className="text-3xl font-extrabold text-emerald-400 mt-1">$500,000</div>
                <div className="w-full bg-slate-800 h-2 rounded-full mt-3 overflow-hidden">
                  <div className="bg-gradient-to-r from-blue-500 to-emerald-400 h-full w-[10%]" />
                </div>
              </div>
            </div>

            {/* Asset Allocation Breakdown */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl">
                <h3 className="text-lg font-bold text-white mb-4">Current Asset Breakdown</h3>
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
                  <h3 className="text-lg font-bold text-white mb-2">AI Wealth Health Check</h3>
                  <p className="text-sm text-slate-300 leading-relaxed mt-2">
                    {aiResult?.summary}
                  </p>
                </div>
                <button
                  onClick={() => setActiveTab("ai")}
                  className="w-full mt-6 py-3 px-4 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 font-semibold text-white shadow-lg shadow-blue-600/30 hover:brightness-110 transition text-center"
                >
                  Consult AI Wealth Coach →
                </button>
              </div>
            </div>
          </div>
        )}

        {/* AI WEALTH COACH TAB */}
        {activeTab === "ai" && (
          <div className="space-y-6">
            <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl">
              <h2 className="text-2xl font-bold text-white mb-1">Explainable AI Wealth Assistant</h2>
              <p className="text-sm text-slate-400">Configure your monthly budget and risk tolerance to generate AI investment strategies.</p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Monthly Investment ($)</label>
                  <input
                    type="number"
                    value={budget}
                    onChange={(e) => setBudget(Number(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 font-medium"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Risk Profile</label>
                  <select
                    value={risk}
                    onChange={(e) => setRisk(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 font-medium"
                  >
                    <option value="conservative">Conservative (Preservation & Yield)</option>
                    <option value="moderate">Moderate (Balanced Indexing)</option>
                    <option value="aggressive">Aggressive (High Capital Growth)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">Country Jurisdiction</label>
                  <select
                    value={country}
                    onChange={(e) => setCountry(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-blue-500 font-medium"
                  >
                    <option value="UA">Ukraine (UA)</option>
                    <option value="US">United States (US)</option>
                    <option value="DE">Germany (DE)</option>
                    <option value="UK">United Kingdom (UK)</option>
                  </select>
                </div>
              </div>

              <button
                onClick={handleGenerateAdvice}
                disabled={loadingAi}
                className="mt-5 py-3 px-6 rounded-xl bg-blue-600 font-semibold text-white hover:bg-blue-500 transition shadow-lg shadow-blue-600/30 disabled:opacity-50"
              >
                {loadingAi ? "Analyzing Portfolio & Risk..." : "Generate AI Recommendation"}
              </button>
            </div>

            {aiResult && (
              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
                <div>
                  <div className="text-xs uppercase tracking-wider font-bold text-blue-400">AI Strategy Overview</div>
                  <div className="text-xl font-bold text-white mt-1">{aiResult.summary}</div>
                  <div className="text-sm text-indigo-300 mt-1 font-medium">{aiResult.risk_assessment}</div>
                </div>

                <div>
                  <div className="text-sm font-bold text-slate-300 mb-3">Recommended Actions</div>
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
                  <span className="font-bold text-blue-200">Legal & Country Compliance: </span>
                  {aiResult.country_notes}
                </div>
              </div>
            )}
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
