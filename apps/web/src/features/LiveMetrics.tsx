import React from 'react';
import { Activity, AlertTriangle, ArrowUpRight, ArrowDownRight, Database, Cpu, Zap, HardDrive } from 'lucide-react';
import { MetricsSnapshot } from '../types';

interface LiveMetricsProps {
  metrics: MetricsSnapshot | null;
}

export const LiveMetrics: React.FC<LiveMetricsProps> = ({ metrics }) => {
  const reqRate = metrics?.request_rate ?? 1650;
  const errRate = metrics?.error_rate ?? 0.008;
  const latency = metrics?.latency_ms ?? 45;
  const cpu = metrics?.cpu_percent ?? 28;
  const mem = metrics?.memory_percent ?? 44;
  const dbConn = metrics?.db_connections ?? 120;

  const isDegraded = errRate > 0.05 || latency > 200;

  return (
    <div className="glass-panel p-5 rounded-xl border border-white/10 hover:border-cyan-500/30 transition-all">
      {/* Header */}
      <div className="flex items-center justify-between gap-3 mb-4 pb-3 border-b border-white/5">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Activity className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-sm tracking-wide text-white uppercase">
              LIVE SYSTEM TELEMETRY
            </h3>
            <span className="text-[10px] font-mono text-slate-400">
              High-Frequency Production Metrics Stream
            </span>
          </div>
        </div>

        {isDegraded ? (
          <span className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 border border-rose-500/40 text-xs font-mono font-bold animate-pulse">
            <AlertTriangle className="w-3.5 h-3.5" /> SLA BREACHED
          </span>
        ) : (
          <span className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-mono font-bold">
            SLA WITHIN BOUNDS
          </span>
        )}
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-6 gap-3">
        {/* Metric 1: Request Rate */}
        <div className="p-3 rounded-lg bg-black/40 border border-white/5 font-mono">
          <div className="flex items-center justify-between text-slate-400 text-[10px] uppercase mb-1">
            <span>Requests</span>
            <Zap className="w-3 h-3 text-cyan-400" />
          </div>
          <p className="text-lg font-bold text-white">{reqRate.toLocaleString()}</p>
          <span className="text-[10px] text-slate-400">req / sec</span>
        </div>

        {/* Metric 2: Error Rate */}
        <div className={`p-3 rounded-lg border font-mono transition-all ${
          errRate > 0.05
            ? 'bg-rose-950/40 border-rose-500 text-rose-300 shadow-[0_0_15px_rgba(239,68,68,0.2)]'
            : 'bg-black/40 border-white/5 text-slate-200'
        }`}>
          <div className="flex items-center justify-between text-[10px] uppercase mb-1">
            <span>Error Rate</span>
            {errRate > 0.05 ? (
              <ArrowUpRight className="w-3.5 h-3.5 text-rose-400 animate-bounce" />
            ) : (
              <ArrowDownRight className="w-3.5 h-3.5 text-emerald-400" />
            )}
          </div>
          <p className="text-lg font-bold">{(errRate * 100).toFixed(1)}%</p>
          <span className="text-[10px] text-slate-400">SLA &lt; 5.0%</span>
        </div>

        {/* Metric 3: Latency */}
        <div className={`p-3 rounded-lg border font-mono transition-all ${
          latency > 200
            ? 'bg-rose-950/40 border-rose-500 text-rose-300 shadow-[0_0_15px_rgba(239,68,68,0.2)]'
            : 'bg-black/40 border-white/5 text-slate-200'
        }`}>
          <div className="flex items-center justify-between text-[10px] uppercase mb-1">
            <span>Latency p95</span>
            {latency > 200 ? (
              <ArrowUpRight className="w-3.5 h-3.5 text-rose-400" />
            ) : (
              <ArrowDownRight className="w-3.5 h-3.5 text-emerald-400" />
            )}
          </div>
          <p className="text-lg font-bold">{latency}ms</p>
          <span className="text-[10px] text-slate-400">SLA &lt; 200ms</span>
        </div>

        {/* Metric 4: CPU Usage */}
        <div className="p-3 rounded-lg bg-black/40 border border-white/5 font-mono">
          <div className="flex items-center justify-between text-slate-400 text-[10px] uppercase mb-1">
            <span>Cluster CPU</span>
            <Cpu className="w-3 h-3 text-purple-400" />
          </div>
          <p className="text-lg font-bold text-white">{cpu}%</p>
          <div className="w-full bg-slate-800 h-1 rounded mt-1.5 overflow-hidden">
            <div
              className={`h-full ${cpu > 70 ? 'bg-rose-500' : 'bg-cyan-400'}`}
              style={{ width: `${Math.min(100, cpu)}%` }}
            />
          </div>
        </div>

        {/* Metric 5: Memory Usage */}
        <div className="p-3 rounded-lg bg-black/40 border border-white/5 font-mono">
          <div className="flex items-center justify-between text-slate-400 text-[10px] uppercase mb-1">
            <span>Memory (RAM)</span>
            <HardDrive className="w-3 h-3 text-blue-400" />
          </div>
          <p className="text-lg font-bold text-white">{mem}%</p>
          <div className="w-full bg-slate-800 h-1 rounded mt-1.5 overflow-hidden">
            <div
              className={`h-full ${mem > 80 ? 'bg-amber-400' : 'bg-blue-400'}`}
              style={{ width: `${Math.min(100, mem)}%` }}
            />
          </div>
        </div>

        {/* Metric 6: DB Connections */}
        <div className="p-3 rounded-lg bg-black/40 border border-white/5 font-mono">
          <div className="flex items-center justify-between text-slate-400 text-[10px] uppercase mb-1">
            <span>DB Pool</span>
            <Database className="w-3 h-3 text-emerald-400" />
          </div>
          <p className="text-lg font-bold text-white">{dbConn} / 500</p>
          <span className="text-[10px] text-slate-400">PostgreSQL</span>
        </div>
      </div>
    </div>
  );
};
