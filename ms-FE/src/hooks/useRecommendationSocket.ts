import { useState, useCallback, useEffect } from 'react';
import { wsService } from '../api/websocket';
import type { WSMessage } from '../types/websocket';

export function useRecommendationSocket() {
    const [status, setStatus] = useState<'idle' | 'connecting' | 'job_created' | 'completed' | 'error'>('idle');
    const [jobId, setJobId] = useState<string | null>(null);
    const [recommendation, setRecommendation] = useState<any | null>(null);

    const connectAndRequest = useCallback((summonerName: string, tagLine: string) => {
        setStatus('connecting');

        wsService.connect('ws://localhost:8181/ws', (message: WSMessage) => {
            if (message.type === 'job_created') {
                setJobId(message.payload.jobId);
                setStatus('job_created');
            } else if (message.type === 'recommendation') {
                // Handle the structured payload: { response, role, aspect }
                let data = null;
                const payload = message.payload;

                if (payload.response) {
                    // This is the structure the user specified: { jobId, status, response, aspect, role }
                    data = {
                        recommendation: typeof payload.response === 'string' ? payload.response : JSON.stringify(payload.response),
                        role: payload.role || "unknown",
                        primary_aspect: payload.aspect || "gameplay"
                    };
                } else if (payload.recommendations && payload.recommendations.response) {
                    // Fallback for older nested format
                    data = {
                        recommendation: payload.recommendations.response,
                        role: payload.role || "unknown",
                        primary_aspect: "gameplay"
                    };
                } else if (payload.recommendation) {
                    // Fallback for previous structured format
                    data = {
                        recommendation: payload.recommendation,
                        role: payload.role || "unknown",
                        primary_aspect: payload.primary_aspect || "gameplay"
                    };
                } else {
                    // Ultimate fallback
                    data = {
                        recommendation: typeof payload === 'string' ? payload : JSON.stringify(payload),
                        role: "unknown",
                        primary_aspect: "gameplay"
                    };
                }

                setRecommendation(data);
                setStatus('completed');
                wsService.disconnect();
            }
        });

        // Wait for connection to be open before sending (wsService might need logic for this, 
        // but typically onopen handles it if queueing not implemented. 
        // The existing ws.service implementation in api/websocket.ts doesn't queue. 
        // So we rely on a small delay or check readyState. 
        // Ideally wsService should accept a callback for 'onConnected', but for now:
        setTimeout(() => {
            wsService.send({
                type: 'recom_request',
                payload: { summonerName, tagLine }
            });
        }, 1000);
    }, []);

    const disconnect = useCallback(() => {
        wsService.disconnect();
        setStatus('idle');
    }, []);

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            wsService.disconnect();
        };
    }, []);

    return { status, jobId, recommendation, connectAndRequest, disconnect };
}
