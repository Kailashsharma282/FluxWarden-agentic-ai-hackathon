import React, { useState } from 'react';
import { Cpu, ArrowDown, Database, Shield, Zap, Layers, GitBranch, RefreshCw, CheckCircle2, User, Globe, Code } from 'lucide-react';

interface ComponentDetail {
  id: string;
  name: string;
  category: string;
  responsibility: string;
  inputs: string[];
  outputs: string[];
  technologies: string[];
}

export const ArchitecturePage: React.FC = () => {
  const [selectedId, setSelectedId] = useState<string>('agent_controller');

  const components: ComponentDetail[] = [
    {
      id: 'user',
      name: 'Human Operator / Judge',
      category: 'Client',
      responsibility: 'Issues high-level incident objectives and provides approval on high-risk gated operations.',
      inputs: ['Operational alerts', 'SLO breach notifications'],
      outputs: ['Natural language mission prompt', 'Approval decisions (Approve/Reject)'],
      technologies: ['Human SRE', 'IIT BBS Hackathon Judge']
    },
    {
      id: 'web_application',
      name: 'Web Application Command Center',
      category: 'Frontend',
      responsibility: 'Renders real-time telemetry, topology graphs, execution timelines, and monospace terminals with glassmorphism UI.',
      inputs: ['WebSocket event stream', 'REST telemetry endpoints'],
      outputs: ['HTTP API requests', 'User commands', 'Approval actions'],
      technologies: ['React 18', 'Vite', 'TypeScript', 'Tailwind CSS', 'HTML5 Canvas']
    },
    {
      id: 'fastapi',
      name: 'FastAPI Gateway API',
      category: 'API Layer',
      responsibility: 'High-throughput async gateway providing REST endpoints and WebSocket broadcasting with structured JSON logging.',
      inputs: ['HTTP requests from frontend', 'Agent internal events'],
      outputs: ['JSON responses', 'WebSocket broadcast stream'],
      technologies: ['FastAPI', 'Uvicorn', 'Pydantic v2', 'Starlette WebSockets']
    },
    {
      id: 'agent_controller',
      name: 'Agent Controller (Cognitive Brain)',
      category: 'Agentic Core',
      responsibility: 'Manages incident lifecycle, step loops, cognitive decisions, and maintains strongly typed AgentState across turns.',
      inputs: ['Mission goal', 'Live service telemetry', 'Tool execution outputs'],
      outputs: ['Action plans', 'Structured explanations', 'Real-time AgentEvents'],
      technologies: ['Python 3.13', 'AsyncIO', 'Multi-Provider Abstraction']
    },
    {
      id: 'state_graph',
      name: 'Agent State Graph (Explicit FSM)',
      category: 'State Machine',
      responsibility: 'Enforces strict finite-state graph transitions (LangGraph architectural model) preventing uncontrolled infinite loops.',
      inputs: ['Current phase', 'Action results'],
      outputs: ['Valid next phase transitions', 'Bounded step guards'],
      technologies: ['Finite State Machine', 'Enum state validation']
    },
    {
      id: 'tool_router',
      name: 'Tool Router & Risk Engine',
      category: 'Safety & Gating',
      responsibility: 'Validates input schemas, enforces execution timeouts, classifies risk levels (LOW/MED/HIGH/CRIT), and halts for human approvals.',
      inputs: ['Tool invocation requests', 'Tool parameters'],
      outputs: ['Authorized tool dispatch or WAITING_FOR_APPROVAL halt'],
      technologies: ['Pydantic Schema Validation', 'Risk Classification Matrix']
    },
    {
      id: 'tool_registry',
      name: 'Tool Registry (39 Tools)',
      category: 'Execution Layer',
      responsibility: 'Houses 39 distinct tools across Diagnostic, Remediation, Verification, and Safety categories.',
      inputs: ['Validated parameters'],
      outputs: ['Structured ToolResult payloads'],
      technologies: ['Python Async Handlers', 'Strict Input/Output typing']
    },
    {
      id: 'simulation_env',
      name: 'Simulated Production Environment',
      category: 'Infrastructure Sandbox',
      responsibility: 'Simulates 10 microservices, traffic routing, error rates, latencies, CPU/RAM telemetry, and chaos fault injection.',
      inputs: ['Remediation tool actions', 'Chaos injection commands'],
      outputs: ['Live cluster metrics', 'Stderr logs', 'Deployment manifests'],
      technologies: ['In-Memory Cluster State', 'PostgreSQL / SQLite', 'Redis']
    },
    {
      id: 'observation',
      name: 'Observation & Evidence Collector',
      category: 'Cognitive Layer',
      responsibility: 'Aggregates telemetry, stderr logs, and deployment anomalies into structured evidence for hypothesis formulation.',
      inputs: ['Raw diagnostic tool outputs'],
      outputs: ['Correlated evidence tokens', 'Telemetry observations'],
      technologies: ['Pattern correlation', 'Log index parser']
    },
    {
      id: 'evaluator',
      name: 'Evaluator & Verification Engine',
      category: 'Verification Core',
      responsibility: 'Guarantees {"success": true} never marks an incident resolved. Runs 6 independent verification probes before resolving.',
      inputs: ['Remediation outcome', 'Cluster telemetry'],
      outputs: ['Verification passed/failed decisions', 'Audit checklist'],
      technologies: ['Multi-probe synthetic verification', 'ACID integrity probes']
    },
    {
      id: 'replanner',
      name: 'Replanner & Operational Memory',
      category: 'Adaptation Core',
      responsibility: 'Detects remediation failure, recalls past incident recoveries from Operational Memory, and dynamically adapts strategy.',
      inputs: ['Failure error signatures', 'Historical resolution memories'],
      outputs: ['Alternative recovery strategy (e.g. Ingress rerouting)'],
      technologies: ['Operational Memory Store', 'Adaptive Fallback Heuristics']
    }
  ];

  const selected = components.find((c) => c.id === selectedId) || components[3];

  return (
    <div className="space-y-6">
      {/* Page Title */}
      <div className="glass-panel p-6 rounded-2xl border border-white/10 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
              <Cpu className="w-5 h-5" />
            </div>
            <h2 className="font-heading font-extrabold text-xl text-white tracking-wide">
              INTERACTIVE ARCHITECTURAL EXPLORER
            </h2>
          </div>
          <p className="text-xs text-slate-400 font-mono">
            Click any architectural component to reveal its responsibilities, input/output contracts, and tech stack.
          </p>
        </div>
      </div>

      {/* Two Column Layout: Diagram on Left, Deep Inspector on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Interactive Diagram Nodes */}
        <div className="lg:col-span-7 glass-panel p-5 rounded-xl border border-white/10 space-y-2">
          {components.map((comp, idx) => {
            const isSelected = comp.id === selectedId;
            return (
              <React.Fragment key={comp.id}>
                <div
                  onClick={() => setSelectedId(comp.id)}
                  className={`cursor-pointer p-3 rounded-xl border transition-all flex items-center justify-between font-mono text-xs ${
                    isSelected
                      ? 'bg-cyan-950/40 border-cyan-400 shadow-[0_0_20px_rgba(0,240,255,0.25)] ring-1 ring-cyan-400 text-white'
                      : 'bg-black/30 border-white/5 hover:border-cyan-500/30 text-slate-300'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-md bg-slate-800 flex items-center justify-center text-[10px] text-cyan-400 font-bold">
                      {idx + 1}
                    </span>
                    <div>
                      <span className="font-bold text-sm block">{comp.name}</span>
                      <span className="text-[10px] text-slate-400 uppercase tracking-widest">
                        {comp.category}
                      </span>
                    </div>
                  </div>
                  <span className="text-[10px] text-cyan-400 px-2 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/20">
                    Inspect
                  </span>
                </div>

                {idx < components.length - 1 && (
                  <div className="flex justify-center py-0.5">
                    <ArrowDown className="w-3.5 h-3.5 text-cyan-500/50 animate-pulse" />
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>

        {/* Right Column: Deep-Dive Component Inspector */}
        <div className="lg:col-span-5">
          <div className="glass-panel p-6 rounded-xl border border-cyan-500/30 sticky top-20 shadow-[0_0_30px_rgba(0,0,0,0.5)] space-y-4">
            <div className="border-b border-white/10 pb-3">
              <span className="text-[10px] font-mono text-cyan-400 uppercase font-bold tracking-widest block mb-1">
                COMPONENT INSPECTOR
              </span>
              <h3 className="font-heading font-extrabold text-xl text-white">{selected.name}</h3>
              <span className="text-xs font-mono text-slate-400">{selected.category}</span>
            </div>

            {/* Responsibility */}
            <div>
              <span className="text-[10px] font-mono font-bold uppercase text-slate-400 tracking-wider block mb-1">
                Responsibility
              </span>
              <p className="text-xs text-slate-200 leading-relaxed bg-black/40 p-3 rounded-lg border border-white/5 font-mono">
                {selected.responsibility}
              </p>
            </div>

            {/* Inputs */}
            <div>
              <span className="text-[10px] font-mono font-bold uppercase text-purple-400 tracking-wider block mb-1">
                Inputs
              </span>
              <ul className="space-y-1 font-mono text-xs text-slate-300">
                {selected.inputs.map((inp, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="text-purple-400">❯</span>
                    <span>{inp}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Outputs */}
            <div>
              <span className="text-[10px] font-mono font-bold uppercase text-emerald-400 tracking-wider block mb-1">
                Outputs
              </span>
              <ul className="space-y-1 font-mono text-xs text-slate-300">
                {selected.outputs.map((out, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="text-emerald-400">❯</span>
                    <span>{out}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Technologies */}
            <div>
              <span className="text-[10px] font-mono font-bold uppercase text-cyan-400 tracking-wider block mb-1.5">
                Technologies
              </span>
              <div className="flex flex-wrap gap-1.5 font-mono text-[10px]">
                {selected.technologies.map((tech, i) => (
                  <span
                    key={i}
                    className="px-2 py-1 rounded bg-slate-900 border border-white/10 text-cyan-300"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
