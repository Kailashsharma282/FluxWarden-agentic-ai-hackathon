import React, { useRef, useEffect } from 'react';
import { Terminal, Copy, Check, Download } from 'lucide-react';
import { AgentEvent } from '../types';

interface AgentTerminalProps {
  events: AgentEvent[];
}

export const AgentTerminal: React.FC<AgentTerminalProps> = ({ events }) => {
  const terminalEndRef = useRef<HTMLDivElement | null>(null);
  const [copied, setCopied] = React.useState(false);

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [events]);

  const handleCopyLogs = () => {
    const text = events.map((e) => `[${e.time_display}] ${e.type}: ${e.summary}`).join('\n');
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getEventColor = (type: string, severity: string) => {
    if (type.includes('FAIL') || severity === 'error') return 'text-rose-400 font-bold';
    if (type.includes('REPLAN') || severity === 'warning') return 'text-purple-300 font-bold';
    if (type.includes('PASSED') || type.includes('RESOLVED') || severity === 'success') return 'text-emerald-300 font-bold';
    if (type.includes('TOOL') || type.includes('ACTION')) return 'text-cyan-300';
    return 'text-slate-300';
  };

  return (
    <div className="glass-panel p-5 rounded-xl border border-white/10 flex flex-col h-[480px]">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-white/5">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Terminal className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-sm text-white uppercase tracking-wide">
              AGENT EVENT TERMINAL
            </h3>
            <span className="text-[10px] font-mono text-slate-400">
              Live Real-Time Event Bus • Subscribed via WebSocket
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopyLogs}
            className="flex items-center gap-1 px-2.5 py-1 rounded bg-slate-800/80 hover:bg-slate-700 text-[11px] font-mono text-slate-300 border border-white/10 transition-colors"
          >
            {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3 text-slate-400" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
        </div>
      </div>

      {/* Terminal Viewport */}
      <div className="flex-1 bg-[#06080d] p-3.5 rounded-lg border border-white/5 overflow-y-auto font-mono text-xs space-y-1.5 shadow-inner">
        {events.length === 0 ? (
          <div className="text-slate-600 text-center py-20">
            Waiting for agent events... Trigger 'RUN DEMO' or dispatch a mission.
          </div>
        ) : (
          events.map((e) => (
            <div key={e.id} className="flex items-start gap-2.5 leading-relaxed hover:bg-white/[0.02] p-0.5 rounded">
              <span className="text-slate-600 select-none text-[11px]">{e.time_display}</span>
              <span className="text-cyan-500 select-none">❯</span>
              <div className="flex-1 min-w-0">
                <span className="text-slate-400 font-semibold mr-2">[{e.type}]</span>
                <span className={getEventColor(e.type, e.severity)}>
                  {e.tool ? `${e.tool}() — ` : ''}
                  {e.summary}
                </span>
              </div>
            </div>
          ))
        )}
        <div ref={terminalEndRef} />
      </div>
    </div>
  );
};
