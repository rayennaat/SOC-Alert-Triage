// src/components/AlertTable.tsx
import React, { useMemo, useState } from 'react';
import type { Alert, AlertTableProps } from '../types';
import PriorityBadge from './PriorityBadge';

type SortColumn = 'id' | 'timestamp' | 'alertType' | 'aiPriority' | 'confidence';
type SortDirection = 'asc' | 'desc';
type FilterPriority = 'ALL' | 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';

const priorityFilters: FilterPriority[] = ['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'];

const recommendationsByPriority: Record<Alert['aiPriority'], string[]> = {
  CRITICAL: [
    'Escalate immediately to the incident response owner.',
    'Validate affected source and destination hosts.',
    'Consider isolating impacted systems while evidence is preserved.',
  ],
  HIGH: [
    'Investigate within the next operational window.',
    'Check related alerts from the same source IP.',
    'Review authentication, firewall, and endpoint logs for correlation.',
  ],
  MEDIUM: [
    'Queue for analyst review and correlation.',
    'Monitor for repeated activity from the same source.',
    'Tune detection thresholds if this pattern is expected traffic.',
  ],
  LOW: [
    'Keep for trend analysis and daily review.',
    'Correlate with future alerts before escalation.',
    'Document if the activity matches a known benign pattern.',
  ],
};

