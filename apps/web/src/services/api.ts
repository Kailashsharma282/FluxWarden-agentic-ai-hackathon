import { AgentEvent, AgentState, MetricsSnapshot, Scenario, ServiceNode } from '../types';

const RAW_API_URL = (import.meta as any).env?.VITE_API_URL || '';
const API_BASE = RAW_API_URL ? `${RAW_API_URL.replace(/\/+$/, '')}/api` : '/api';

export const api = {
  async getSystemStatus() {
    const res = await fetch(`${API_BASE}/system/status`);
    return res.json();
  },

  async getServices(): Promise<{ services: ServiceNode[] }> {
    const res = await fetch(`${API_BASE}/system/services`);
    return res.json();
  },

  async getMetrics(): Promise<{ metrics: MetricsSnapshot }> {
    const res = await fetch(`${API_BASE}/system/metrics`);
    return res.json();
  },

  async getSettings() {
    const res = await fetch(`${API_BASE}/system/settings`);
    return res.json();
  },

  async updateSettings(payload: any) {
    const res = await fetch(`${API_BASE}/system/settings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async getScenarios(): Promise<{ scenarios: Scenario[]; active_scenario: string | null }> {
    const res = await fetch(`${API_BASE}/scenarios`);
    return res.json();
  },

  async injectScenario(scenario_id: string) {
    const res = await fetch(`${API_BASE}/scenarios/inject`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_id })
    });
    return res.json();
  },

  async resetEnvironment() {
    const res = await fetch(`${API_BASE}/scenarios/reset`, { method: 'POST' });
    return res.json();
  },

  async getIncidentState(id: string): Promise<AgentState> {
    const res = await fetch(`${API_BASE}/incidents/${id}/state`);
    return res.json();
  },

  async getIncidentEvents(id: string): Promise<{ events: AgentEvent[] }> {
    const res = await fetch(`${API_BASE}/incidents/${id}/events`);
    return res.json();
  },

  async sendChatMessage(message: string) {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    return res.json();
  },

  async runDemo(step_delay = 0.9) {
    const res = await fetch(`${API_BASE}/demo/run?step_delay=${step_delay}`, { method: 'POST' });
    return res.json();
  },

  async approveAction(incident_id: string) {
    const res = await fetch(`${API_BASE}/incidents/${incident_id}/approve`, { method: 'POST' });
    return res.json();
  },

  async rejectAction(incident_id: string, reason?: string) {
    const res = await fetch(`${API_BASE}/incidents/${incident_id}/reject`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason: reason || 'Operator rejected action' })
    });
    return res.json();
  }
};

export class RealtimeStream {
  private ws: WebSocket | null = null;
  private subscribers: Array<(event: AgentEvent | { type: string; state?: AgentState; events?: AgentEvent[] }) => void> = [];
  private isConnecting = false;

  connect() {
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return;
    }
    this.isConnecting = true;

    let wsUrl: string;
    if (RAW_API_URL) {
      try {
        const url = new URL(RAW_API_URL);
        const wsProtocol = url.protocol === 'https:' ? 'wss:' : 'ws:';
        wsUrl = `${wsProtocol}//${url.host}/ws/events`;
      } catch (e) {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        wsUrl = `${protocol}//${window.location.host}/ws/events`;
      }
    } else {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.host;
      wsUrl = `${protocol}//${host}/ws/events`;
    }

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        this.isConnecting = false;
        console.log('[FluxWarden WS] Connected to live agent event stream at', wsUrl);
      };

      this.ws.onmessage = (messageEvent) => {
        try {
          const payload = JSON.parse(messageEvent.data);
          this.subscribers.forEach((sub) => sub(payload));
        } catch (err) {
          console.error('[FluxWarden WS] Error parsing payload:', err);
        }
      };

      this.ws.onclose = () => {
        this.isConnecting = false;
        setTimeout(() => this.connect(), 2000);
      };

      this.ws.onerror = () => {
        this.isConnecting = false;
        this.ws?.close();
      };
    } catch (e) {
      this.isConnecting = false;
      setTimeout(() => this.connect(), 2500);
    }
  }

  subscribe(callback: (event: any) => void) {
    this.subscribers.push(callback);
    return () => {
      this.subscribers = this.subscribers.filter((s) => s !== callback);
    };
  }
}

export const realtimeStream = new RealtimeStream();
