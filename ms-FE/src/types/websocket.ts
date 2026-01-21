export type WSMessage = 
    | { type: "ping" }
    | { type: "recom_request"; payload: recomRequest } 
    | { type: "recom_respone"; payload: recomResponse }
     
export interface recomRequest {
    summoner: string;
    tag: string
}

export interface recomResponse {
    recommendation: object
}