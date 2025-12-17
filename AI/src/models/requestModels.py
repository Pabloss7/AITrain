from pydantic import BaseModel,ConfigDict
from typing import List, Dict, Any, Optional


from pydantic import BaseModel, field_validator
from typing import Optional, List
from pydantic import ConfigDict


class Participant(BaseModel):
    puuid: str
    championName: Optional[str] = None

    kills: Optional[int] = None
    deaths: Optional[int] = None
    assists: Optional[int] = None

    totalDamageDealtToChampions: Optional[int] = None
    totalMinionsKilled: Optional[int] = None
    visionScore: Optional[int] = None
    goldEarned: Optional[int] = None

    individualPosition: Optional[str] = None

    model_config = ConfigDict(extra="allow")

    @field_validator(
        "kills",
        "deaths",
        "assists",
        "totalDamageDealtToChampions",
        "totalMinionsKilled",
        "visionScore",
        "goldEarned",
        mode="before"
    )
    def cast_to_int(cls, v):
        if v is None:
            return None
        try:
            return int(v)
        except (ValueError, TypeError):
            return None



class Info(BaseModel):
    gameCreation: Optional[int] = None
    gameDuration: Optional[int] = None
    queueId: Optional[int] = None
    participants: List[Participant] 


class Metadata(BaseModel):
    dataVersion: Optional[str] = None
    matchId: str
    participants: List[str]


class MatchProcessRequest(BaseModel):
    jobId: str
    matchId: str
    puuid: str  
    metadata: Metadata
    info: Info
