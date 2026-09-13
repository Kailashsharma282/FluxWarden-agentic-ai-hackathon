import React from 'react';
import { AlertTriangle, CheckCircle, XCircle, ShieldAlert } from 'lucide-react';

interface ApprovalModalProps {
  isOpen: boolean;
  actionDetails: {
    tool: string;
    impact: string;
    reason: string;
    safety: string;
    params?: Record<string, any>;
  } | null;
  onApprove: () => void;
  onReject: () => void;
}

export const ApprovalModal: React.FC<ApprovalModalProps> = ({
  isOpen,
  actionDetails,
  onApprove,
  onReject
}) => {
  if (!isOpen || !actionDetails) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-lg glass-panel-red p-6 rounded-xl border border-rose-500/40 shadow-[0_0_40px_rgba(239,68,68,0.3)]">
        {/* Header */}
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2.5 rounded-lg bg-rose-500/20 text-rose-400 border border-rose-500/30 animate-pulse">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <span className="px-2 py-0.5 text-[10px] font-mono font-bold tracking-wider rounded bg-rose-500/30 text-rose-300 uppercase">
              HIGH-RISK ACTION GATING
            </span>
            <h3 className="font-heading font-bold text-xl text-white mt-0.5">
              Action Requires Human Approval
            </h3>
          </div>
        </div>

        {/* Content Box */}
        <div className="space-y-3.5 my-5 text-sm">
          <div className="p-3 rounded-lg bg-black/40 border border-white/10 font-mono">
            <span className="text-xs text-slate-400 block uppercase">Proposed Tool</span>
            <span className="text-cyan-300 font-bold text-base">{actionDetails.tool}</span>
          </div>

          <div className="space-y-1">
            <span className="text-xs font-semibold text-rose-400 uppercase tracking-wider block">
              Operational Impact
            </span>
            <p className="text-slate-300 text-xs bg-slate-900/60 p-2.5 rounded border border-white/5">
              {actionDetails.impact}
            </p>
          </div>

          <div className="space-y-1">
            <span className="text-xs font-semibold text-amber-400 uppercase tracking-wider block">
              Reasoning
            </span>
            <p className="text-slate-300 text-xs bg-slate-900/60 p-2.5 rounded border border-white/5">
              {actionDetails.reason}
            </p>
          </div>

          <div className="space-y-1">
            <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider block">
              Safety Verification Guarantee
            </span>
            <p className="text-slate-300 text-xs bg-slate-900/60 p-2.5 rounded border border-white/5">
              {actionDetails.safety}
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-white/10">
          <button
            onClick={onReject}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-white/10 transition-colors"
          >
            <XCircle className="w-4 h-4 text-slate-400" />
            <span>Reject Action</span>
          </button>
          <button
            onClick={onApprove}
            className="flex items-center gap-1.5 px-5 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-heading font-bold shadow-[0_0_20px_rgba(239,68,68,0.4)] transition-all"
          >
            <CheckCircle className="w-4 h-4" />
            <span>Approve & Resume</span>
          </button>
        </div>
      </div>
    </div>
  );
};
