import React, { useEffect, useRef, useState } from 'react';
import { connectBus, BusFrameOut } from '../api/busStream';
import { AetherRenderer } from '../gpu/renderer';

function App() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rendererRef = useRef<AetherRenderer | null>(null);
  const [status, setStatus] = useState<string>('Connecting...');
  const [irData, setIrData] = useState<any>(null);

  useEffect(() => {
    if (canvasRef.current && !rendererRef.current) {
      rendererRef.current = new AetherRenderer(canvasRef.current);
    }

    const ws = connectBus((frame: BusFrameOut) => {
      setStatus(`Connected | Governor: ${frame.governor_status} | Entropy: ${frame.shannon_entropy.toFixed(4)}`);
      setIrData(frame.ir);
      if (rendererRef.current) {
        rendererRef.current.update(frame.ir);
      }
    });

    return () => {
      ws.close();
    };
  }, []);

  const sendIntent = () => {
    // Demo sending an intent to trigger state changes over WebSocket
    // Real implementation would have a robust WS connection instance
  };

  return (
    <div style={{ width: '100vw', height: '100vh', backgroundColor: '#0B1026', color: 'white', overflow: 'hidden' }}>
      <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 10 }}>
        <h1>Aetherium Manifest</h1>
        <p>Status: {status}</p>
        <pre style={{fontSize: '10px'}}>{JSON.stringify(irData, null, 2)}</pre>
      </div>
      <canvas ref={canvasRef} style={{ display: 'block', width: '100%', height: '100%' }} />
    </div>
  );
}

export default App;
