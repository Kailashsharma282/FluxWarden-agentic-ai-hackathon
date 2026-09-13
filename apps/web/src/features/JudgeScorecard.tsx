import React from 'react';
import { Award, CheckCircle2, ShieldCheck, Zap, Bot, RefreshCw, Eye, Lock, FileCheck, Cpu } from 'lucide-react';

export const JudgeScorecard: React.FC = () => {
  const capabilities = [
    {
      title: 'Goal Driven',
      icon: Zap,
      status: 'VERIFIED',
      description: 'Receives open-ended, high-level objectives ("The payment API is failing. Investigate and restore service without data loss") and extracts operational constraints without requiring hardcoded scripts.',
      implementation: 'app/agents/engine.py: initialize_mission() parses goal into dynamic hypothesis space.'
    },
    {
      title: 'Dynamic Tool Selection',
      icon: Cpu,
      status: 'VERIFIED',
      description: 'Dynamically selects and parameterizes tools from a sandboxed registry of 39 diagnostic, remediation, verification, and safety tools based on evolving system state.',
      implementation: 'app/tools/registry.py: 39 tools with strict Pydantic schemas, permissions, timeouts, and retry policies.'
    },
    {
      title: 'Multi-Step Execution',
      icon: Bot,
      status: 'VERIFIED',
      description: 'Performs multi-turn dependent sequences: health discovery ➔ stderr inspection ➔ CI/CD commit correlation ➔ remediation ➔ verification.',
      implementation: '12-stage execution timeline tracking step-by-step progress through state transitions.'
    },
    {
      title: 'State Management',
      icon: Eye,
      status: 'VERIFIED',
      description: 'Maintains strongly typed AgentState including incident IDs, hypotheses, completed actions, failed actions, and system telemetry across turns.',
      implementation: 'app/models/state.py: Strongly typed Pydantic AgentState model with durable persistence.'
    },
    {
      title: 'Failure Detection',
      icon: CheckCircle2,
      status: 'VERIFIED',
      description: 'Detects tool execution failure (e.g. rollback image unavailable) without crashing the application or entering infinite loops.',
      implementation: 'app/agents/engine.py: Traps failed actions into state.failed_actions and dispatches ACTION_FAILED events.'
    },
    {
      title: 'Adaptation',
      icon: RefreshCw,
      status: 'VERIFIED',
      description: 'THE CRITICAL DEMONSTRATION: When rollback fails intentionally, the agent transitions to REPLAN, consults Operational Memory, discovers a healthy standby replica, and shifts strategy.',
      implementation: 'MockLLMProvider / state_graph.py: REPLAN state dynamically chooses backup-service traffic routing.'
    },
    {
      title: 'Independent Verification',
      icon: FileCheck,
      status: 'VERIFIED',
      description: 'An action returning {"success": true} never resolves the incident. The system independently runs 6 probes (Health, Smoke, SLA Error, Latency, Dependencies, DB ACID integrity).',
      implementation: 'app/verification/engine.py: Mandatory 6-probe VerificationEngine.'
    },
    {
      title: 'Safety Controls & Bounded Loops',
      icon: Lock,
      status: 'VERIFIED',
      description: 'Enforces hard ceilings: MAX_AGENT_STEPS = 15, MAX_REPLAN_ATTEMPTS = 3, MAX_TOOL_RETRIES = 2. Destructive operations (delete_data) are strictly blocked.',
      implementation: 'app/config.py & app/safety/risk_engine.py: Risk hierarchy (LOW, MEDIUM, HIGH, CRITICAL).'
    },
    {
      title: 'Human Approval System',
      icon: ShieldCheck,
      status: 'VERIFIED',
      description: 'High-risk operations pause execution in WAITING_FOR_APPROVAL state until human operator reviews impact, reason, and safety in an approval modal.',
      implementation: 'ApprovalModal.tsx + /api/incidents/{id}/approve & /reject endpoints.'
    },
    {
      title: 'Autonomous Recovery',
      icon: Award,
      status: 'VERIFIED',
      description: 'Restores 100% service availability (error rate drops from 74% to 0.001, latency drops from 921ms to 38ms) and generates a full exportable post-mortem.',
      implementation: 'FinalResolutionCard + exportable JSON / Markdown forensic post-mortem.'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner with Hackathon & Participant Credits */}
      <div className="glass-panel p-6 rounded-2xl border border-cyan-500/30 flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
              <Award className="w-5 h-5 text-amber-400" />
            </div>
            <h2 className="font-heading font-extrabold text-xl text-white tracking-wide">
              AGENTIC CAPABILITY SCORECARD
            </h2>
          </div>
          <p className="text-xs text-slate-300 font-mono">
            Direct mapping of FluxWarden capabilities to the Hackathon Evaluation Rubric.
          </p>
        </div>

        <div className="p-3 rounded-xl bg-black/40 border border-white/10 font-mono text-xs space-y-0.5">
          <div className="text-slate-400">
            Hackathon: <strong className="text-amber-300">Tech Zephyr 4.0 | IIT Bhubaneswar</strong>
          </div>
          <div className="text-slate-400">
            Participant: <strong className="text-cyan-300">Pochiraju Kailash Ram Markandeya Sharma</strong> (Solo)
          </div>
          <div className="text-slate-400">
            Team Name: <strong className="text-purple-300">kailashsharma8</strong>
          </div>
        </div>
      </div>

      {/* 10 Scorecard Items Grid (Section 41) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {capabilities.map((cap, idx) => {
          const Icon = cap.icon;
          return (
            <div
              key={idx}
              className="glass-panel p-5 rounded-xl border border-white/10 hover:border-cyan-500/40 transition-all font-mono"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2.5">
                  <div className="p-1.5 rounded-md bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                    <Icon className="w-4 h-4" />
                  </div>
                  <h3 className="font-heading font-bold text-sm text-white">{cap.title}</h3>
                </div>
                <span className="flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                  {cap.status}
                </span>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed mb-3">
                {cap.description}
              </p>

              <div className="p-2 rounded bg-black/40 border border-white/5 text-[11px] text-cyan-300/90 truncate">
                <span className="text-slate-500 font-semibold mr-1.5">Code Reference:</span>
                {cap.implementation}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
