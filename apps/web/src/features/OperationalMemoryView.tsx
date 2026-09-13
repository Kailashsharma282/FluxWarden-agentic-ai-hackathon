import React, { useState } from 'react';
import { Database, Search, Sparkles, CheckCircle2, History, ArrowRight } from 'lucide-react';

export const OperationalMemoryView: React.FC = () => {
  const [query, setQuery] = useState('payment');

  const historicalMemories = [
    {
      incident_id: 'INC-HIST-881',
      date: '2026-08-14 09:22:15 UTC',
      scenario: 'bad_deployment',
      symptoms: ['HTTP 500 spike (74%)', 'Release v42 rollout', 'NullPointerReference in checkout'],
      failed_attempts: ['rollback_deployment (image registry sha256 mismatch)'],
      successful_strategy: 'route_traffic ➔ backup-service (standby replica v40-stable)',
      confidence: 0.96,
      duration: '38.4s',
      notes: 'Rollback frequently fails when CI container registry cache is desynced. Routing to standby replica restores instant 99.99% availability.'
    },
    {
      incident_id: 'INC-HIST-742',
      date: '2026-07-29 14:10:00 UTC',
      scenario: 'db_connection_exhaustion',
      symptoms: ['Postgres connection pool > 95%', 'Client connection timeouts'],
      failed_attempts: ['restart_service (connections immediately restacked)'],
      successful_strategy: 'scale_service (dynamically increase pool to 500) and connection reset',
      confidence: 0.91,
      duration: '24.0s',
      notes: 'Scaling connection pool and resetting idle connection leaks resolved the database lockup.'
    },
    {
      incident_id: 'INC-HIST-610',
      date: '2026-06-18 18:45:00 UTC',
      scenario: 'redis_outage',
      symptoms: ['Redis connection refused on 6379', 'Cache miss latency explosion'],
      failed_attempts: [],
      successful_strategy: 'failover_service ➔ promoted Redis hot standby replica',
      confidence: 0.98,
      duration: '16.2s',
      notes: 'Hot standby promotion completes within 3 seconds with zero data loss.'
    }
  ];

  const filtered = historicalMemories.filter((m) =>
    m.symptoms.some((s) => s.toLowerCase().includes(query.toLowerCase())) ||
    m.scenario.toLowerCase().includes(query.toLowerCase()) ||
    m.incident_id.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="space-y-6 font-mono">
      {/* Top Header */}
      <div className="glass-panel p-6 rounded-2xl border border-white/10 flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
              <Database className="w-5 h-5" />
            </div>
            <h2 className="font-heading font-extrabold text-xl text-white tracking-wide">
              OPERATIONAL MEMORY & PATTERN RECALL
            </h2>
          </div>
          <p className="text-xs text-slate-400">
            Section 19: Learning from past incidents via structured operational memory (not black-box ML).
          </p>
        </div>

        {/* Search Filter */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-black/40 border border-white/10 text-xs">
          <Search className="w-3.5 h-3.5 text-slate-400" />
          <input
            type="text"
            placeholder="Search symptoms, scenarios..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="bg-transparent text-white placeholder-slate-500 focus:outline-none text-xs"
          />
        </div>
      </div>

      {/* Memory Cards */}
      <div className="space-y-4">
        {filtered.map((rec) => (
          <div
            key={rec.incident_id}
            className="glass-panel p-5 rounded-xl border border-white/10 hover:border-emerald-500/30 transition-all text-xs space-y-3"
          >
            <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-white/5">
              <div className="flex items-center gap-2">
                <span className="font-bold text-emerald-400 text-sm">{rec.incident_id}</span>
                <span className="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300">
                  {rec.scenario}
                </span>
                <span className="text-[10px] text-slate-500">{rec.date}</span>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-[10px] text-slate-400">Recall Confidence:</span>
                <strong className="text-emerald-400 text-xs font-bold">
                  {(rec.confidence * 100).toFixed(0)}%
                </strong>
              </div>
            </div>

            {/* Symptoms */}
            <div>
              <span className="text-[10px] uppercase text-slate-400 font-bold block mb-1">
                Symptom Signature:
              </span>
              <div className="flex flex-wrap gap-1.5">
                {rec.symptoms.map((s, i) => (
                  <span
                    key={i}
                    className="px-2 py-0.5 rounded bg-rose-950/40 text-rose-300 border border-rose-500/20 text-[11px]"
                  >
                    {s}
                  </span>
                ))}
              </div>
            </div>

            {/* Failed vs Successful Strategy */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div className="p-2.5 rounded bg-black/40 border border-white/5">
                <span className="text-[10px] uppercase text-rose-400 font-bold block mb-0.5">
                  Failed Strategy in Past:
                </span>
                <p className="text-slate-300 text-[11px]">
                  {rec.failed_attempts.join(', ') || 'None'}
                </p>
              </div>

              <div className="p-2.5 rounded bg-emerald-950/20 border border-emerald-500/20">
                <span className="text-[10px] uppercase text-emerald-400 font-bold block mb-0.5">
                  Verified Historical Recovery:
                </span>
                <p className="text-emerald-200 text-[11px] font-semibold">
                  {rec.successful_strategy}
                </p>
              </div>
            </div>

            <p className="text-[11px] text-slate-400 leading-relaxed italic">
              Note: {rec.notes}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
