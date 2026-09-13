import React, { useState } from 'react';
import { Flame, RotateCcw, AlertTriangle, Play, CheckCircle2, Shield, Zap } from 'lucide-react';
import { Scenario } from '../types';
import { api } from '../services/api';

interface ChaosLabProps {
  scenarios: Scenario[];
  activeScenario: string | null;
  onScenarioInjected: () => void;
  onEnvironmentReset: () => void;
  onRunDemo: () => void;
}

export const ChaosLab: React.FC<ChaosLabProps> = ({
  scenarios,
  activeScenario,
  onScenarioInjected,
  onEnvironmentReset,
  onRunDemo
}) => {
  const [injecting, setInjecting] = useState<string | null>(null);
  const [resetting, setResetting] = useState(false);

  const handleInject = async (scenarioId: string) => {
    setInjecting(scenarioId);
    try {
      await api.injectScenario(scenarioId);
      onScenarioInjected();
    } finally {
      setInjecting(null);
    }
  };

  const handleReset = async () => {
    setResetting(true);
    try {
      await api.resetEnvironment();
      onEnvironmentReset();
    } finally {
      setResetting(false);
    }
  };

  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case 'CRITICAL':
        return 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      case 'HIGH':
        return 'bg-orange-500/20 text-orange-300 border-orange-500/40';
      case 'MEDIUM':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      default:
        return 'bg-slate-800 text-slate-400 border-white/10';
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="glass-panel p-6 rounded-2xl border border-white/10 flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="p-2 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400">
              <Flame className="w-5 h-5" />
            </div>
            <h2 className="font-heading font-extrabold text-xl text-white tracking-wide">
              CHAOS LAB: RESILIENCE INJECTION SUITE
            </h2>
          </div>
          <p className="text-xs text-slate-400 font-mono">
            Inject realistic production failures to observe autonomous agentic adaptation and multi-probe recovery.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleReset}
            disabled={resetting}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono font-bold border border-white/10 transition-colors"
          >
            <RotateCcw className={`w-3.5 h-3.5 ${resetting ? 'animate-spin' : ''}`} />
            <span>Reset Environment</span>
          </button>
          <button
            onClick={onRunDemo}
            className="flex items-center gap-1.5 px-5 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-heading font-bold text-xs shadow-[0_0_20px_rgba(0,240,255,0.3)] transition-all transform hover:-translate-y-0.5"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>Trigger Demo Scenario</span>
          </button>
        </div>
      </div>

      {/* Scenario Cards Grid (Section 16 & 39) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {scenarios.map((sc) => {
          const isActive = activeScenario === sc.id;
          const isProcessing = injecting === sc.id;

          return (
            <div
              key={sc.id}
              className={`glass-panel p-5 rounded-xl border flex flex-col justify-between transition-all ${
                isActive
                  ? 'border-rose-500/70 bg-rose-950/20 shadow-[0_0_25px_rgba(239,68,68,0.25)]'
                  : 'border-white/10 hover:border-cyan-500/30'
              }`}
            >
              <div>
                {/* Header */}
                <div className="flex items-center justify-between gap-2 mb-3">
                  <h3 className="font-heading font-bold text-sm text-white uppercase tracking-wide">
                    {sc.title}
                  </h3>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${getSeverityBadge(
                      sc.severity
                    )}`}
                  >
                    {sc.severity}
                  </span>
                </div>

                <p className="text-xs text-slate-300 mb-4 leading-relaxed">
                  {sc.description}
                </p>

                {/* Symptoms */}
                <div className="space-y-1.5 font-mono text-[11px] mb-4">
                  <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block">
                    Expected Symptoms:
                  </span>
                  <p className="text-rose-300/90 bg-black/40 p-2 rounded border border-white/5">
                    {sc.symptoms}
                  </p>
                </div>

                {/* Affected Services */}
                <div className="space-y-1.5 font-mono text-[11px] mb-4">
                  <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block">
                    Affected Services:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {sc.affected_services.map((svc) => (
                      <span
                        key={svc}
                        className="px-2 py-0.5 rounded bg-slate-900 border border-white/10 text-slate-300 text-[10px]"
                      >
                        {svc}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Adaptive Flow Note */}
                {sc.adaptation_flow && (
                  <div className="p-2 rounded bg-purple-950/20 border border-purple-500/20 text-[10px] text-purple-300 font-mono mb-4">
                    <strong className="text-purple-400 block mb-0.5">Adaptation Pattern:</strong>
                    {sc.adaptation_flow}
                  </div>
                )}
              </div>

              {/* Action Button */}
              <div className="pt-3 border-t border-white/5">
                <button
                  onClick={() => handleInject(sc.id)}
                  disabled={isProcessing}
                  className={`w-full py-2 px-3 rounded-lg font-heading font-bold text-xs flex items-center justify-center gap-1.5 transition-all ${
                    isActive
                      ? 'bg-rose-500 text-white shadow-[0_0_15px_rgba(239,68,68,0.4)]'
                      : 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-white/10'
                  }`}
                >
                  <Flame className="w-3.5 h-3.5 text-rose-400" />
                  <span>{isActive ? 'Scenario Active in Cluster' : 'Inject Incident'}</span>
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
