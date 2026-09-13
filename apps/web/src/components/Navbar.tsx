import React from 'react';
import { Shield, Activity, Play, RotateCcw, Search, Terminal, Award, Cpu } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  systemStatus: string;
  onRunDemo: () => void;
  onReset: () => void;
  onOpenCommandPalette: () => void;
  isAgentActive: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  systemStatus,
  onRunDemo,
  onReset,
  onOpenCommandPalette,
  isAgentActive
}) => {
  const isHealthy = systemStatus === 'OPERATIONAL';
  const isInvestigating = isAgentActive;

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/10 bg-[#0a0d14]/90 backdrop-blur-md px-4 lg:px-6 py-2.5">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        {/* Logo & Brand */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('overview')}>
          <div className="relative flex items-center justify-center w-9 h-9 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Shield className="w-5 h-5" />
            <div className="absolute inset-0 rounded-lg shadow-[0_0_15px_rgba(0,240,255,0.4)] pointer-events-none" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-heading font-extrabold tracking-wider text-lg text-white">FLUXWARDEN</span>
              <span className="px-1.5 py-0.5 text-[10px] font-mono font-semibold rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                AI SRE
              </span>
            </div>
            <p className="text-[10px] text-slate-400 font-mono hidden sm:block">
              Observe. Decide. Act. Adapt. Recover.
            </p>
          </div>
        </div>

        {/* Hackathon & Participant Badge */}
        <div className="hidden xl:flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900/80 border border-white/10 text-xs">
          <Award className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-slate-300 font-mono">Tech Zephyr 4.0 | IIT Bhubaneswar</span>
          <span className="text-slate-600">|</span>
          <span className="text-cyan-300 font-mono font-semibold">kailashsharma8 (Solo)</span>
        </div>

        {/* Live System Operational Badge */}
        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900/60 border border-white/10 text-xs font-mono">
          <div
            className={`w-2.5 h-2.5 rounded-full ${
              isInvestigating
                ? 'bg-amber-400 animate-pulse shadow-[0_0_10px_#f59e0b]'
                : isHealthy
                ? 'bg-emerald-400 shadow-[0_0_8px_#10b981]'
                : 'bg-rose-500 animate-pulse shadow-[0_0_10px_#f43f5e]'
            }`}
          />
          <span
            className={`${
              isInvestigating
                ? 'text-amber-300'
                : isHealthy
                ? 'text-emerald-300'
                : 'text-rose-400 font-bold'
            }`}
          >
            {isInvestigating ? 'AGENT ACTIVE' : systemStatus}
          </span>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          {/* RUN DEMO Button */}
          <button
            onClick={onRunDemo}
            disabled={isAgentActive}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-heading font-bold text-xs shadow-[0_0_20px_rgba(0,240,255,0.4)] transition-all transform active:scale-95 disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>RUN DEMO</span>
          </button>

          {/* Reset Environment */}
          <button
            onClick={onReset}
            title="Reset Environment to Baseline"
            className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-white/10 text-slate-300 text-xs font-mono transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span className="hidden md:inline">Reset</span>
          </button>

          {/* Command Palette Trigger */}
          <button
            onClick={onOpenCommandPalette}
            className="hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-900 border border-white/10 hover:border-cyan-500/40 text-slate-400 hover:text-white text-xs font-mono transition-colors"
          >
            <Search className="w-3.5 h-3.5" />
            <span>Cmd+K</span>
          </button>
        </div>
      </div>
    </header>
  );
};
