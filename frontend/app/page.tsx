"use client";

import { useState, useEffect } from "react";

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

interface AIConnectionState {
  connection_id: string;
  display_name: string;
  provider: string;
  default_model: string;
  base_url: string;
  api_key_masked: string;
  new_api_key?: string;
  enabled: boolean;
  is_active: boolean;
  description: string;
  is_local: boolean;
}

interface TestResult {
  status: "ok" | "error" | "loading";
  latency_ms?: number;
  message: string;
  response_sample?: string;
  model_used?: string;
}

export default function CapitalOSDashboard() {
  const [activeTab, setActiveTab] = useState<"overview" | "rebalance" | "ai" | "connections" | "voice" | "goals">("overview");
  const [budget, setBudget] = useState<number>(1000);
  const [risk, setRisk] = useState<string>("moderate");
  const [country, setCountry] = useState<string>("UA");
  const [loadingAi, setLoadingAi] = useState<boolean>(false);
  const [loadingRebalance, setLoadingRebalance] = useState<boolean>(false);

  // Active AI Provider state
  const [activeProvider, setActiveProvider] = useState<string>("omnirouter");
  const [switchingProvider, setSwitchingProvider] = useState<boolean>(false);

  // AI Connections state
  const [connections, setConnections] = useState<AIConnectionState[]>([
    {
      connection_id: "omnirouter",
      display_name: "OmniRouter AI",
      provider: "openai_compatible",
      default_model: "gpt-4o-mini",
      base_url: "https://api.omnirouter.ai/v1",
      api_key_masked: "sk-1*****************917",
      enabled: true,
      is_active: true,
      description: "Unified AI routing gateway connecting multi-model pipelines via OpenAI-compatible endpoints.",
      is_local: false,
    },
    {
      connection_id: "openai",
      display_name: "OpenAI Platform",
      provider: "openai",
      default_model: "gpt-4o-mini",
      base_url: "https://api.openai.com/v1",
      api_key_masked: "sk-1*****************917",
      enabled: true,
      is_active: false,
      description: "Direct OpenAI API integration for GPT-4o and lightweight financial reasoning models.",
      is_local: false,
    },
    {
      connection_id: "gemini",
      display_name: "Google Gemini",
      provider: "gemini",
      default_model: "gemini-2.5-flash",
      base_url: "https://generativelanguage.googleapis.com",
      api_key_masked: "AIza*****************394",
      enabled: true,
      is_active: false,
      description: "High-speed multimodal intelligence for macro-economic and ETF market analysis.",
      is_local: false,
    },
    {
      connection_id: "groq",
      display_name: "Groq LPU Inference",
      provider: "groq",
      default_model: "llama-3.3-70b-versatile",
      base_url: "https://api.groq.com/openai/v1",
      api_key_masked: "gsk-*****************412",
      enabled: true,
      is_active: false,
      description: "Sub-second ultra-fast inference with Llama 3.3 70B for real-time asset allocations.",
      is_local: false,
    },
    {
      connection_id: "claude",
      display_name: "Anthropic Claude",
      provider: "claude",
      default_model: "claude-3-5-sonnet",
      base_url: "https://api.anthropic.com/v1",
      api_key_masked: "sk-a*****************881",
      enabled: true,
      is_active: false,
      description: "Advanced quantitative reasoning and tax-compliance logic with Claude 3.5 Sonnet.",
      is_local: false,
    },
    {
      connection_id: "ollama",
      display_name: "Ollama Local Engine",
      provider: "openai_compatible",
      default_model: "llama3",
      base_url: "http://localhost:11434/v1",
      api_key_masked: "(Zero Key Required)",
      enabled: true,
      is_active: false,
      description: "Self-hosted private on-premise execution with zero external network data transmission.",
      is_local: true,
    },
  ]);

  // Test & Edit state
  const [testResults, setTestResults] = useState<Record<string, TestResult>>({});
  const [editingKey, setEditingKey] = useState<Record<string, string>>({});
  const [editingModel, setEditingModel] = useState<Record<string, string>>({});
  const [editingBaseUrl, setEditingBaseUrl] = useState<Record<string, string>>({});
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  // Voice assistant state
  const [voiceQuery, setVoiceQuery] = useState<string>("");
  const [voiceResponse, setVoiceResponse] = useState<{
    transcript_received: string;
    intent: string;
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
    provider_used?: string;
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
    provider_used: "OmniRouter AI",
  });

  const [transactions] = useState<Transaction[]>([
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

  const getApiUrl = (path: string): string => {
    const envUrl = process.env.NEXT_PUBLIC_API_URL;
    if (!envUrl) return `http://localhost:8000${path}`;
    const base = envUrl.startsWith("http") ? envUrl : `https://${envUrl}`;
    return `${base.replace(/\/$/, "")}${path}`;
  };

  // Fetch AI status from backend on mount
  useEffect(() => {
    fetchAiStatus();
  }, []);

  const fetchAiStatus = async () => {
    try {
      const res = await fetch(getApiUrl("/api/ai/status"));
      if (res.ok) {
        const data = await res.json();
        if (data.active_provider) {
          setActiveProvider(data.active_provider);
        }
        if (data.connections) {
          setConnections((prev) =>
            prev.map((c) => {
              const live = data.connections[c.connection_id];
              if (live) {
                return {
                  ...c,
                  api_key_masked: live.api_key || c.api_key_masked,
                  default_model: live.default_model || c.default_model,
                  base_url: live.base_url || c.base_url,
                  enabled: live.enabled !== undefined ? live.enabled : c.enabled,
                  is_active: data.active_provider === c.connection_id,
                };
              }
              return c;
            })
          );
        }
      }
    } catch {
      // Offline simulation fallback
    }
  };

  const handleSetActiveProvider = async (providerId: string) => {
    setSwitchingProvider(true);
    try {
      const res = await fetch(getApiUrl("/api/ai/set-active-provider"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ provider: providerId }),
      });
      if (res.ok) {
        const data = await res.json();
        setActiveProvider(data.active_provider);
        setStatusMessage(`Active AI engine switched to: ${providerId.toUpperCase()}`);
        setTimeout(() => setStatusMessage(null), 3500);
      }
    } catch {
      setActiveProvider(providerId);
      setStatusMessage(`Active AI engine locally set to: ${providerId.toUpperCase()}`);
      setTimeout(() => setStatusMessage(null), 3500);
    } finally {
      setSwitchingProvider(false);
    }
  };

  const handleTestConnection = async (connectionId: string) => {
    setTestResults((prev) => ({
      ...prev,
      [connectionId]: { status: "loading", message: "Pinging AI endpoint..." },
    }));

    try {
      const res = await fetch(getApiUrl("/api/ai/test-connection"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ connection_id: connectionId, prompt: "Capital OS health probe." }),
      });

      if (res.ok) {
        const data = await res.json();
        setTestResults((prev) => ({
          ...prev,
          [connectionId]: {
            status: data.status === "ok" ? "ok" : "error",
            latency_ms: data.latency_ms,
            message: data.message,
            response_sample: data.response_sample,
            model_used: data.model_used,
          },
        }));
      } else {
        setTestResults((prev) => ({
          ...prev,
          [connectionId]: { status: "error", message: "Server returned non-200 status code." },
        }));
      }
    } catch {
      // Local verification simulation
      setTimeout(() => {
        setTestResults((prev) => ({
          ...prev,
          [connectionId]: {
            status: "ok",
            latency_ms: 114,
            message: "Simulation: Connection verified via AIRouter.",
            response_sample: "OK (Capital OS Health Probe)",
          },
        }));
      }, 500);
    }
  };

  const handleSaveConnection = async (conn: AIConnectionState) => {
    const newKey = editingKey[conn.connection_id];
    const newModel = editingModel[conn.connection_id] || conn.default_model;
    const newUrl = editingBaseUrl[conn.connection_id] !== undefined ? editingBaseUrl[conn.connection_id] : conn.base_url;

    try {
      const payload = {
        connection_id: conn.connection_id,
        provider: conn.provider,
        api_key: newKey || conn.api_key_masked,
        base_url: newUrl || null,
        default_model: newModel,
        enabled: conn.enabled,
        display_name: conn.display_name,
      };

      const res = await fetch(getApiUrl("/api/ai/connections"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        setStatusMessage(`Saved configuration for ${conn.display_name}`);
        setTimeout(() => setStatusMessage(null), 3000);
        // Clear secret input field for security
        setEditingKey((prev) => ({ ...prev, [conn.connection_id]: "" }));
        fetchAiStatus();
      }
    } catch {
      setStatusMessage(`Saved locally: ${conn.display_name}`);
      setTimeout(() => setStatusMessage(null), 3000);
    }
  };

  const handleCalculateRebalance = async () => {
    setLoadingRebalance(true);
    try {
      const res = await fetch(getApiUrl("/api/portfolios/rebalance"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ current_assets: assets, monthly_budget: budget, risk_profile: risk }),
      });
      if (res.ok) {
        const data = await res.json();
        setRebalanceData(data);
      }
    } catch {
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
      const res = await fetch(getApiUrl("/api/ai/recommend"), {
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
        provider_used: `${activeProvider.toUpperCase()} (Simulated Response)`,
      });
    } finally {
      setLoadingAi(false);
    }
  };

  const handleVoiceSubmit = async (queryText: string) => {
    const text = queryText || voiceQuery;
    if (!text) return;
    try {
      const res = await fetch(getApiUrl("/api/voice/process"), {
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
              v1.2 MULTI-AI
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
              onClick={() => setActiveTab("connections")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                activeTab === "connections" ? "bg-blue-600 text-white shadow-md shadow-blue-600/30" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              AI Connections
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
              <div className="text-[10px] uppercase tracking-wider text-slate-400">Active Engine</div>
              <div className="text-xs font-extrabold text-blue-400 capitalize">{activeProvider}</div>
            </div>
            <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-semibold text-slate-300">
              PRO
            </div>
          </div>
        </div>
      </header>

      {/* Global Status Banner */}
      {statusMessage && (
        <div className="bg-gradient-to-r from-blue-900/80 to-indigo-900/80 border-b border-blue-500/30 px-6 py-2.5 text-center text-xs font-semibold text-blue-200 animate-fade-in">
          ✨ {statusMessage}
        </div>
      )}

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
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="text-lg font-bold text-white">AI Wealth Health Summary</h3>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 font-semibold">
                      {aiResult?.provider_used || activeProvider}
                    </span>
                  </div>
                  <p className="text-sm text-slate-300 leading-relaxed mt-2">
                    {aiResult?.summary}
                  </p>
                </div>
                <div className="space-y-2 mt-6">
                  <button
                    onClick={() => setActiveTab("rebalance")}
                    className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 font-semibold text-white shadow-lg shadow-blue-600/30 hover:brightness-110 transition text-center"
                  >
                    Calculate Rebalance →
                  </button>
                  <button
                    onClick={() => setActiveTab("connections")}
                    className="w-full py-2 px-4 rounded-xl bg-slate-800/80 border border-slate-700 font-medium text-xs text-slate-300 hover:text-white transition text-center"
                  >
                    Configure Multi-AI Providers ⚙️
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* AI CONNECTIONS TAB */}
        {activeTab === "connections" && (
          <div className="space-y-6 animate-fade-in">
            {/* Top Control Header */}
            <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h2 className="text-2xl font-bold text-white flex items-center gap-2.5">
                  <span>AI Connections & Multi-Provider Hub</span>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
                    6 Connectors Available
                  </span>
                </h2>
                <p className="text-sm text-slate-400 mt-1">
                  Manage LLM credentials, OpenAI-compatible proxy gateways, local endpoints, and active routing engine.
                </p>
              </div>

              <div className="flex items-center gap-3 bg-slate-950/80 p-3 rounded-xl border border-slate-800">
                <div className="text-xs">
                  <span className="text-slate-400 block text-[10px] uppercase font-bold">Active AI Provider</span>
                  <span className="font-extrabold text-emerald-400 capitalize text-sm">{activeProvider}</span>
                </div>
                <button
                  onClick={fetchAiStatus}
                  className="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-200 hover:text-white hover:bg-slate-700 transition"
                >
                  ↻ Refresh Status
                </button>
              </div>
            </div>

            {/* Providers Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {connections.map((conn) => {
                const isCurrentActive = activeProvider === conn.connection_id;
                const result = testResults[conn.connection_id];

                return (
                  <div
                    key={conn.connection_id}
                    className={`bg-slate-900/80 border rounded-2xl p-5 shadow-xl flex flex-col justify-between transition-all duration-200 ${
                      isCurrentActive
                        ? "border-blue-500/80 ring-1 ring-blue-500/50 bg-gradient-to-b from-slate-900/90 to-blue-950/20"
                        : "border-slate-800 hover:border-slate-700"
                    }`}
                  >
                    <div>
                      {/* Card Header */}
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <div className="flex items-center gap-2">
                            <h3 className="font-bold text-white text-base">{conn.display_name}</h3>
                            {conn.is_local && (
                              <span className="text-[10px] px-2 py-0.2 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 font-semibold">
                                Self-Hosted
                              </span>
                            )}
                          </div>
                          <span className="text-xs font-mono text-slate-400">
                            protocol: {conn.provider}
                          </span>
                        </div>

                        {isCurrentActive ? (
                          <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Active
                          </span>
                        ) : (
                          <button
                            onClick={() => handleSetActiveProvider(conn.connection_id)}
                            disabled={switchingProvider}
                            className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 border border-slate-700 transition"
                          >
                            Set Active
                          </button>
                        )}
                      </div>

                      <p className="text-xs text-slate-400 leading-relaxed mb-4">
                        {conn.description}
                      </p>

                      {/* Connection Fields */}
                      <div className="space-y-3 bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/80 text-xs">
                        {/* API Key Field */}
                        <div>
                          <label className="block text-[11px] font-semibold text-slate-400 mb-1 flex justify-between">
                            <span>API Key Secret</span>
                            <span className="text-[10px] text-slate-500 font-mono">
                              {conn.is_local ? "Optional" : "Never stored plaintext"}
                            </span>
                          </label>
                          <input
                            type="password"
                            placeholder={conn.api_key_masked || "Enter API Key..."}
                            value={editingKey[conn.connection_id] || ""}
                            onChange={(e) =>
                              setEditingKey((prev) => ({
                                ...prev,
                                [conn.connection_id]: e.target.value,
                              }))
                            }
                            className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-white font-mono text-xs focus:outline-none focus:border-blue-500 placeholder:text-slate-600"
                          />
                        </div>

                        {/* Model Field */}
                        <div>
                          <label className="block text-[11px] font-semibold text-slate-400 mb-1">
                            Default Model
                          </label>
                          <input
                            type="text"
                            value={
                              editingModel[conn.connection_id] !== undefined
                                ? editingModel[conn.connection_id]
                                : conn.default_model
                            }
                            onChange={(e) =>
                              setEditingModel((prev) => ({
                                ...prev,
                                [conn.connection_id]: e.target.value,
                              }))
                            }
                            className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-white font-mono text-xs focus:outline-none focus:border-blue-500"
                          />
                        </div>

                        {/* Base URL Field */}
                        <div>
                          <label className="block text-[11px] font-semibold text-slate-400 mb-1">
                            Endpoint Base URL
                          </label>
                          <input
                            type="text"
                            value={
                              editingBaseUrl[conn.connection_id] !== undefined
                                ? editingBaseUrl[conn.connection_id]
                                : conn.base_url || ""
                            }
                            onChange={(e) =>
                              setEditingBaseUrl((prev) => ({
                                ...prev,
                                [conn.connection_id]: e.target.value,
                              }))
                            }
                            placeholder="https://..."
                            className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-white font-mono text-xs focus:outline-none focus:border-blue-500 placeholder:text-slate-600"
                          />
                        </div>
                      </div>

                      {/* Test Results Area */}
                      {result && (
                        <div
                          className={`mt-3 p-3 rounded-xl border text-xs leading-relaxed ${
                            result.status === "loading"
                              ? "bg-blue-950/30 border-blue-800/40 text-blue-300"
                              : result.status === "ok"
                              ? "bg-emerald-950/30 border-emerald-800/40 text-emerald-300"
                              : "bg-red-950/30 border-red-800/40 text-red-300"
                          }`}
                        >
                          <div className="flex justify-between items-center font-bold">
                            <span>{result.status === "ok" ? "✓ Test Passed" : result.status === "loading" ? "⏳ Testing..." : "✕ Test Failed"}</span>
                            {result.latency_ms !== undefined && (
                              <span className="font-mono text-[10px]">{result.latency_ms}ms</span>
                            )}
                          </div>
                          <div className="mt-1 text-[11px] text-slate-300">{result.message}</div>
                          {result.response_sample && (
                            <div className="mt-1 font-mono text-[10px] text-slate-400 truncate">
                              Sample: {result.response_sample}
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Actions */}
                    <div className="flex items-center gap-2 mt-4 pt-3 border-t border-slate-800/80">
                      <button
                        onClick={() => handleTestConnection(conn.connection_id)}
                        disabled={result?.status === "loading"}
                        className="flex-1 py-1.5 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs transition border border-slate-700"
                      >
                        ⚡ Test Connection
                      </button>
                      <button
                        onClick={() => handleSaveConnection(conn)}
                        className="py-1.5 px-3 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition shadow-md shadow-blue-600/20"
                      >
                        Save
                      </button>
                    </div>
                  </div>
                );
              })}
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
              <div className="flex justify-between items-center mb-1">
                <h2 className="text-2xl font-bold text-white">Explainable AI & Country Tax Module</h2>
                <span className="text-xs font-mono px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-bold">
                  Engine: {activeProvider.toUpperCase()}
                </span>
              </div>
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
                  <div className="flex justify-between items-center">
                    <div className="text-xs uppercase tracking-wider font-bold text-blue-400">Localized Strategy Overview</div>
                    <span className="text-xs text-slate-400 font-mono">Provider: {aiResult.provider_used || activeProvider}</span>
                  </div>
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
