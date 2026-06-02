// src/components/StatsCards.tsx
import React from 'react';
import type { StatsCardsProps } from '../types';

interface CardConfig {
  title: string;
  value: string | number;
  code: string;
  accent: string;
  valueColor: string;
  description: string;
}

const StatsCards: React.FC<StatsCardsProps> = ({ stats }) => {
  const cards: CardConfig[] = [
    { title: 'Processed Alerts', value: stats.totalAlerts, code: 'ALL', accent: 'border-l-teal-400', valueColor: 'text-teal-200', description: 'Total records classified' },
    { title: 'Critical Queue', value: stats.critical, code: 'P1', accent: 'border-l-red-500', valueColor: 'text-red-300', description: 'Immediate escalation' },
    { title: 'High Queue', value: stats.high, code: 'P2', accent: 'border-l-amber-500', valueColor: 'text-amber-300', description: 'Prompt analyst review' },
    { title: 'Medium Queue', value: stats.medium, code: 'P3', accent: 'border-l-yellow-500', valueColor: 'text-yellow-200', description: 'Correlation candidate' },
    { title: 'Low Queue', value: stats.low, code: 'P4', accent: 'border-l-sky-500', valueColor: 'text-sky-300', description: 'Trend monitoring' },
    { title: 'Top Source', value: stats.topThreatIp, code: 'SRC', accent: 'border-l-violet-500', valueColor: 'text-violet-300', description: 'Most frequent origin' },
  ];

  return (
    <section className="mb-7 grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-6">
      {cards.map((card) => (
        <article key={card.title} className={['border border-zinc-800 border-l-4 bg-zinc-950/90 p-4 shadow-[0_18px_50px_rgba(0,0,0,0.22)]', card.accent].join(' ')}>
          <div className="mb-4 flex items-center justify-between gap-3">
            <p className="text-xs font-semibold uppercase tracking-normal text-zinc-500">{card.title}</p>
            <span className="border border-zinc-700 bg-zinc-900 px-2 py-0.5 font-mono text-[11px] text-zinc-400">{card.code}</span>
          </div>
          <p className={['truncate text-2xl font-semibold', card.valueColor].join(' ')} title={String(card.value)}>{card.value}</p>
          <p className="mt-2 text-xs text-zinc-500">{card.description}</p>
        </article>
      ))}
    </section>
  );
};

export default StatsCards;
