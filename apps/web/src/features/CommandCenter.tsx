import React, { useState } from 'react';
import {
  Layers,
  Bot,
  Activity,
  Network,
  Flame,
  FileText,
  Database,
  Cpu,
  Award,
  Settings as SettingsIcon,
  Play,
  RotateCcw,
  MessageSquare
} from 'lucide-react';
import { AgentEvent, AgentState, MetricsSnapshot, Scenario, ServiceNode } from '../types';
import { AgentStatusPanel } from './AgentStatusPanel';
import { ExecutionTimeline } from './ExecutionTimeline';
import { ServiceTopology } from './ServiceTopology';
import { LiveMetrics } from './LiveMetrics';
import { ChatMission } from './ChatMission';
import { AgentTerminal } from './AgentTerminal';
import { FinalResolutionCard } from './FinalResolutionCard';
import { ChaosLab } from './ChaosLab';
import { ArchitecturePage } from './ArchitecturePage';
import { JudgeScorecard } from './JudgeScorecard';
import { OperationalMemoryView } from './OperationalMemoryView';
import { IncidentDetail } from './IncidentDetail';
import { SettingsView } from './SettingsView';

interface CommandCenterProps {
  activeSubTab: string;
  setActiveSubTab: (tab: string) => void;
  state: AgentState | null;
  events: AgentEvent[];
  services: ServiceNode[];
  metrics: MetricsSnapshot | null;
  scenarios: Scenario[];
  activeScenario: string | null;
  trafficTarget: string;
  onRunDemo: () => void;
  onReset: () => void;
  onScenarioInjected: () => void;
}

export const CommandCenter: React.FC<CommandCenterProps> = ({
  activeSubTab,
  setActiveSubTab,
  state,
  events,
  services,
  metrics,
  scenarios,
  activeScenario,
  trafficTarget,
  onRunDemo,
  onReset,
  onScenarioInjected
}) => {
  const navItems = [
    { id: 'overview', label: 'Mission Control', icon: Layers },
    { id: 'agent', label: 'Agent Brain & State', icon: Bot },
    { id: 'services', label: 'Service Topology', icon: Network },
    { id: 'metrics', label: 'Live Telemetry', icon: Activity },
    { id: 'chaos', label: 'Chaos Lab', icon: Flame },
    { id: 'incidents', label: 'Incident Forensics', icon: FileText },
    { id: 'chat', label: 'Mission Chat', icon: MessageSquare },
    { id: 'memory', label: 'Operational Memory', icon: Database },
    { id: 'architecture', label: 'Architecture', icon: Cpu },
    { id: 'scorecard', label: 'Judge Scorecard', icon: Award },
    { id: 'settings', label: 'Settings', icon: SettingsIcon },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-6 py-6 space-y-6">
      {/* Sub Navigation Bar */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-2 border-b border-white/5 scrollbar-none font-mono text-xs">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeSubTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveSubTab(item.id)}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg whitespace-nowrap transition-all ${
                isActive
                  ? 'bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 font-bold shadow-[0_0_15px_rgba(0,240,255,0.15)]'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5 border border-transparent'
              }`}
            >
              <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-cyan-400' : 'text-slate-500'}`} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>

      {/* Main View Switching */}
      {activeSubTab === 'overview' && (
        <div className="space-y-6">
          {/* Final Resolution Card if Resolved */}
          <FinalResolutionCard state={state} />

          {/* Top Row: Agent Status Panel + Live Telemetry */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-5">
              <AgentStatusPanel state={state} />
            </div>
            <div className="lg:col-span-7">
              <LiveMetrics metrics={metrics} />
            </div>
          </div>

          {/* Middle Row: Execution Timeline */}
          <ExecutionTimeline events={events} state={state} />

          {/* Bottom Row: Topology & Terminal */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-7">
              <ServiceTopology services={services} trafficTarget={trafficTarget} />
            </div>
            <div className="lg:col-span-5">
              <AgentTerminal events={events} />
            </div>
          </div>
        </div>
      )}

      {activeSubTab === 'agent' && (
        <div className="space-y-6">
          <FinalResolutionCard state={state} />
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-6">
              <AgentStatusPanel state={state} />
            </div>
            <div className="lg:col-span-6">
              <AgentTerminal events={events} />
            </div>
          </div>
          <ExecutionTimeline events={events} state={state} />
        </div>
      )}

      {activeSubTab === 'services' && (
        <div className="space-y-6">
          <ServiceTopology services={services} trafficTarget={trafficTarget} />
          <LiveMetrics metrics={metrics} />
        </div>
      )}

      {activeSubTab === 'metrics' && (
        <div className="space-y-6">
          <LiveMetrics metrics={metrics} />
          <ServiceTopology services={services} trafficTarget={trafficTarget} />
        </div>
      )}

      {activeSubTab === 'chaos' && (
        <ChaosLab
          scenarios={scenarios}
          activeScenario={activeScenario}
          onScenarioInjected={onScenarioInjected}
          onEnvironmentReset={onReset}
          onRunDemo={onRunDemo}
        />
      )}

      {activeSubTab === 'incidents' && (
        <IncidentDetail state={state} events={events} />
      )}

      {activeSubTab === 'chat' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-6">
            <ChatMission onMissionStarted={() => setActiveSubTab('overview')} />
          </div>
          <div className="lg:col-span-6">
            <AgentTerminal events={events} />
          </div>
        </div>
      )}

      {activeSubTab === 'memory' && <OperationalMemoryView />}

      {activeSubTab === 'architecture' && <ArchitecturePage />}

      {activeSubTab === 'scorecard' && <JudgeScorecard />}

      {activeSubTab === 'settings' && <SettingsView />}
    </div>
  );
};
