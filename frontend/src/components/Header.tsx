import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="mb-6 border-b border-zinc-800/80 pb-5">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div className="mb-3 inline-flex items-center gap-2 border border-teal-500/30 bg-teal-950/20 px-3 py-1 text-xs font-semibold uppercase tracking-normal text-teal-300">
            <span className="h-2 w-2 bg-teal-400" />
            SecuIQ Operations Console
          </div>
          <h1 className="text-3xl font-semibold text-zinc-100 md:text-4xl">SOC Alert Triage</h1>
          <p className="mt-2 max-w-2xl text-sm text-zinc-400">
            Network-flow alert classification, priority scoring, and analyst review queue.
          </p>
        </div>

        <div className="border border-zinc-800 bg-zinc-950 px-4 py-3 text-sm">
          <div className="text-xs uppercase tracking-normal text-zinc-500">Updated</div>
          <div className="mt-1 font-mono text-zinc-200">Live</div>
        </div>
      </div>
    </header>
  );
};

export default Header;
