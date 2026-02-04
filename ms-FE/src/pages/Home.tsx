import { useState } from 'react';
import { useRecommendationSocket } from "../hooks/useRecommendationSocket";

// Icons
const CopyIcon = () => (
  <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ marginRight: '4px' }}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
  </svg>
);

const CheckIcon = () => (
  <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ marginRight: '4px' }}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
  </svg>
);

const InfoIcon = () => (
  <svg width="40" height="40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

interface HomeProps {
  onNavigate: (page: string) => void;
}

export default function Home({ onNavigate }: HomeProps) {
  const [summonerName, setSummonerName] = useState('');
  const [tagLine, setTagLine] = useState('');
  const [copied, setCopied] = useState(false);

  const { status, recommendation, connectAndRequest, disconnect } = useRecommendationSocket();

  const handleAnalyze = () => {
    if (summonerName && tagLine) {
      connectAndRequest(summonerName, tagLine);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && summonerName && tagLine) {
      handleAnalyze();
    }
  };

  const handleCopy = () => {
    if (recommendation) {
      navigator.clipboard.writeText(JSON.stringify(recommendation, null, 2));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const isFormValid = summonerName.trim() !== '' && tagLine.trim() !== '';

  return (
    <>
      {/* Background Blobs */}
      <div className="bg-blob blob-1"></div>
      <div className="bg-blob blob-2"></div>

      <div className="container">
        <div style={{ position: 'absolute', top: '1rem', right: '1rem', zIndex: 10 }}>
          <button
            onClick={() => onNavigate('about')}
            style={{
              background: 'rgba(255,255,255,0.05)',
              border: 'none',
              padding: '14px',
              borderRadius: '50%',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
            title="About AITrain"
          >
            <InfoIcon />
          </button>
        </div>

        <div style={{ textAlign: 'center', marginBottom: '1rem', position: 'relative', zIndex: 1 }}>
          <h1>AITrain</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem', fontWeight: 300, letterSpacing: '0.02em' }}>
            Real-time League of Legends match analysis & recommendations
          </p>
        </div>

        <div className="glass-panel" style={{ padding: '2.5rem', position: 'relative', zIndex: 1 }}>
          <div className="input-group">
            <input
              type="text"
              placeholder="Summoner Name"
              value={summonerName}
              onChange={(e) => setSummonerName(e.target.value)}
              onKeyDown={handleKeyDown}
              style={{ flex: 2 }}
            />
            <input
              type="text"
              placeholder="Tag"
              value={tagLine}
              onChange={(e) => setTagLine(e.target.value)}
              onKeyDown={handleKeyDown}
              style={{ flex: 1 }}
            />
          </div>

          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
            {status !== 'idle' && (
              <button
                onClick={disconnect}
                className="secondary"
              >
                Reset
              </button>
            )}
            <button
              onClick={handleAnalyze}
              disabled={status === 'connecting' || status === 'job_created' || !isFormValid}
            >
              {status === 'connecting' ? 'Connecting...' : status === 'job_created' ? 'Processing...' : 'Analyze Match'}
            </button>
          </div>
        </div>

        {status !== 'idle' && (
          <div className="glass-panel result-card" style={{ position: 'relative', zIndex: 1 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3>Analysis Status</h3>
              <span className={`status-badge status-${status}`}>
                {status === 'job_created' ? 'Processing' : status}
              </span>
            </div>

            {status === 'connecting' || status === 'job_created' ? (
              <div style={{ textAlign: 'center', padding: '3rem' }}>
                <div className="spinner"></div>
                <div className="animate-pulse" style={{ color: 'var(--primary)', marginBottom: '1rem', fontSize: '1.2rem' }}>
                  Analyzing match data...
                </div>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>This may take a few moments</p>
              </div>
            ) : null}

            {recommendation && (
              <div style={{ marginTop: "20px", position: "relative" }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                  <h4 style={{ color: 'var(--accent-cyan)', margin: 0 }}>Recommendation Result</h4>
                  <button onClick={handleCopy} className="copy-btn">
                    {copied ? (
                      <span style={{ display: 'flex', alignItems: 'center', color: '#4ade80' }}>
                        <CheckIcon /> Copied
                      </span>
                    ) : (
                      <span style={{ display: 'flex', alignItems: 'center' }}>
                        <CopyIcon /> Copy JSON
                      </span>
                    )}
                  </button>
                </div>

                <pre className="code-block" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                  {JSON.stringify(recommendation, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}

        <footer style={{
          marginTop: 'auto',
          paddingBottom: '1rem',
          textAlign: 'center',
          color: 'var(--text-muted)',
          fontSize: '0.8rem'
        }}>
          &copy; {new Date().getFullYear()} AITrain
        </footer>
      </div>
    </>
  );
}
