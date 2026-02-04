

// Icons
const ArrowLeftIcon = () => (
  <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ marginRight: '8px' }}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
  </svg>
);

const LinkedinIcon = () => (
  <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24" style={{ marginRight: '8px' }}>
    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
  </svg>
);

interface AboutProps {
  onNavigate: (page: string) => void;
}

export default function About({ onNavigate }: AboutProps) {
  return (
    <>
      {/* Background Blobs (reused for consistency) */}
      <div className="bg-blob blob-1"></div>
      <div className="bg-blob blob-2"></div>

      <div className="container" style={{ maxWidth: '800px' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem', position: 'relative', zIndex: 1 }}>
          <h1>About AITrain</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem', fontWeight: 300 }}>
            Made by Pablo Sanchez - BE/AI Engineer
          </p>
        </div>

        <div className="glass-panel" style={{ padding: '2.5rem', position: 'relative', zIndex: 1 }}>
          <div style={{ marginBottom: '2rem' }}>
            <h3>Technical Architecture</h3>
            <p style={{ color: 'var(--text-muted)', lineHeight: '1.6', marginBottom: '1rem' }}>
              AITrain is built on a scalable <strong>Microservices Architecture</strong> designed for real-time performance.
              The system orchestrates data flow using <strong>Docker</strong> containers, utilizing <strong>Java Spring Boot</strong> for the core logic
              and <strong>WebSockets</strong> for instant communication between the backend and the frontend.
            </p>
            <p style={{ color: 'var(--text-muted)', lineHeight: '1.6', marginBottom: '1rem' }}>
              Key Technologies:
            </p>
            <ul style={{ color: 'var(--text-muted)', paddingLeft: '1.5rem', lineHeight: '1.6' }}>
              <li><strong>Frontend</strong>: React, Vite, TypeScript, Glassmorphism UI</li>
              <li><strong>Backend</strong>: Java Spring Boot, WebSocket API</li>
              <li><strong>AI Engine</strong>: Python, FastAPI, XGBoost, SHAP, Google Gemma 3</li>
              <li><strong>Infrastructure</strong>: Docker, Docker Compose</li>
              <li><strong>Data</strong>: Real-time Riot Games API integration</li>
            </ul>
          </div>

          <div style={{ marginBottom: '2rem' }}>
            <h3>Project Vision (TFG)</h3>
            <p style={{ color: 'var(--text-muted)', marginBottom: '1rem', lineHeight: '1.6' }}>
              Developed as a Final Degree Project (TFG), AITrain was created with the specific intention
              of researching and implementing <strong>cutting-edge technologies</strong>. It serves as a platform for
              advanced learning in distributed systems and modern web development.
            </p>
            <a
              href="https://www.linkedin.com/in/pablo-sanchez-sanchez-dev/"
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                textDecoration: 'none',
                color: '#0a66c2',
                fontWeight: 'bold',
                fontSize: '1.1rem'
              }}
            >
              <LinkedinIcon /> Connect on LinkedIn
            </a>
          </div>

          <button
            onClick={() => onNavigate('home')}
            className="secondary"
            style={{ display: 'flex', alignItems: 'center' }}
          >
            <ArrowLeftIcon /> Back to Analyzer
          </button>
        </div>

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
