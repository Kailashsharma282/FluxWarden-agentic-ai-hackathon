import React, { useState, useEffect, useCallback } from 'react';
import { Navbar } from '../components/Navbar';
import { BackgroundCanvas } from '../components/BackgroundCanvas';
import { ApprovalModal } from '../components/ApprovalModal';
import { CommandPalette } from '../components/CommandPalette';
import { LandingPage } from '../features/LandingPage';
import { CommandCenter } from '../features/CommandCenter';
import { api, realtimeStream } from '../services/api';
import { AgentEvent, AgentState, MetricsSnapshot, Scenario, ServiceNode } from '../types';

export const App: React.FC = () => {
  // Navigation & View State
  const [currentView, setCurrentView] = useState<'landing' | 'command'>('landing');
  const [activeSubTab, setActiveSubTab] = useState<string>('overview');
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);

  // System & Telemetry State
  const [systemStatus, setSystemStatus] = useState<string>('OPERATIONAL');
  const [services, setServices] = useState<ServiceNode[]>([]);
  const [metrics, setMetrics] = useState<MetricsSnapshot | null>(null);
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [activeScenario, setActiveScenario] = useState<string | null>(null);
  const [trafficTarget, setTrafficTarget] = useState<string>('payment-api');

  // Agent State & Events
  const [agentState, setAgentState] = useState<AgentState | null>(null);
  const [events, setEvents] = useState<AgentEvent[]>([]);

  // Polling data refresh
  const refreshData = useCallback(async () => {
    try {
      const [statusRes, servicesRes, metricsRes, scenariosRes] = await Promise.all([
        api.getSystemStatus(),
        api.getServices(),
        api.getMetrics(),
        api.getScenarios()
      ]);

      setSystemStatus(statusRes.overall_status);
      setTrafficTarget(statusRes.traffic_target || 'payment-api');
      setServices(servicesRes.services || []);
      setMetrics(metricsRes.metrics || null);
      setScenarios(scenariosRes.scenarios || []);
      setActiveScenario(scenariosRes.active_scenario || null);

      // Fetch active incident state if present
      const stateRes = await api.getIncidentState('INC-1042');
      if (stateRes && stateRes.incident_id !== 'NONE') {
        setAgentState(stateRes);
      }
    } catch (err) {
      console.warn('API polling error:', err);
    }
  }, []);

  // Initial mount & WebSocket subscription
  useEffect(() => {
    refreshData();
    const interval = setInterval(refreshData, 2000);

    realtimeStream.connect();
    const unsubscribe = realtimeStream.subscribe((payload: any) => {
      if (payload.type === 'INITIAL_STATE') {
        if (payload.state) setAgentState(payload.state);
        if (payload.events) setEvents(payload.events);
      } else if (payload.type) {
        // Individual AgentEvent payload
        setEvents((prev) => {
          if (prev.some((e) => e.id === payload.id)) return prev;
          return [...prev, payload];
        });
        refreshData();
      }
    });

    return () => {
      clearInterval(interval);
      unsubscribe();
    };
  }, [refreshData]);

  // Global Keyboard Shortcuts (Section 49)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't trigger shortcuts if typing inside an input or textarea
      if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) {
        return;
      }

      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsCommandPaletteOpen((prev) => !prev);
      } else if (e.key.toLowerCase() === 'c') {
        setCurrentView('command');
        setActiveSubTab('chat');
      } else if (e.key.toLowerCase() === 'r') {
        refreshData();
      } else if (e.key.toLowerCase() === 'd') {
        handleRunDemo();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [refreshData]);

  // Actions
  const handleRunDemo = async () => {
    setCurrentView('command');
    setActiveSubTab('overview');
    try {
      await api.runDemo();
      refreshData();
    } catch (e) {
      console.error(e);
    }
  };

  const handleReset = async () => {
    try {
      await api.resetEnvironment();
      setAgentState(null);
      setEvents([]);
      refreshData();
    } catch (e) {
      console.error(e);
    }
  };

  const handleApproveAction = async () => {
    if (agentState?.incident_id) {
      await api.approveAction(agentState.incident_id);
      refreshData();
    }
  };

  const handleRejectAction = async () => {
    if (agentState?.incident_id) {
      await api.rejectAction(agentState.incident_id);
      refreshData();
    }
  };

  const isAgentActive =
    !!agentState &&
    !['IDLE', 'COMPLETE', 'FAILED'].includes(agentState.current_phase);

  return (
    <div className="min-h-screen bg-[#0a0d14] text-slate-100 flex flex-col relative">
      {/* Background canvas effects (Section 29) */}
      <BackgroundCanvas />

      {/* Top Navigation Bar */}
      <Navbar
        activeTab={currentView}
        setActiveTab={(tab) => {
          if (tab === 'overview') {
            setCurrentView('command');
            setActiveSubTab('overview');
          }
        }}
        systemStatus={systemStatus}
        onRunDemo={handleRunDemo}
        onReset={handleReset}
        onOpenCommandPalette={() => setIsCommandPaletteOpen(true)}
        isAgentActive={isAgentActive}
      />

      {/* Main View Area */}
      <main className="flex-1 relative z-10">
        {currentView === 'landing' ? (
          <LandingPage
            onLaunch={() => setCurrentView('command')}
            onViewArchitecture={() => {
              setCurrentView('command');
              setActiveSubTab('architecture');
            }}
            onRunDemo={handleRunDemo}
          />
        ) : (
          <CommandCenter
            activeSubTab={activeSubTab}
            setActiveSubTab={setActiveSubTab}
            state={agentState}
            events={events}
            services={services}
            metrics={metrics}
            scenarios={scenarios}
            activeScenario={activeScenario}
            trafficTarget={trafficTarget}
            onRunDemo={handleRunDemo}
            onReset={handleReset}
            onScenarioInjected={refreshData}
          />
        )}
      </main>

      {/* Human Approval Modal (Section 22 & 42) */}
      <ApprovalModal
        isOpen={!!agentState?.approval_required}
        actionDetails={agentState?.pending_approval_action || null}
        onApprove={handleApproveAction}
        onReject={handleRejectAction}
      />

      {/* Command Palette (Section 49) */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onSelectTab={(tab) => {
          setCurrentView('command');
          setActiveSubTab(tab);
        }}
        onRunDemo={handleRunDemo}
        onReset={handleReset}
        onInjectBadDeployment={async () => {
          setCurrentView('command');
          setActiveSubTab('overview');
          await api.injectScenario('bad_deployment');
          refreshData();
        }}
      />
    </div>
  );
};
