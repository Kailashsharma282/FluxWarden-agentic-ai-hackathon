import { useEffect, useState, useCallback } from 'react';
import { realtimeStream, api } from '../services/api';
import { AgentEvent, AgentState } from '../types';

export function useAgentEvents() {
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [state, setState] = useState<AgentState | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'reconnecting' | 'disconnected'>('disconnected');

  const refreshState = useCallback(async () => {
    try {
      const res = await api.getIncidentState('INC-1042');
      if (res && res.incident_id !== 'NONE') {
        setState(res);
      }
    } catch {
      // Graceful fallback
    }
  }, []);

  useEffect(() => {
    realtimeStream.connect();
    setConnectionStatus('connected');

    const unsubscribe = realtimeStream.subscribe((payload: any) => {
      if (payload.type === 'INITIAL_STATE') {
        if (payload.state) setState(payload.state);
        if (payload.events) setEvents(payload.events);
      } else if (payload.type) {
        setEvents((prev) => {
          if (prev.some((e) => e.id === payload.id)) return prev;
          return [...prev, payload];
        });
        refreshState();
      }
    });

    return () => {
      unsubscribe();
    };
  }, [refreshState]);

  return { events, state, connectionStatus, refreshState };
}
