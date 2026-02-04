import { useEffect, useState } from "react";
import { wsService } from "../api/websocket";
import type { WSMessage } from "../types/websocket";

export function useWebSocket(url: string) {
  const [lastMessage, setLastMessage] = useState<WSMessage | null>(null);

  useEffect(() => {
    wsService.connect(url, setLastMessage);

    return () => {
      wsService.disconnect();
    };
  }, [url]);

  const sendMessage = (message: WSMessage) => {
    wsService.send(message);
  };

  return { lastMessage, sendMessage };
}
