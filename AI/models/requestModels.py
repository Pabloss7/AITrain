from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class Participant(BaseModel):
    puuid: str
    championName: Optional[str] = None
    kills: Optional[int] = None
    deaths: Optional[int] = None
    assists: Optional[int] = None
    individualPosition: Optional[str] = None
    totalDamageDealtToChampions: Optional[int] = None
    totalMinionsKilled: Optional[int] = None
    visionScore: Optional[int] = None
    goldEarned: Optional[int] = None
    # Esto evita que tengas que mantener a mano los +200 campos.
    __root__: Dict[str, Any] = {}


class Info(BaseModel):
    gameCreation: Optional[int] = None
    gameDuration: Optional[int] = None
    queueId: Optional[int] = None
    participants: List[Dict[str, Any]]  # datos completos tal cual los devuelve Riot


class Metadata(BaseModel):
    dataVersion: Optional[str] = None
    matchId: str
    participants: List[str]


class MatchProcessRequest(BaseModel):
    jobId: str
    matchId: str
    puuid: str        # puuid del jugador a analizar
    metadata: Metadata
    info: Info
