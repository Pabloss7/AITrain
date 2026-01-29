import { useState } from 'react';
import { useRecommendationSocket } from "../hooks/useRecommendationSocket";

export default function Home() {
  const [summonerName, setSummonerName] = useState('xxkattaa');
  const [tagLine, setTagLine] = useState('KOI');

  const { status, jobId, recommendation, connectAndRequest, disconnect } = useRecommendationSocket();

  const handleAnalyze = () => {
    connectAndRequest(summonerName, tagLine);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ color: "#333", borderBottom: "1px solid #ccc", paddingBottom: "10px" }}>AITrain Analysis</h1>

      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Summoner Name"
          value={summonerName}
          onChange={(e) => setSummonerName(e.target.value)}
          style={{ padding: "8px", borderRadius: "4px", border: "1px solid #aaa", flex: 1 }}
        />
        <input
          type="text"
          placeholder="Tag Line"
          value={tagLine}
          onChange={(e) => setTagLine(e.target.value)}
          style={{ padding: "8px", borderRadius: "4px", border: "1px solid #aaa", width: "80px" }}
        />
        <button
          onClick={handleAnalyze}
          disabled={status === 'connecting' || status === 'job_created'}
          style={{
            padding: "8px 16px",
            backgroundColor: status === 'connecting' ? "#ccc" : "#007BFF",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: status === 'connecting' ? "not-allowed" : "pointer"
          }}
        >
          {status === 'connecting' ? 'Connecting...' : 'Analyze'}
        </button>
        {status !== 'idle' && (
          <button onClick={disconnect} style={{ padding: "8px", background: "red", color: "white", border: "none", borderRadius: "4px" }}>
            Reset
          </button>
        )}
      </div>

      <div style={{ background: "#f5f5f5", padding: "15px", borderRadius: "8px" }}>
        <h3>Status: <span style={{ color: status === 'completed' ? 'green' : (status === 'error' ? 'red' : 'blue') }}>{status.toUpperCase()}</span></h3>

        {jobId && <p><strong>Job ID:</strong> {jobId}</p>}

        {recommendation && (
          <div style={{ marginTop: "20px" }}>
            <h4>Recommendation Result:</h4>
            <pre style={{ background: "#eee", padding: "10px", borderRadius: "5px", overflow: "auto" }}>
              {JSON.stringify(recommendation, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
