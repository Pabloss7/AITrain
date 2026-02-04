import { useState } from 'react';
import { useRecommendationSocket } from "../hooks/useRecommendationSocket";

// Icons
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
                  <h4 style={{ color: 'var(--accent-cyan)', margin: 0 }}>Coach Advice</h4>
                </div>

                <div className="advice-content" style={{
                  color: 'var(--text-light)',
                  lineHeight: '1.6',
                  fontSize: '1.1rem',
                  whiteSpace: 'pre-wrap',
                  padding: '1rem',
                  background: 'rgba(255, 255, 255, 0.03)',
                  borderRadius: '12px',
                  border: '1px solid rgba(255, 255, 255, 0.05)',
                  marginBottom: '1.5rem'
                }}>
                  {typeof recommendation === 'string' ? recommendation : (recommendation?.recommendation ?? JSON.stringify(recommendation))}
                </div>

                {/* YouTube Guide Section */}
                <div style={{
                  marginTop: '1.5rem',
                  padding: '1.5rem',
                  background: 'rgba(255, 0, 0, 0.05)',
                  borderRadius: '12px',
                  border: '1px solid rgba(255, 0, 0, 0.1)'
                }}>
                  <h4 style={{ color: '#ff0000', margin: '0 0 0.5rem 0', display: 'flex', alignItems: 'center' }}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" style={{ marginRight: '8px' }}>
                      <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z" />
                    </svg>
                    Video Guide Recommendation
                  </h4>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
                    Based on your primary area for improvement, we've found some helpful resources:
                  </p>
                  <a
                    href={`https://www.youtube.com/results?search_query=how+to+improve+${encodeURIComponent(recommendation.primary_aspect || 'gameplay')}+as+${encodeURIComponent(recommendation.role || 'player')}+in+league+of+legends`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="secondary"
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      textDecoration: 'none',
                      background: '#ff0000',
                      color: 'white',
                      padding: '10px 20px',
                      borderRadius: '8px',
                      fontWeight: 'bold',
                      fontSize: '0.9rem'
                    }}
                  >
                    Watch Guide on YouTube
                  </a>
                </div>
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