const AlertTable: React.FC<AlertTableProps> = ({ alerts }) => {
  const [sortColumn, setSortColumn] = useState<SortColumn>('aiPriority');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');
  const [filterPriority, setFilterPriority] = useState<FilterPriority>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);

  const handleSort = (column: SortColumn) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('desc');
    }
  };

  const sortedAndFilteredAlerts = useMemo(() => {
    const normalizedQuery = searchQuery.trim().toLowerCase();
    const priorityOrder: Record<string, number> = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };

    return alerts
      .filter((alert) => filterPriority === 'ALL' || alert.aiPriority === filterPriority)
      .filter((alert) => {
        if (!normalizedQuery) return true;
        return [
          alert.alertId,
          alert.sourceIp,
          alert.destinationIp,
          alert.alertType,
          alert.description,
          alert.aiPriority,
        ]
          .filter(Boolean)
          .some((value) => String(value).toLowerCase().includes(normalizedQuery));
      })
      .sort((a, b) => {
        let aValue: string | number = a[sortColumn] as string | number;
        let bValue: string | number = b[sortColumn] as string | number;

        if (sortColumn === 'aiPriority') {
          aValue = priorityOrder[a.aiPriority] ?? 4;
          bValue = priorityOrder[b.aiPriority] ?? 4;
        }

        if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1;
        if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1;
        return 0;
      });
  }, [alerts, filterPriority, searchQuery, sortColumn, sortDirection]);

  const priorityCounts = useMemo(() => {
    return alerts.reduce<Record<FilterPriority, number>>(
      (counts, alert) => {
        counts.ALL += 1;
        counts[alert.aiPriority] += 1;
        return counts;
      },
      { ALL: 0, CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 }
    );
  }, [alerts]);

  const getSortIcon = (column: SortColumn): string => {
    if (sortColumn !== column) return '↕';
    return sortDirection === 'asc' ? '↑' : '↓';
  };

  const getRowColor = (priority: Alert['aiPriority']): string => {
    switch(priority) {
      case 'CRITICAL': return 'bg-red-950/20 hover:bg-red-900/30';
      case 'HIGH': return 'bg-orange-950/20 hover:bg-orange-900/30';
      case 'MEDIUM': return 'bg-yellow-950/20 hover:bg-yellow-900/30';
      case 'LOW': return 'bg-sky-950/15 hover:bg-sky-950/35';
      default: return 'hover:bg-zinc-900';
    }
  };

  const exportIncidentReport = () => {
    const generatedAt = new Date().toLocaleString();
    const summary = sortedAndFilteredAlerts.reduce<Record<Alert['aiPriority'], number>>(
      (counts, alert) => {
        counts[alert.aiPriority] += 1;
        return counts;
      },
      { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 }
    );

    const rows = sortedAndFilteredAlerts.map((alert) => `
      <tr>
        <td>#${alert.id}</td>
        <td>${alert.timestamp}</td>
        <td>${alert.sourceIp}</td>
        <td>${alert.destinationIp}</td>
        <td>${alert.alertType}</td>
        <td>${alert.aiPriority}</td>
        <td>${alert.confidence}%</td>
        <td>${alert.priorityScore ?? 'N/A'}</td>
      </tr>
    `).join('');

    const reportHtml = `<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>SOC Incident Triage Report</title>
  <style>
    body { font-family: Arial, sans-serif; color: #111827; margin: 32px; }
    h1 { margin-bottom: 4px; }
    .muted { color: #6b7280; }
    .cards { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin: 24px 0; }
    .card { border: 1px solid #d1d5db; border-radius: 8px; padding: 12px; }
    .label { color: #6b7280; font-size: 12px; text-transform: uppercase; }
    .value { font-size: 24px; font-weight: 700; margin-top: 4px; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 13px; }
    th, td { border: 1px solid #d1d5db; padding: 8px; text-align: left; }
    th { background: #f3f4f6; }
  </style>
</head>
<body>
  <h1>SOC Incident Triage Report</h1>
  <div class="muted">Generated ${generatedAt}</div>
  <div class="muted">Filter: ${filterPriority}; Search: ${searchQuery || 'None'}</div>
  <section class="cards">
    <div class="card"><div class="label">Total</div><div class="value">${sortedAndFilteredAlerts.length}</div></div>
    <div class="card"><div class="label">Critical</div><div class="value">${summary.CRITICAL}</div></div>
    <div class="card"><div class="label">High</div><div class="value">${summary.HIGH}</div></div>
    <div class="card"><div class="label">Medium</div><div class="value">${summary.MEDIUM}</div></div>
    <div class="card"><div class="label">Low</div><div class="value">${summary.LOW}</div></div>
  </section>
  <h2>Prioritized Alerts</h2>
  <table>
    <thead>
      <tr><th>Rank</th><th>Timestamp</th><th>Source IP</th><th>Destination IP</th><th>Attack Type</th><th>Priority</th><th>Confidence</th><th>Priority Score</th></tr>
    </thead>
    <tbody>${rows || '<tr><td colspan="8">No alerts matched the current filters.</td></tr>'}</tbody>
  </table>
</body>
</html>`;

    const blob = new Blob([reportHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `soc-incident-report-${new Date().toISOString().slice(0, 10)}.html`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="relative border border-zinc-800 bg-zinc-950/80 shadow-[0_18px_50px_rgba(0,0,0,0.25)] overflow-hidden">
      <div className="p-6 border-b border-zinc-800">
        <div className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
          <div>
            <h3 className="text-xl font-bold text-white">AI-Prioritized Alerts</h3>
            <p className="text-zinc-400 text-sm">
              ML-classified threats based on network traffic analysis
            </p>
          </div>

          <div className="flex flex-col gap-3 lg:min-w-[620px]">
            <div className="flex flex-col gap-3 sm:flex-row">
              <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search IP, attack type, priority, alert ID..."
                className="min-w-0 flex-1 rounded-md border border-zinc-700 bg-black/40 px-3 py-2 text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
              <button
                onClick={exportIncidentReport}
                className="rounded-md bg-teal-700 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-teal-600"
              >
                Export Report
              </button>
            </div>

            <div className="flex flex-wrap gap-2">
              {priorityFilters.map((priority) => (
                <button
                  key={priority}
                  onClick={() => setFilterPriority(priority)}
                  className={`rounded-md border px-3 py-1.5 text-sm transition-colors ${
                    filterPriority === priority
                      ? 'border-teal-500 bg-teal-500/15 text-teal-200'
                      : 'border-zinc-700 bg-zinc-900 text-zinc-300 hover:border-zinc-500'
                  }`}
                >
                  {priority === 'ALL' ? 'All' : priority} ({priorityCounts[priority]})
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="max-h-[860px] overflow-auto">
        <table className="w-full min-w-[980px]">
          <thead className="sticky top-0 z-10 bg-zinc-950">
            <tr>
              <th className="text-left py-4 px-6 text-zinc-400 font-semibold text-sm cursor-pointer hover:text-zinc-300" onClick={() => handleSort('id')}>
                <div className="flex items-center">Rank {getSortIcon('id')}</div>
              </th>
              <th className="text-left py-4 px-6 text-zinc-400 font-semibold text-sm cursor-pointer hover:text-zinc-300" onClick={() => handleSort('timestamp')}>
                <div className="flex items-center">Timestamp {getSortIcon('timestamp')}</div>
              </th>
              <th className="text-left py-4 px-6 text-zinc-400 font-semibold text-sm">Source IP</th>
              <th className="text-left py-4 px-6 text-zinc-400 font-semibold text-sm">Destination IP</th>
              <th className="text-left py-4 px-6 text-zinc-400 font-semibold text-sm cursor-pointer hover:text-zinc-300" onClick={() => handleSort('alertType')}>
                <div className="flex items-center">Attack Type {getSortIcon('alertType')}</div>
              </th>
              <th className="text-left py-4 px-6 text-zinc-400 font-semibold text-sm cursor-pointer hover:text-zinc-300" onClick={() => handleSort('aiPriority')}>
                <div className="flex items-center text-amber-300">AI Priority {getSortIcon('aiPriority')}</div>
              </th>
              <th className="text-left py-4 px-6 text-zinc-400 font-semibold text-sm cursor-pointer hover:text-zinc-300" onClick={() => handleSort('confidence')}>
                <div className="flex items-center">Confidence {getSortIcon('confidence')}</div>
              </th>
            </tr>
          </thead>
          <tbody>
            {sortedAndFilteredAlerts.length > 0 ? (
              sortedAndFilteredAlerts.map((alert) => (
                <tr
                  key={`${alert.alertId ?? alert.id}-${alert.sourceIp}-${alert.destinationIp}`}
                  onClick={() => setSelectedAlert(alert)}
                  className={`cursor-pointer border-b border-zinc-800/50 transition-colors ${getRowColor(alert.aiPriority)}`}
                >
                  <td className="py-4 px-6 text-zinc-300 font-mono text-sm">#{alert.id}</td>
                  <td className="py-4 px-6">
                    <div className="text-zinc-300 text-sm">{alert.timestamp.split(' ')[0]}</div>
                    <div className="text-zinc-500 text-xs">{alert.timestamp.split(' ')[1]}</div>
                  </td>
                  <td className="py-4 px-6"><div className="text-teal-300 font-mono text-sm">{alert.sourceIp}</div></td>
                  <td className="py-4 px-6"><div className="text-emerald-300 font-mono text-sm">{alert.destinationIp}</div></td>
                  <td className="py-4 px-6">
                    <span className="text-zinc-300 font-medium">{alert.alertType}</span>
                    {alert.count > 1 && <span className="ml-2 bg-zinc-900 text-zinc-400 text-xs px-2 py-1 rounded-sm">{alert.count}x</span>}
                  </td>
                  <td className="py-4 px-6"><PriorityBadge priority={alert.aiPriority} /></td>
                  <td className="py-4 px-6">
                    <div className="flex items-center">
                      <div className="w-16 bg-zinc-900 rounded-sm h-2 mr-3 overflow-hidden">
                        <div className="h-full bg-gradient-to-r from-teal-400 to-amber-300 rounded-sm transition-all duration-300" style={{ width: `${alert.confidence}%` }} />
                      </div>
                      <span className={`font-semibold text-sm ${alert.confidence > 90 ? 'text-emerald-300' : alert.confidence > 75 ? 'text-amber-300' : 'text-amber-400'}`}>
                        {alert.confidence}%
                      </span>
                    </div>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={7} className="py-12 text-center text-zinc-500">No alerts match the selected filters</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="p-4 border-t border-zinc-800 bg-zinc-950/70">
        <div className="flex flex-col gap-3 text-sm text-zinc-400 md:flex-row md:items-center md:justify-between">
          <div>
            Showing {sortedAndFilteredAlerts.length} of {alerts.length} alerts
            {filterPriority !== 'ALL' && ` filtered by ${filterPriority}`}
            {searchQuery && ` matching "${searchQuery}"`}
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <span className="flex items-center"><div className="w-3 h-3 bg-red-500 rounded-sm mr-1.5" />Critical</span>
            <span className="flex items-center"><div className="w-3 h-3 bg-amber-500 rounded-sm mr-1.5" />High</span>
            <span className="flex items-center"><div className="w-3 h-3 bg-yellow-500 rounded-sm mr-1.5" />Medium</span>
            <span className="flex items-center"><div className="w-3 h-3 bg-sky-500 rounded-sm mr-1.5" />Low</span>
          </div>
        </div>
      </div>

      {selectedAlert && (
        <div className="fixed inset-0 z-50 flex justify-end bg-black/35" onClick={() => setSelectedAlert(null)}>
          <aside
            className="h-full w-full max-w-xl overflow-y-auto border-l border-zinc-800 bg-zinc-950 p-6 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mb-6 flex items-start justify-between gap-4">
              <div>
                <div className="text-sm text-zinc-500">Alert Detail</div>
                <h3 className="mt-1 text-2xl font-bold text-white">{selectedAlert.alertType}</h3>
                <div className="mt-2"><PriorityBadge priority={selectedAlert.aiPriority} /></div>
              </div>
              <button
                onClick={() => setSelectedAlert(null)}
                className="rounded-md border border-zinc-700 px-3 py-1.5 text-sm text-zinc-300 hover:bg-zinc-900"
              >
                Close
              </button>
            </div>

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
              <DetailItem label="Rank" value={`#${selectedAlert.id}`} />
              <DetailItem label="Alert ID" value={selectedAlert.alertId ?? 'N/A'} />
              <DetailItem label="Timestamp" value={selectedAlert.timestamp} />
              <DetailItem label="Confidence" value={`${selectedAlert.confidence}%`} />
              <DetailItem label="Source IP" value={selectedAlert.sourceIp} />
              <DetailItem label="Destination IP" value={selectedAlert.destinationIp} />
              <DetailItem label="Priority Score" value={selectedAlert.priorityScore?.toString() ?? 'N/A'} />
              <DetailItem label="Priority Confidence" value={selectedAlert.priorityConfidence ? `${selectedAlert.priorityConfidence}%` : 'N/A'} />
            </div>

            <section className="mt-6 rounded-md border border-zinc-800 bg-zinc-950/70 p-4">
              <h4 className="font-semibold text-white">Description</h4>
              <p className="mt-2 text-sm text-zinc-300">{selectedAlert.description}</p>
            </section>

            <section className="mt-6 rounded-md border border-zinc-800 bg-zinc-950/70 p-4">
              <h4 className="font-semibold text-white">Recommended Analyst Actions</h4>
              <ul className="mt-3 space-y-2 text-sm text-zinc-300">
                {recommendationsByPriority[selectedAlert.aiPriority].map((recommendation) => (
                  <li key={recommendation} className="flex gap-2">
                    <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-sm bg-teal-400" />
                    <span>{recommendation}</span>
                  </li>
                ))}
              </ul>
            </section>
          </aside>
        </div>
      )}
    </div>
  );
};

const DetailItem: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="rounded-md border border-zinc-800 bg-zinc-950/70 p-3">
    <div className="text-xs uppercase tracking-normal text-zinc-500">{label}</div>
    <div className="mt-1 break-words font-mono text-sm text-zinc-200">{value}</div>
  </div>
);

export default AlertTable;
