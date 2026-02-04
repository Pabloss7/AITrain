import type { WSMessage } from "../types/websocket";

class WebSocketService {
  private socket: WebSocket | null = null;

  connect(url: string, onMessage: (msg: WSMessage) => void) {
    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      console.log("WebSocket connected");
    };

    this.socket.onmessage = (event) => {
      const data: WSMessage = JSON.parse(event.data);
      onMessage(data);
    };

    this.socket.onclose = () => {
      console.log("WebSocket disconnected");
    };
  }

  send(message: WSMessage) {
    if (this.socket?.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message));
    }
  }

  disconnect() {
    this.socket?.close();
  }
}

export const wsService = new WebSocketService();
