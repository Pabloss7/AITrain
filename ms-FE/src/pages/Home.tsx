import { useWebSocket } from "../hooks/useWebSocket";

export default function Home() {
  const { lastMessage, sendMessage } = useWebSocket(
    "ws://localhost:8000/ws"
  );

  const requestPrediction = () => {
    sendMessage({
      type: "recom_request",
      payload: {
        summoner: "xxkattaa",
        tag: "KOI"
      },
    });
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>AITrain</h1>

      <button onClick={requestPrediction}>
        Solicitar predicción
      </button>

      {lastMessage && (
        <pre>{JSON.stringify(lastMessage, null, 2)}</pre>
      )}
    </div>
  );
}
