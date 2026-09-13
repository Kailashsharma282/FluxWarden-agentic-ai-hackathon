import React from 'react';
import { CheckCircle, XCircle, RefreshCw, AlertTriangle, ArrowRight, ShieldCheck, Clock } from 'lucide-react';
import { AgentEvent, AgentState } from '../types';

interface ExecutionTimelineProps {
  events: AgentEvent[];
  state: AgentState | null;
}

export const ExecutionTimeline: React.FC<ExecutionTimelineProps> = ({ events, state }) => {
  // 12 Standard Stages required by Section 32
  const timelineStages = [
    { num: '01', title: 'Goal Identified', eventMatcher: (t: string) => t.includes('GOAL_ACCEPTED') },
    { num: '02', title: 'Service Health Observed', eventMatcher: (t: string, s: string) => s.includes('get_service_health') || s.includes('health') },
    { num: '03', title: 'Logs Inspected', eventMatcher: (t: string, s: string) => s.includes('get_recent_logs') || s.includes('logs') },
    { num: '04', title: 'Deployment Anomaly Detected', eventMatcher: (t: string, s: string) => s.includes('deployments') || s.includes('HYPOTHESIS') },
    { num: '05', title: 'Rollback Selected', eventMatcher: (t: string, s: string) => s.includes('rollback_deployment') && !t.includes('FAILED') },
    { num: '06', title: 'Rollback Failed', isFailureStep: true, eventMatcher: (t: string, s: string) => t.includes('ACTION_FAILED') && s.includes('rollback') },
    { num: '07', title: 'Adaptation Triggered', isAdaptationStep: true, eventMatcher: (t: string) => t.includes('REPLAN_STARTED') },
    { num: '08', title: 'Backup Evaluated', eventMatcher: (t: string, s: string) => s.includes('backup_status') || s.includes('ALTERNATIVE_SELECTED') },
    { num: '09', title: 'Failover Selected', eventMatcher: (t: string, s: string) => s.includes('Alternative Strategy') || s.includes('route_traffic') },
    { num: '10', title: 'Traffic Rerouted', eventMatcher: (t: string, s: string) => s.includes('traffic_target') || (s.includes('route_traffic') && t.includes('COMPLETED')) },
    { num: '11', title: 'Verification Started', eventMatcher: (t: string) => t.includes('VERIFICATION_STARTED') },
    { num: '12', title: 'Recovery Confirmed', eventMatcher: (t: string) => t.includes('INCIDENT_RESOLVED') || t.includes('VERIFICATION_PASSED') },
  ];

  // Map which stages are complete based on events
  const stageStatus = timelineStages.map((stage) => {
    const matchedEvent = events.find((e) => stage.eventMatcher(e.type, `${e.summary} ${e.tool || ''}`));
    return {
      ...stage,
      completed: !!matchedEvent,
      event: matchedEvent
    };
  });

  return (
    <div className="glass-panel p-5 rounded-xl border border-white/10 hover:border-cyan-500/30 transition-all">
      {/* Header */}
      <div className="flex items-center justify-between gap-3 mb-4 pb-3 border-b border-white/5">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Clock className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-sm tracking-wide text-white uppercase">
              EXECUTION TIMELINE
            </h3>
            <span className="text-[10px] font-mono text-slate-400">
              Live Sequential Cognitive Trace (12-Phase Model)
            </span>
          </div>
        </div>

        <span className="text-[11px] font-mono text-cyan-400 px-2.5 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/20">
          {stageStatus.filter((s) => s.completed).length} / 12 COMPLETE
        </span>
      </div>

      {/* Grid of Steps */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
        {stageStatus.map((step) => {
          const isDone = step.completed;
          const isFail = step.isFailureStep && isDone;
          const isAdapt = step.isAdaptationStep && isDone;

          return (
            <div
              key={step.num}
              className={`relative p-3 rounded-lg border transition-all text-xs font-mono flex items-start gap-2.5 ${
                isFail
                  ? 'bg-rose-950/40 border-rose-500 shadow-[0_0_20px_rgba(239,68,68,0.35)] animate-pulse'
                  : isAdapt
                  ? 'bg-purple-950/40 border-purple-400 shadow-[0_0_20px_rgba(168,85,247,0.35)] animate-glow-amber'
                  : isDone
                  ? 'bg-slate-900/80 border-cyan-500/40 text-slate-200'
                  : 'bg-black/30 border-white/5 text-slate-500 opacity-60'
              }`}
            >
              <div className="flex flex-col items-center">
                <span
                  className={`text-[10px] font-bold px-1 rounded ${
                    isFail
                      ? 'bg-rose-500 text-white'
                      : isAdapt
                      ? 'bg-purple-500 text-white'
                      : isDone
                      ? 'bg-cyan-500/20 text-cyan-300'
                      : 'bg-slate-800 text-slate-500'
                  }`}
                >
                  {step.num}
                </span>
                {isFail ? (
                  <XCircle className="w-4 h-4 text-rose-400 mt-1.5" />
                ) : isAdapt ? (
                  <RefreshCw className="w-4 h-4 text-purple-400 mt-1.5 animate-spin" />
                ) : isDone ? (
                  <CheckCircle className="w-4 h-4 text-emerald-400 mt-1.5" />
                ) : (
                  <div className="w-3.5 h-3.5 rounded-full border border-slate-700 mt-1.5" />
                )}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p
                    className={`font-semibold text-xs leading-tight ${
                      isFail
                        ? 'text-rose-300 font-bold'
                        : isAdapt
                        ? 'text-purple-300 font-bold'
                        : isDone
                        ? 'text-slate-100'
                        : 'text-slate-500'
                    }`}
                  >
                    {step.title}
                  </p>
                  {step.event && (
                    <span className="text-[10px] text-slate-500 ml-1">
                      {step.event.time_display}
                    </span>
                  )}
                </div>
                {step.event && (
                  <p className="text-[10px] text-slate-400 truncate mt-0.5">
                    {step.event.summary}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
