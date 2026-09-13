import React, { useState, useEffect } from 'react';
import { Search, Play, RotateCcw, MessageSquare, Award, Cpu, Database, Flame, X } from 'lucide-react';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectTab: (tab: string) => void;
  onRunDemo: () => void;
  onReset: () => void;
  onInjectBadDeployment: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  onSelectTab,
  onRunDemo,
  onReset,
  onInjectBadDeployment
}) => {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const commands = [
    {
      id: 'demo',
      title: 'Run Deterministic Demo Mode',
      subtitle: 'Execute full Goal -> Rollback -> Fail -> Adapt -> Verify cycle',
      icon: Play,
      color: 'text-cyan-400',
      action: () => { onRunDemo(); onClose(); }
    },
    {
      id: 'inject_bad_deploy',
      title: 'Chaos Lab: Inject Bad Deployment',
      subtitle: 'Simulate corrupted release v42 with NullPointerReference',
      icon: Flame,
      color: 'text-rose-400',
      action: () => { onInjectBadDeployment(); onClose(); }
    },
    {
      id: 'reset',
      title: 'Reset Infrastructure to Baseline',
      subtitle: 'Restore all 10 microservices to 100% healthy baseline',
      icon: RotateCcw,
      color: 'text-slate-400',
      action: () => { onReset(); onClose(); }
    },
    {
      id: 'chat',
      title: 'Open Mission Chat Interface',
      subtitle: 'Send natural language objectives to the autonomous agent',
      icon: MessageSquare,
      color: 'text-purple-400',
      action: () => { onSelectTab('chat'); onClose(); }
    },
    {
      id: 'scorecard',
      title: 'View Judge Capability Scorecard',
      subtitle: 'Review agentic capabilities mapping to hackathon evaluation criteria',
      icon: Award,
      color: 'text-amber-400',
      action: () => { onSelectTab('scorecard'); onClose(); }
    },
    {
      id: 'architecture',
      title: 'View Interactive Architecture',
      subtitle: 'Inspect cognitive loop, tool router, and simulated environment nodes',
      icon: Cpu,
      color: 'text-blue-400',
      action: () => { onSelectTab('architecture'); onClose(); }
    },
    {
      id: 'memory',
      title: 'View Operational Memory',
      subtitle: 'Examine historical incident patterns and learned recoveries',
      icon: Database,
      color: 'text-emerald-400',
      action: () => { onSelectTab('memory'); onClose(); }
    }
  ];

  const filtered = commands.filter((c) =>
    c.title.toLowerCase().includes(query.toLowerCase()) ||
    c.subtitle.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 p-4 bg-black/75 backdrop-blur-sm">
      <div className="w-full max-w-xl glass-panel-cyan rounded-xl p-3 shadow-[0_0_50px_rgba(0,0,0,0.8)] border border-cyan-500/30 overflow-hidden">
        {/* Search input */}
        <div className="flex items-center gap-3 px-3 py-2 border-b border-white/10">
          <Search className="w-4 h-4 text-cyan-400" />
          <input
            autoFocus
            type="text"
            placeholder="Type a command or search actions..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent text-sm text-white placeholder-slate-500 focus:outline-none font-mono"
          />
          <button onClick={onClose} className="text-slate-500 hover:text-white">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Command list */}
        <div className="max-h-72 overflow-y-auto py-2 space-y-1">
          {filtered.length === 0 ? (
            <div className="py-6 text-center text-xs text-slate-500 font-mono">No matching commands</div>
          ) : (
            filtered.map((cmd) => {
              const Icon = cmd.icon;
              return (
                <button
                  key={cmd.id}
                  onClick={cmd.action}
                  className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-white/5 text-left transition-colors group"
                >
                  <div className={`p-1.5 rounded-md bg-slate-800/80 ${cmd.color}`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-semibold text-slate-200 group-hover:text-cyan-300 transition-colors">
                      {cmd.title}
                    </p>
                    <p className="text-[11px] text-slate-400 truncate">{cmd.subtitle}</p>
                  </div>
                </button>
              );
            })
          )}
        </div>

        {/* Footer shortcuts helper */}
        <div className="px-3 py-1.5 border-t border-white/5 flex items-center justify-between text-[10px] text-slate-500 font-mono">
          <span>Navigate with mouse or enter</span>
          <span>ESC to close</span>
        </div>
      </div>
    </div>
  );
};
