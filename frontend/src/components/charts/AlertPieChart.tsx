import React from 'react';
import type { AlertPieChartProps } from '../../types';

const AlertPieChart: React.FC<AlertPieChartProps> = ({ data }) => {
  const total = data.reduce((sum, item) => sum + item.value, 0);
  let accumulatedAngle = 0;
  const radius = 60;
  const center = 70;
  const formattedTotal = new Intl.NumberFormat('en', { notation: 'compact', maximumFractionDigits: 1 }).format(total);
  const totalSizeClass = formattedTotal.length > 5
    ? 'text-base'
    : formattedTotal.length > 3
      ? 'text-xl'
      : 'text-2xl';

  const paths = data.map((item, index) => {
    const angle = (item.value / total) * 360;
    const startAngle = accumulatedAngle;
    const endAngle = startAngle + angle;
    accumulatedAngle = endAngle;

    const startRad = (startAngle - 90) * (Math.PI / 180);
    const endRad = (endAngle - 90) * (Math.PI / 180);

    const x1 = center + radius * Math.cos(startRad);
    const y1 = center + radius * Math.sin(startRad);
    const x2 = center + radius * Math.cos(endRad);
    const y2 = center + radius * Math.sin(endRad);

    const largeArc = angle > 180 ? 1 : 0;

    const pathData = [
      `M ${center} ${center}`,
      `L ${x1} ${y1}`,
      `A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2}`,
      'Z'
    ].join(' ');

    return (
      <path
        key={index}
        d={pathData}
        fill={item.color}
        stroke="#1f2937"
        strokeWidth="1"
        className="transition-all duration-300 hover:opacity-80 cursor-pointer"
      />
    );
  });

  return (
    <div className="border border-zinc-800 bg-zinc-950/80 shadow-[0_18px_50px_rgba(0,0,0,0.25)] p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Alert Priority Distribution</h3>
      <div className="flex items-center">
        <div className="relative w-40 h-40 shrink-0">
          <svg className="mx-auto" width="140" height="140" viewBox="0 0 140 140">
            {paths}
            <circle cx={center} cy={center} r={radius * 0.5} fill="#111827" />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="flex h-16 w-16 flex-col items-center justify-center overflow-hidden rounded-sm text-center">
              <div
                className={`max-w-[3.75rem] truncate font-bold leading-none text-white ${totalSizeClass}`}
                title={total.toLocaleString()}
              >
                {formattedTotal}
              </div>
              <div className="mt-1 mb-3 text-[11px] uppercase leading-none tracking-normal text-zinc-400">
                Total
              </div>
            </div>
          </div>
        </div>
        <div className="ml-6 flex-1">
          {data.map((item, index) => (
            <div key={index} className="flex items-center justify-between mb-3">
              <div className="flex items-center">
                <div 
                  className="w-3 h-3 rounded-sm mr-2"
                  style={{ backgroundColor: item.color }}
                ></div>
                <span className="text-zinc-300">{item.name}</span>
              </div>
              <div className="text-right">
                <div className="text-white font-semibold">{item.value}</div>
                <div className="text-zinc-500 text-sm">
                  {((item.value / total) * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AlertPieChart;