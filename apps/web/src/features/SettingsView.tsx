import React, { useState, useEffect } from 'react';
import { Settings, Shield, Sliders, Key, Database, Cpu, Check, Eye, EyeOff, Save } from 'lucide-react';
import { motion } from 'framer-motion';
import { APP_CONFIG } from '../lib/constants';
import { api } from '../services/api';

export const SettingsView: React.FC = () => {
  const [provider, setProvider] = useState<'mock' | 'openai' | 'gemini' | 'anthropic'>('mock');
  const [openaiKey, setOpenaiKey] = useState('');
  const [geminiKey, setGeminiKey] = useState('');
  const [anthropicKey, setAnthropicKey] = useState('');
  const [hasKeys, setHasKeys] = useState({ openai: false, gemini: false, anthropic: false });
  const [showKeys, setShowKeys] = useState(false);
  const [maxSteps, setMaxSteps] = useState(APP_CONFIG.MAX_AGENT_STEPS);
  const [maxReplans, setMaxReplans] = useState(APP_CONFIG.MAX_REPLAN_ATTEMPTS);
  const [maxRetries, setMaxRetries] = useState(APP_CONFIG.MAX_TOOL_RETRIES);
  const [stepDelay, setStepDelay] = useState(0.8);
  const [reducedMotion, setReducedMotion] = useState(false);
  const [savedNotice, setSavedNotice] = useState(false);

  useEffect(() => {
    api.getSettings().then((data) => {
      if (data) {
        if (data.llm_provider) setProvider(data.llm_provider);
        if (data.max_agent_steps) setMaxSteps(data.max_agent_steps);
        if (data.max_replan_attempts) setMaxReplans(data.max_replan_attempts);
        if (data.max_tool_retries !== undefined) setMaxRetries(data.max_tool_retries);
        setHasKeys({
          openai: !!data.has_openai_key,
          gemini: !!data.has_gemini_key,
          anthropic: !!data.has_anthropic_key
        });
      }
    }).catch((e) => console.warn('Could not fetch settings:', e));
  }, []);

  const handleSave = async () => {
    try {
      const payload: any = {
        llm_provider: provider,
        max_agent_steps: maxSteps,
        max_replan_attempts: maxReplans,
        max_tool_retries: maxRetries
      };
      if (openaiKey) payload.openai_api_key = openaiKey;
      if (geminiKey) payload.gemini_api_key = geminiKey;
      if (anthropicKey) payload.anthropic_api_key = anthropicKey;

      const res = await api.updateSettings(payload);
      if (res) {
        setHasKeys({
          openai: !!res.has_openai_key,
          gemini: !!res.has_gemini_key,
          anthropic: !!res.has_anthropic_key
        });
      }
      setSavedNotice(true);
      setTimeout(() => setSavedNotice(false), 2500);
    } catch (e) {
      console.error('Failed to save settings:', e);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6 max-w-4xl mx-auto font-mono text-xs"
    >
      {/* Header */}
      <div className="glass-panel p-6 rounded-2xl border border-white/10 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
              <Settings className="w-5 h-5" />
            </div>
            <h2 className="font-heading font-extrabold text-xl text-white tracking-wide">
              SYSTEM & AGENT SETTINGS
            </h2>
          </div>
          <p className="text-xs text-slate-400">
            Configure LLM execution providers, cognitive state graph limits, and safety controls (Section 30).
          </p>
        </div>

        {savedNotice && (
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs">
            <Check className="w-3.5 h-3.5" />
            <span>Settings Saved</span>
          </div>
        )}
      </div>

      {/* 1. LLM Provider Selection (Section 23 & 56 & 57) */}
      <div className="glass-panel p-6 rounded-xl border border-white/10 space-y-4">
        <div className="flex items-center gap-2 pb-2 border-b border-white/5">
          <Cpu className="w-4 h-4 text-cyan-400" />
          <h3 className="font-heading font-bold text-sm text-white uppercase tracking-wider">
            Cognitive Provider Abstraction (Section 23)
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
          {(['mock', 'openai', 'gemini', 'anthropic'] as const).map((p) => (
            <button
              key={p}
              onClick={() => setProvider(p)}
              className={`p-3.5 rounded-xl border text-left transition-all ${
                provider === p
                  ? 'bg-cyan-500/15 border-cyan-400 text-white shadow-[0_0_15px_rgba(0,240,255,0.2)]'
                  : 'bg-black/30 border-white/10 text-slate-400 hover:border-white/20'
              }`}
            >
              <div className="font-bold text-xs uppercase text-cyan-300 mb-1">{p}</div>
              <div className="text-[10px] text-slate-400">
                {p === 'mock' ? 'Autonomous zero-key engine (Default)' : `Real ${p.toUpperCase()} API`}
              </div>
            </button>
          ))}
        </div>

        {provider !== 'mock' && (
          <div className="space-y-3 pt-2">
            <div className="flex items-center justify-between text-slate-400">
              <span>API Key Configuration</span>
              <button
                type="button"
                onClick={() => setShowKeys(!showKeys)}
                className="flex items-center gap-1 text-[11px] text-cyan-400 hover:underline"
              >
                {showKeys ? <EyeOff className="w-3 h-3" /> : <Eye className="w-3 h-3" />}
                <span>{showKeys ? 'Hide Keys' : 'Show Keys'}</span>
              </button>
            </div>

            {provider === 'openai' && (
              <div className="space-y-1">
                {hasKeys.openai && (
                  <div className="text-[10px] text-emerald-400 flex items-center gap-1">
                    <Check className="w-3 h-3" /> Key active in environment. Enter new value below to override.
                  </div>
                )}
                <input
                  type={showKeys ? 'text' : 'password'}
                  placeholder={hasKeys.openai ? "•••••••••••••••• (Enter new key to update)" : "sk-proj-..."}
                  value={openaiKey}
                  onChange={(e) => setOpenaiKey(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-black/40 border border-white/10 text-white placeholder-slate-500 focus:border-cyan-400 outline-none"
                />
              </div>
            )}
            {provider === 'gemini' && (
              <div className="space-y-1">
                {hasKeys.gemini && (
                  <div className="text-[10px] text-emerald-400 flex items-center gap-1">
                    <Check className="w-3 h-3" /> Key active in environment. Enter new value below to override.
                  </div>
                )}
                <input
                  type={showKeys ? 'text' : 'password'}
                  placeholder={hasKeys.gemini ? "•••••••••••••••• (Enter new key to update)" : "AIzaSy..."}
                  value={geminiKey}
                  onChange={(e) => setGeminiKey(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-black/40 border border-white/10 text-white placeholder-slate-500 focus:border-cyan-400 outline-none"
                />
              </div>
            )}
            {provider === 'anthropic' && (
              <div className="space-y-1">
                {hasKeys.anthropic && (
                  <div className="text-[10px] text-emerald-400 flex items-center gap-1">
                    <Check className="w-3 h-3" /> Key active in environment. Enter new value below to override.
                  </div>
                )}
                <input
                  type={showKeys ? 'text' : 'password'}
                  placeholder={hasKeys.anthropic ? "•••••••••••••••• (Enter new key to update)" : "sk-ant-api03-..."}
                  value={anthropicKey}
                  onChange={(e) => setAnthropicKey(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-black/40 border border-white/10 text-white placeholder-slate-500 focus:border-cyan-400 outline-none"
                />
              </div>
            )}
          </div>
        )}
      </div>

      {/* 2. Safety Limits & State Machine Guards (Section 5) */}
      <div className="glass-panel p-6 rounded-xl border border-white/10 space-y-4">
        <div className="flex items-center gap-2 pb-2 border-b border-white/5">
          <Shield className="w-4 h-4 text-purple-400" />
          <h3 className="font-heading font-bold text-sm text-white uppercase tracking-wider">
            Agent Safety & Bounded Loops (Section 5)
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-3.5 rounded-lg bg-black/30 border border-white/5 space-y-1.5">
            <label className="text-slate-400 text-[11px] block">MAX_AGENT_STEPS</label>
            <input
              type="number"
              min={5}
              max={50}
              value={maxSteps}
              onChange={(e) => setMaxSteps(Number(e.target.value))}
              className="w-full px-2.5 py-1.5 rounded bg-black/50 border border-white/10 text-white"
            />
            <span className="text-[10px] text-slate-500">Ceiling to prevent infinite loops</span>
          </div>

          <div className="p-3.5 rounded-lg bg-black/30 border border-white/5 space-y-1.5">
            <label className="text-slate-400 text-[11px] block">MAX_REPLAN_ATTEMPTS</label>
            <input
              type="number"
              min={1}
              max={10}
              value={maxReplans}
              onChange={(e) => setMaxReplans(Number(e.target.value))}
              className="w-full px-2.5 py-1.5 rounded bg-black/50 border border-white/10 text-white"
            />
            <span className="text-[10px] text-slate-500">Max alternate paths evaluated</span>
          </div>

          <div className="p-3.5 rounded-lg bg-black/30 border border-white/5 space-y-1.5">
            <label className="text-slate-400 text-[11px] block">MAX_TOOL_RETRIES</label>
            <input
              type="number"
              min={0}
              max={5}
              value={maxRetries}
              onChange={(e) => setMaxRetries(Number(e.target.value))}
              className="w-full px-2.5 py-1.5 rounded bg-black/50 border border-white/10 text-white"
            />
            <span className="text-[10px] text-slate-500">Exponential backoff retry limit</span>
          </div>
        </div>
      </div>

      {/* 3. Animation & Accessibility (Section 29 & 48) */}
      <div className="glass-panel p-6 rounded-xl border border-white/10 space-y-4">
        <div className="flex items-center gap-2 pb-2 border-b border-white/5">
          <Sliders className="w-4 h-4 text-emerald-400" />
          <h3 className="font-heading font-bold text-sm text-white uppercase tracking-wider">
            UI Motion & Execution Telemetry
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="p-3.5 rounded-lg bg-black/30 border border-white/5 space-y-2">
            <div className="flex justify-between">
              <span className="text-slate-300">Autonomous Step Delay</span>
              <span className="text-cyan-400 font-bold">{stepDelay}s</span>
            </div>
            <input
              type="range"
              min={0.2}
              max={2.5}
              step={0.1}
              value={stepDelay}
              onChange={(e) => setStepDelay(Number(e.target.value))}
              className="w-full accent-cyan-400"
            />
            <span className="text-[10px] text-slate-500">Speed of live cognitive turns</span>
          </div>

          <div className="p-3.5 rounded-lg bg-black/30 border border-white/5 flex items-center justify-between">
            <div>
              <span className="text-slate-300 block font-bold">Prefers Reduced Motion</span>
              <span className="text-[10px] text-slate-500">Disable background particle motion (Section 29)</span>
            </div>
            <button
              onClick={() => setReducedMotion(!reducedMotion)}
              className={`w-11 h-6 flex items-center rounded-full p-1 transition-colors ${
                reducedMotion ? 'bg-cyan-500' : 'bg-slate-700'
              }`}
            >
              <div
                className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${
                  reducedMotion ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-heading font-bold shadow-[0_0_20px_rgba(0,240,255,0.3)] transition-all"
        >
          <Save className="w-4 h-4" />
          <span>Apply Configuration</span>
        </button>
      </div>
    </motion.div>
  );
};
