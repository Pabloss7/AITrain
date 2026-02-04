export type WSMessage =
    | { type: "ping" }
    | { type: "recom_request"; payload: RecomRequest }
    | { type: "job_created"; payload: { jobId: string } }
    | { type: "recommendation"; payload: any } // Payload type depends on AI service response, keeping loose for now

export interface RecomRequest {
    summonerName: string;
    tagLine: string;
}