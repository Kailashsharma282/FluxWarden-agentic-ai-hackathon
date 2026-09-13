import React from 'react';
import { MetricsSnapshot } from '../types';

interface MetricsChartCanvasProps {
  metrics: MetricsSnapshot | null;
}

export const MetricsChartCanvas: React.FC<MetricsChartCanvasProps> = ({ metrics }) => {
  return (
    <div className="w-full h-full flex flex-col justify-end p-2 font-mono text-xs">
      <div className="flex items-end gap-1.5 h-24 border-b border-white/10 pb-1">
        {[20, 25, 30, 45, 60, 85, 95, 40, 25, 20].map((h, i) => (
          <div
            key={i}
            className={`flex-1 rounded-t transition-all duration-500 ${
              h > 50 ? 'bg-rose-500/60' : 'bg-cyan-500/50'
            }`}
            style={{ height: `${h}%` }}
          />
        ))}
      </div>
      <div className="flex justify-between text-[10px] text-slate-500 mt-1">
        <span>-10m</span>
        <span>-5m</span>
        <span>Now</span>
      </div>
    </div>
  );
};
