import React from 'react';
import { motion } from 'framer-motion';
import { ServiceNode } from '../types';

interface TopologyCanvasProps {
  services: ServiceNode[];
  trafficTarget: string;
  onSelectService?: (name: string) => void;
}

export const TopologyCanvas: React.FC<TopologyCanvasProps> = ({
  services,
  trafficTarget,
  onSelectService
}) => {
  const isBackup = trafficTarget === 'backup-service';

  return (
    <div className="relative w-full h-full flex flex-col items-center justify-center p-4">
      {/* Dynamic Animated Flow Lines */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none stroke-cyan-500/30">
        <defs>
          <linearGradient id="cyanGlow" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#00f0ff" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.8" />
          </linearGradient>
        </defs>
      </svg>
      <div className="text-center font-mono text-[11px] text-slate-400">
        Active Traffic Route: <span className="text-cyan-400 font-bold">{trafficTarget}</span>
        {isBackup && <span className="ml-2 text-purple-400 font-bold">(Standby Replica Active)</span>}
      </div>
    </div>
  );
};
