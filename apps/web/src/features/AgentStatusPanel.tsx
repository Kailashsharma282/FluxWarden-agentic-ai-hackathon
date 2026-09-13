import React from 'react';
import { Bot, AlertCircle, RefreshCw, CheckCircle, ShieldAlert, Zap, Compass } from 'lucide-react';
import { AgentState } from '../types';

interface AgentStatusPanelProps {
  state: AgentState | null;
}

export const AgentStatusPanel: React.FC<AgentStatusPanelProps> = ({ state }) => {
  const phase = state?.current_phase || 'IDLE';
  const goal = state?.user_goal || 'Standby for objective';
  const hypothesis = state?.hypotheses?.length ? state.hypotheses[state.hypotheses.length - 1] : 'Awaiting diagnostic observations';
  const explanation = state?.structured_explanation;
  const currentAction = explanation?.current_action || (state?.completed_actions?.length ? `Last: ${state.completed_actions[state.completed_actions.length - 1]}` : 'Idle');
  const risk = state?.risk_level || 'LOW';

  const isReplanning = phase === 'REPLAN';
  const isFailed = phase === 'FAILED';
  const isComplete = phase === 'COMPLETE';
  const isWaitingApproval = phase === 'WAITING_FOR_APPROVAL';

  const getPhaseBadge = () => {
    switch (phase) {
      case 'INVESTIGATE':
        return { label: 'INVESTIGATING', bg: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40 animate-pulse' };
      case 'HYPOTHESIS':
        return { label: 'HYPOTHESIS FORMATION', bg: 'bg-purple-500/20 text-purple-300 border-purple-500/40' };
      case 'PLAN':
        return { label: 'PLANNING STRATEGY', bg: 'bg-blue-500/20 text-blue-300 border-blue-500/40' };
      case 'EXECUTE':
        return { label: 'EXECUTING REMEDIATION', bg: 'bg-amber-500/20 text-amber-300 border-amber-500/40 animate-pulse' };
      case 'EVALUATE':
        return { label: 'EVALUATING RESULT', bg: 'bg-slate-500/20 text-slate-300 border-slate-500/40' };
      case 'REPLAN':
        return { label: 'ADAPTIVE REPLANNING', bg: 'bg-rose-500/20 text-rose-300 border-rose-500/50 animate-glow-red' };
      case 'WAITING_FOR_APPROVAL':
        return { label: 'WAITING FOR APPROVAL', bg: 'bg-rose-500/30 text-rose-200 border-rose-500/60 animate-pulse' };
      case 'VERIFY':
        return { label: 'RUNNING INDEPENDENT VERIFICATION', bg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40 animate-pulse' };
      case 'COMPLETE':
        return { label: 'INCIDENT RESOLVED', bg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50' };
      case 'FAILED':
        return { label: 'HALTED / ESCALATED', bg: 'bg-rose-500/30 text-rose-300 border-rose-500/50' };
      default:
        return { label: 'SYSTEM IDLE', bg: 'bg-slate-800 text-slate-400 border-white/10' };
    }
  };

  const badge = getPhaseBadge();

  return (
    <div className={`glass-panel p-5 rounded-xl border transition-all duration-300 ${
      isReplanning ? 'border-rose-500/50 shadow-[0_0_25px_rgba(239,68,68,0.2)]' :
      isComplete ? 'border-emerald-500/50 shadow-[0_0_25px_rgba(16,185,129,0.2)]' :
      'border-white/10 hover:border-cyan-500/30'
    }`}>
      {/* Header */}
      <div className="flex items-center justify-between gap-3 mb-4 pb-3 border-b border-white/5">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-sm tracking-wide text-white uppercase">
              AGENT STATUS PANEL
            </h3>
            <span className="text-[10px] font-mono text-slate-400">
              Cognitive Graph Loop • Step {state?.attempt_count || 0} / 15
            </span>
          </div>
        </div>

        <span className={`px-2.5 py-1 text-xs font-mono font-bold rounded border tracking-wider ${badge.bg}`}>
          {badge.label}
        </span>
      </div>

      {/* Grid of details */}
      <div className="space-y-3.5 text-xs font-mono">
        {/* CURRENT GOAL */}
        <div>
          <span className="text-[10px] uppercase font-bold tracking-widest text-slate-400 block mb-1">
            CURRENT GOAL
          </span>
          <div className="p-2.5 rounded-lg bg-slate-900/80 border border-white/5 text-slate-200">
            {goal}
          </div>
        </div>

        {/* CURRENT HYPOTHESIS */}
        <div>
          <span className="text-[10px] uppercase font-bold tracking-widest text-purple-400 block mb-1">
            CURRENT HYPOTHESIS
          </span>
          <div className="p-2.5 rounded-lg bg-purple-950/20 border border-purple-500/20 text-purple-200">
            {hypothesis}
          </div>
        </div>

        {/* CURRENT ACTION & RISK */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
          <div className="sm:col-span-2">
            <span className="text-[10px] uppercase font-bold tracking-widest text-cyan-400 block mb-1">
              CURRENT ACTION
            </span>
            <div className="p-2.5 rounded-lg bg-cyan-950/20 border border-cyan-500/20 text-cyan-300 font-semibold truncate">
              {currentAction}
            </div>
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold tracking-widest text-slate-400 block mb-1">
              RISK
            </span>
            <div className={`p-2.5 rounded-lg font-bold text-center border ${
              risk === 'CRITICAL' ? 'bg-rose-500/30 text-rose-300 border-rose-500/40' :
              risk === 'HIGH' ? 'bg-orange-500/20 text-orange-300 border-orange-500/40' :
              risk === 'MEDIUM' ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' :
              'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
            }`}>
              {risk}
            </div>
          </div>
        </div>

        {/* Structured Safe Operational Explanation (Section 8) */}
        {explanation && (
          <div className="mt-3 pt-3 border-t border-white/5 space-y-2">
            <div className="flex items-center justify-between text-[10px] text-slate-400 font-bold uppercase tracking-wider">
              <span>Operational Rationale</span>
              <span className="text-cyan-400">Structured Safe Summary</span>
            </div>
            <div className="grid grid-cols-1 gap-1.5 p-2.5 rounded-lg bg-black/40 border border-white/5 text-[11px]">
              <div>
                <span className="text-slate-500 font-semibold">WHY: </span>
                <span className="text-slate-300">{explanation.why}</span>
              </div>
              <div>
                <span className="text-slate-500 font-semibold">EXPECTED: </span>
                <span className="text-slate-300">{explanation.expected_result}</span>
              </div>
              {explanation.adaptation && (
                <div>
                  <span className="text-rose-400 font-semibold">ADAPTATION: </span>
                  <span className="text-rose-200">{explanation.adaptation}</span>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
