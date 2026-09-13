import React from 'react';
import { Shield, Play, ArrowRight, Cpu, Zap, Activity, RefreshCw, CheckCircle, Award } from 'lucide-react';

interface LandingPageProps {
  onLaunch: () => void;
  onViewArchitecture: () => void;
  onRunDemo: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({
  onLaunch,
  onViewArchitecture,
  onRunDemo
}) => {
  return (
    <div className="relative min-h-[calc(100vh-64px)] flex flex-col justify-between px-4 lg:px-8 py-12 max-w-7xl mx-auto">
      {/* Top Hackathon & Team Pill */}
      <div className="flex flex-wrap items-center justify-center gap-3">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono tracking-wide shadow-[0_0_15px_rgba(0,240,255,0.2)]">
          <Award className="w-3.5 h-3.5 text-amber-400" />
          <span>Agentic AI Hackathon | Tech Zephyr 4.0 • IIT Bhubaneswar</span>
        </div>
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs font-mono tracking-wide">
          <span>Team: <strong>kailashsharma8</strong> (Pochiraju Kailash Ram Markandeya Sharma)</span>
        </div>
      </div>

      {/* Main Hero Section (Section 28) */}
      <div className="my-auto py-12 text-center max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 mb-6 rounded-md bg-slate-900/80 border border-white/10 text-slate-400 text-xs font-mono uppercase tracking-widest">
          <Zap className="w-3 h-3 text-cyan-400" />
          Autonomous AI Incident Response Engineer
        </div>

        <h1 className="font-heading font-extrabold text-5xl sm:text-7xl lg:text-8xl tracking-tight text-white mb-6">
          FLUX<span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-blue-500">WARDEN</span>
        </h1>

        <div className="space-y-2 mb-8">
          <p className="font-mono text-sm sm:text-base font-semibold tracking-widest text-cyan-300 uppercase">
            AUTONOMOUS INCIDENT RECOVERY
          </p>
          <div className="text-xl sm:text-3xl text-slate-200 font-heading font-medium leading-relaxed">
            AI THAT DOESN'T JUST TELL YOU WHAT WENT WRONG.
          </div>
          <div className="text-2xl sm:text-4xl font-heading font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400 tracking-wide">
            IT ADAPTS. IT ACTS. IT RECOVERS.
          </div>
        </div>

        <p className="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto leading-relaxed mb-10 font-mono">
          An authentic agentic state machine that observes microservice telemetry, forms hypotheses, tests remediations, dynamically adapts when actions fail, and independently verifies full system recovery.
        </p>

        {/* Hero CTAs */}
        <div className="flex flex-wrap items-center justify-center gap-4">
          <button
            onClick={onLaunch}
            className="flex items-center gap-2 px-7 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-heading font-bold text-sm sm:text-base shadow-[0_0_30px_rgba(0,240,255,0.4)] transition-all transform hover:-translate-y-0.5 active:translate-y-0"
          >
            <span>Launch Command Center</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={onRunDemo}
            className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-cyan-500/40 text-cyan-300 font-heading font-bold text-sm sm:text-base shadow-[0_0_20px_rgba(0,240,255,0.15)] transition-all transform hover:-translate-y-0.5"
          >
            <Play className="w-4 h-4 fill-cyan-400 text-cyan-400" />
            <span>Trigger Demo Mode</span>
          </button>

          <button
            onClick={onViewArchitecture}
            className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-slate-900/60 hover:bg-slate-800/80 border border-white/10 text-slate-300 font-heading font-semibold text-sm sm:text-base transition-colors"
          >
            <Cpu className="w-4 h-4 text-slate-400" />
            <span>View Architecture</span>
          </button>
        </div>
      </div>

      {/* Feature Highlights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-8 border-t border-white/5">
        <div className="glass-panel p-4 rounded-xl border border-white/5 hover:border-cyan-500/30 transition-colors">
          <div className="flex items-center gap-2 text-cyan-400 text-xs font-mono uppercase mb-1">
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Adaptation Loop</span>
          </div>
          <p className="text-xs text-slate-300">
            Intentionally detects failed rollbacks without crashing and replans alternate recovery paths.
          </p>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-white/5 hover:border-cyan-500/30 transition-colors">
          <div className="flex items-center gap-2 text-purple-400 text-xs font-mono uppercase mb-1">
            <Shield className="w-3.5 h-3.5" />
            <span>39 Sandboxed Tools</span>
          </div>
          <p className="text-xs text-slate-300">
            Diagnostics, remediation, safety, and verification tools executing in simulated topology.
          </p>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-white/5 hover:border-cyan-500/30 transition-colors">
          <div className="flex items-center gap-2 text-emerald-400 text-xs font-mono uppercase mb-1">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>Independent Verification</span>
          </div>
          <p className="text-xs text-slate-300">
            Never assumes success from HTTP 200. Multi-probe verification ensures real SLA recovery.
          </p>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-white/5 hover:border-cyan-500/30 transition-colors">
          <div className="flex items-center gap-2 text-amber-400 text-xs font-mono uppercase mb-1">
            <Activity className="w-3.5 h-3.5" />
            <span>Real-time Telemetry</span>
          </div>
          <p className="text-xs text-slate-300">
            Live WebSockets stream timeline steps, active traffic rerouting, and metrics dynamically.
          </p>
        </div>
      </div>
    </div>
  );
};
