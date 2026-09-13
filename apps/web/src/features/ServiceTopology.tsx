import React, { useState } from 'react';
import { Network, Server, Database, Layers, ArrowDown, Activity, Check, AlertOctagon, RefreshCw } from 'lucide-react';
import { ServiceNode } from '../types';

interface ServiceTopologyProps {
  services: ServiceNode[];
  trafficTarget: string;
}

export const ServiceTopology: React.FC<ServiceTopologyProps> = ({ services, trafficTarget }) => {
  const [selectedService, setSelectedService] = useState<string | null>('payment-api');

  const getService = (name: string) => services.find((s) => s.name === name);
  const selectedNode = selectedService ? getService(selectedService) : null;

  const isRoutingToBackup = trafficTarget === 'backup-service';

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'healthy':
        return 'text-emerald-400 border-emerald-500/40 bg-emerald-950/20';
      case 'degraded':
        return 'text-amber-400 border-amber-500/40 bg-amber-950/20 animate-pulse';
      case 'unhealthy':
        return 'text-rose-400 border-rose-500/60 bg-rose-950/30 animate-pulse shadow-[0_0_15px_rgba(239,68,68,0.3)]';
      default:
        return 'text-slate-400 border-white/10 bg-slate-900';
    }
  };

  return (
    <div className="glass-panel p-5 rounded-xl border border-white/10 hover:border-cyan-500/30 transition-all flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between gap-3 mb-4 pb-3 border-b border-white/5">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Network className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-sm tracking-wide text-white uppercase">
              LIVE SERVICE TOPOLOGY & TRAFFIC FLOW
            </h3>
            <span className="text-[10px] font-mono text-slate-400">
              Active Upstream Ingress Target: <strong className={isRoutingToBackup ? 'text-purple-300' : 'text-cyan-300'}>{trafficTarget}</strong>
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2 text-[10px] font-mono">
          <span className="flex items-center gap-1 text-emerald-400">
            <span className="w-2 h-2 rounded-full bg-emerald-400" /> Healthy
          </span>
          <span className="flex items-center gap-1 text-amber-400">
            <span className="w-2 h-2 rounded-full bg-amber-400" /> Degraded
          </span>
          <span className="flex items-center gap-1 text-rose-400">
            <span className="w-2 h-2 rounded-full bg-rose-400" /> Unhealthy
          </span>
        </div>
      </div>

      {/* Interactive Topology Graph Canvas */}
      <div className="relative flex-1 min-h-[360px] flex flex-col items-center justify-between py-2">
        {/* Tier 1: Client Ingress */}
        <div className="flex flex-col items-center z-10">
          <div className="px-4 py-1.5 rounded-lg bg-slate-900 border border-white/20 text-xs font-mono font-bold text-slate-200 shadow-md">
            GLOBAL CLIENT INGRESS
          </div>
          <div className="h-6 w-0.5 bg-gradient-to-b from-slate-400 to-cyan-500 my-0.5 animate-pulse" />
        </div>

        {/* Tier 2: Traffic Router */}
        <div className="z-10">
          {(() => {
            const router = getService('traffic-router');
            return (
              <div
                onClick={() => setSelectedService('traffic-router')}
                className={`cursor-pointer px-5 py-2 rounded-xl border font-mono text-xs flex items-center gap-3 transition-all ${getStatusColor(
                  router?.status
                )} ${selectedService === 'traffic-router' ? 'ring-2 ring-cyan-400' : ''}`}
              >
                <Layers className="w-4 h-4 text-cyan-400" />
                <div>
                  <span className="font-bold block text-white">traffic-router</span>
                  <span className="text-[10px] text-slate-400">Gateway • Ingress Split 100%</span>
                </div>
              </div>
            );
          })()}
        </div>

        {/* Tier 3: Primary (payment-api) vs Standby Replica (backup-service) */}
        <div className="w-full max-w-xl grid grid-cols-2 gap-6 my-3 z-10">
          {/* Primary Payment API Node */}
          {(() => {
            const pay = getService('payment-api');
            const isActive = !isRoutingToBackup;
            return (
              <div
                onClick={() => setSelectedService('payment-api')}
                className={`relative cursor-pointer p-3.5 rounded-xl border font-mono text-xs transition-all ${getStatusColor(
                  pay?.status
                )} ${selectedService === 'payment-api' ? 'ring-2 ring-cyan-400' : ''}`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="font-bold text-white text-xs">payment-api</span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-black/40 text-slate-300">
                    {pay?.version}
                  </span>
                </div>
                <div className="text-[11px] space-y-0.5 text-slate-300">
                  <div className="flex justify-between">
                    <span>Error Rate:</span>
                    <strong className={pay && pay.error_rate > 0.1 ? 'text-rose-400' : 'text-slate-200'}>
                      {pay ? (pay.error_rate * 100).toFixed(1) : 0}%
                    </strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Latency:</span>
                    <strong className={pay && pay.latency_ms > 200 ? 'text-rose-400' : 'text-slate-200'}>
                      {pay?.latency_ms}ms
                    </strong>
                  </div>
                </div>
                {isActive ? (
                  <div className="mt-2 text-[10px] font-bold text-cyan-400 uppercase tracking-widest flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
                    RECEIVING TRAFFIC
                  </div>
                ) : (
                  <div className="mt-2 text-[10px] text-slate-500 font-semibold uppercase">
                    TRAFFIC REROUTED AWAY
                  </div>
                )}
              </div>
            );
          })()}

          {/* Standby Replica (backup-service) Node */}
          {(() => {
            const backup = getService('backup-service');
            const isActive = isRoutingToBackup;
            return (
              <div
                onClick={() => setSelectedService('backup-service')}
                className={`relative cursor-pointer p-3.5 rounded-xl border font-mono text-xs transition-all ${getStatusColor(
                  backup?.status
                )} ${selectedService === 'backup-service' ? 'ring-2 ring-purple-400' : ''} ${
                  isActive ? 'shadow-[0_0_25px_rgba(168,85,247,0.3)] border-purple-400' : ''
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="font-bold text-white text-xs">backup-service</span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-purple-950/60 text-purple-200 border border-purple-500/30">
                    {backup?.version}
                  </span>
                </div>
                <div className="text-[11px] space-y-0.5 text-slate-300">
                  <div className="flex justify-between">
                    <span>Status:</span>
                    <strong className="text-emerald-400">100% HEALTHY</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Latency:</span>
                    <strong className="text-slate-200">{backup?.latency_ms}ms</strong>
                  </div>
                </div>
                {isActive ? (
                  <div className="mt-2 text-[10px] font-bold text-purple-300 uppercase tracking-widest flex items-center gap-1 animate-pulse">
                    <Check className="w-3 h-3 text-purple-400" />
                    ACTIVE FAILOVER TARGET
                  </div>
                ) : (
                  <div className="mt-2 text-[10px] text-slate-400 font-semibold uppercase">
                    STANDBY REPLICA READY
                  </div>
                )}
              </div>
            );
          })()}
        </div>

        {/* Tier 4: Downstream Database & Cache Infrastructure */}
        <div className="w-full max-w-2xl grid grid-cols-2 sm:grid-cols-4 gap-3 z-10">
          {['postgres', 'redis', 'auth-service', 'order-service'].map((svcName) => {
            const svc = getService(svcName);
            return (
              <div
                key={svcName}
                onClick={() => setSelectedService(svcName)}
                className={`cursor-pointer p-2.5 rounded-lg border font-mono text-[11px] transition-all ${getStatusColor(
                  svc?.status
                )} ${selectedService === svcName ? 'ring-2 ring-cyan-400' : ''}`}
              >
                <span className="font-bold block text-white truncate">{svcName}</span>
                <span className="text-[10px] text-slate-400 capitalize">{svc?.status || 'Active'}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Selected Node Inspector Tray */}
      {selectedNode && (
        <div className="mt-3 pt-3 border-t border-white/5 flex flex-wrap items-center justify-between gap-3 text-xs font-mono bg-black/30 p-2.5 rounded-lg">
          <div>
            <span className="text-cyan-400 font-bold uppercase">{selectedNode.name}</span>
            <span className="text-slate-400 ml-2">({selectedNode.display_name})</span>
          </div>
          <div className="flex items-center gap-4 text-[11px]">
            <span>CPU: <strong>{selectedNode.cpu}%</strong></span>
            <span>RAM: <strong>{selectedNode.memory}%</strong></span>
            <span>Requests: <strong>{selectedNode.request_rate} r/s</strong></span>
          </div>
        </div>
      )}
    </div>
  );
};
