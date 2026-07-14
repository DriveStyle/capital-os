export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[radial-gradient(circle_at_top,_rgba(59,130,246,0.25),_transparent_55%)] px-6">
      <section className="w-full max-w-5xl rounded-3xl border border-slate-800 bg-slate-900/70 p-10 shadow-2xl shadow-blue-950/30 backdrop-blur">
        <p className="mb-4 text-sm font-semibold uppercase tracking-[0.3em] text-blue-400">Capital OS</p>
        <h1 className="text-4xl font-semibold text-white sm:text-6xl">
          AI-powered wealth operating system for long-term builders.
        </h1>
        <p className="mt-6 max-w-3xl text-lg text-slate-300">
          Build disciplined portfolios, receive explainable AI guidance, and manage your financial plan from a single modern platform.
        </p>
        <div className="mt-10 flex flex-wrap gap-4">
          <a href="/" className="rounded-full bg-blue-500 px-6 py-3 font-medium text-white transition hover:bg-blue-400">
            Explore the platform
          </a>
          <a href="https://github.com" className="rounded-full border border-slate-700 px-6 py-3 font-medium text-slate-200 transition hover:border-slate-500">
            View roadmap
          </a>
        </div>
      </section>
    </main>
  );
}
