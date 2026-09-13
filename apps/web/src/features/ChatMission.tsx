import React, { useState } from 'react';
import { Send, Bot, User, Sparkles, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

interface ChatMessage {
  id: string;
  sender: 'YOU' | 'FLUXWARDEN';
  text: string;
  timestamp: string;
}

interface ChatMissionProps {
  onMissionStarted?: () => void;
}

export const ChatMission: React.FC<ChatMissionProps> = ({ onMissionStarted }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'init',
      sender: 'FLUXWARDEN',
      text: 'FluxWarden Autonomous SRE online. Ready for infrastructure objectives. You can provide high-level goals like: "The payment API is failing. Investigate the cause and restore service without causing data loss."',
      timestamp: 'Ready'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input.trim();
    setInput('');

    const userMsg: ChatMessage = {
      id: String(Date.now()),
      sender: 'YOU',
      text: userText,
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await api.sendChatMessage(userText);
      const agentMsg: ChatMessage = {
        id: String(Date.now() + 1),
        sender: 'FLUXWARDEN',
        text: res.message || 'Mission registered.',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages((prev) => [...prev, agentMsg]);
      if (res.mission_started && onMissionStarted) {
        onMissionStarted();
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: String(Date.now() + 1),
          sender: 'FLUXWARDEN',
          text: 'Error communicating with Agent Controller. Please ensure API backend is running.',
          timestamp: new Date().toLocaleTimeString()
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handlePresetGoal = (preset: string) => {
    setInput(preset);
  };

  return (
    <div className="glass-panel p-5 rounded-xl border border-white/10 flex flex-col h-[480px]">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-white/5">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-sm text-white uppercase tracking-wide">
              NATURAL LANGUAGE MISSION INTERFACE
            </h3>
            <span className="text-[10px] font-mono text-slate-400">
              Goal-Driven Agent Dispatcher • Autonomous Objective Engine
            </span>
          </div>
        </div>

        <button
          onClick={() =>
            handlePresetGoal(
              'The payment API is failing. Investigate the cause and restore service without causing data loss.'
            )
          }
          className="text-[11px] font-mono text-cyan-400 hover:text-cyan-300 flex items-center gap-1 bg-cyan-500/10 px-2 py-1 rounded border border-cyan-500/20"
        >
          <Sparkles className="w-3 h-3" />
          <span>Load Hackathon Prompt</span>
        </button>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-2 font-mono text-xs">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`p-3 rounded-lg border ${
              m.sender === 'YOU'
                ? 'bg-slate-900 border-white/10 ml-8 text-slate-200'
                : 'bg-cyan-950/20 border-cyan-500/30 mr-8 text-cyan-100'
            }`}
          >
            <div className="flex items-center justify-between mb-1 text-[10px] text-slate-400">
              <span className="font-bold uppercase tracking-wider flex items-center gap-1.5">
                {m.sender === 'YOU' ? (
                  <User className="w-3 h-3 text-slate-400" />
                ) : (
                  <Bot className="w-3 h-3 text-cyan-400" />
                )}
                {m.sender}
              </span>
              <span>{m.timestamp}</span>
            </div>
            <p className="whitespace-pre-line leading-relaxed">{m.text}</p>
          </div>
        ))}
        {loading && (
          <div className="p-2 text-xs font-mono text-cyan-400 animate-pulse flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
            <span>FluxWarden interpreting objective and parsing constraints...</span>
          </div>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSend} className="mt-3 pt-3 border-t border-white/5 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Command objective (e.g. 'Investigate payment degradation and restore without data loss')..."
          className="flex-1 bg-black/50 border border-white/10 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 font-mono"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="px-4 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 disabled:opacity-40 text-slate-950 font-bold text-xs font-mono flex items-center gap-1.5 transition-all"
        >
          <Send className="w-3.5 h-3.5" />
          <span>DISPATCH</span>
        </button>
      </form>
    </div>
  );
};
