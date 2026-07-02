import { WS_BASE_URL } from '../core/config';

export interface BusFrameIn {
  intent_id: string;
  context_vector: string;
  emotional_valence: number;
  energy_level: number;
}

export interface BusFrameOut {
  intent_id: string;
  contract: any;               // later strongly typed with ManifestContract
  governor_status: string;
  shannon_entropy: number;
}

export function connectBus(
  onFrame: (frame: BusFrameOut) => void,
): WebSocket {
  const ws = new WebSocket(`${WS_BASE_URL}/v4/bus/stream`);

  ws.onmessage = (event) => {
    const frame: BusFrameOut = JSON.parse(event.data);
    onFrame(frame);
  };

  return ws;
}
