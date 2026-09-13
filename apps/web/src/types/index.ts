export interface StructuredExplanation {
  current_action: string;
  why: string;
  expected_result: string;
  risk: string;
  result: string;
  adaptation: string;
}

export interface AgentState {
  incident_id: string;
  user_goal: string;
  constraints: string[];
  current_phase: string;
  observations: string[];
  hypotheses: string[];
  selected_actions: string[];
  completed_actions: string[];
  failed_actions: Array<{ tool: string; error?: string; timestamp?: string }>;
  tool_results: any[];
  system_state: Record<string, any>;
  risk_level: string;
  approval_required: boolean;
  pending_approval_action?: {
    tool: string;
    params: Record<string, any>;
    impact: string;
    reason: string;
    safety: string;
  } | null;
  attempt_count: number;
  replan_count: number;
  resolution_status: string;
  final_report?: Record<string, any> | null;
  structured_explanation?: StructuredExplanation | null;
}

export interface AgentEvent {
  id: string;
  incident_id: string;
  timestamp: string;
  time_display: string;
  type: string;
  tool?: string | null;
  summary: string;
  severity: 'info' | 'warning' | 'error' | 'success' | 'critical';
  details?: Record<string, any> | null;
}

export interface ServiceNode {
  name: string;
  display_name: string;
  type: string;
  status: 'healthy' | 'degraded' | 'unhealthy' | 'disabled';
  health_score: number;
  version: string;
  cpu: number;
  memory: number;
  error_rate: number;
  latency_ms: number;
  request_rate: number;
  dependencies: string[];
  configuration: Record<string, any>;
  active_target?: boolean;
}

export interface Scenario {
  id: string;
  title: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  description: string;
  symptoms: string;
  affected_services: string[];
  adaptation_flow: string;
}

export interface MetricsSnapshot {
  timestamp: string;
  request_rate: number;
  error_rate: number;
  latency_ms: number;
  cpu_percent: number;
  memory_percent: number;
  db_connections: number;
  traffic_target: string;
  active_services: number;
}
