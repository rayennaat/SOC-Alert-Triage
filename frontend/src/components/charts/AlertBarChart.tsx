import React from 'react';
import type { AlertBarChartProps } from '../../types';

const AlertBarChart: React.FC<AlertBarChartProps> = ({ data }) => {
  const maxValue = Math.max(...data.map(item => item.count));

  return (
    <div className="border border-zinc-800 bg-zinc-950/80 shadow-[0_18px_50px_rgba(0,0,0,0.25)] p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Alerts by Type</h3>
      <div className="space-y-4">
        {data.map((item, index) => {
          const widthPercent = (item.count / maxValue) * 100;
          
          return (
            <div key={index} className="flex items-center">
              <div className="w-32 text-zinc-400 text-sm truncate">{item.name}</div>
              <div className="flex-1 ml-4">
                <div className="relative h-6 bg-zinc-900 rounded overflow-hidden">
                  <div 
                    className="absolute top-0 left-0 h-full bg-gradient-to-r from-teal-500 to-emerald-300 rounded transition-all duration-500"
                    style={{ width: `${widthPercent}%` }}
                  ></div>
                  <div className="relative z-10 px-3 text-white text-sm font-medium">
                    {item.count} alerts
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AlertBarChart;