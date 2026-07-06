import { useEffect, useRef, useState } from 'react';
import { connectBus, BusFrameOut } from '../api/busStream';
import { AetherRenderer, RenderProfileResolver, ManifestContract } from '../gpu/renderer';

function App() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rendererRef = useRef<AetherRenderer | null>(null);
  const resolverRef = useRef<RenderProfileResolver>(new RenderProfileResolver());
  const [status, setStatus] = useState<string>('Connecting...');
  const [contractData, setContractData] = useState<any>(null);

  useEffect(() => {
    if (canvasRef.current && !rendererRef.current) {
      rendererRef.current = new AetherRenderer(canvasRef.current);
      rendererRef.current.resize(window.innerWidth, window.innerHeight);
    }

    const handleResize = () => {
      if (rendererRef.current) {
        rendererRef.current.resize(window.innerWidth, window.innerHeight);
      }
    };
    window.addEventListener('resize', handleResize);

    const ws = connectBus((frame: BusFrameOut) => {
      setStatus(`Connected | Governor: ${frame.governor_status} | Entropy: ${frame.shannon_entropy.toFixed(4)}`);
      setContractData(frame.contract);
      if (rendererRef.current && frame.contract) {
        const contract = frame.contract as ManifestContract;
        const profile = resolverRef.current.resolve(contract);
        rendererRef.current.update(profile, contract);
      }
    });

    return () => {
      ws.close();
      window.removeEventListener('resize', handleResize);
      if (rendererRef.current) {
         rendererRef.current.dispose();
      }
    };
  }, []);

  return (
    <div style={{ width: '100vw', height: '100vh', backgroundColor: '#0B1026', color: 'white', overflow: 'hidden' }}>
      <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 10 }}>
        <h1>Aetherium Manifest</h1>
        <p>Status: {status}</p>
        <pre style={{fontSize: '10px'}}>{JSON.stringify(contractData, null, 2)}</pre>
      </div>
      <canvas ref={canvasRef} style={{ display: 'block', width: '100%', height: '100%' }} />
    </div>
  );
}

export default App;
