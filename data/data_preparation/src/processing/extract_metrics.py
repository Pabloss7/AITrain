def extract_metrics(match_doc):
    participants = match_doc["info"]["participants"]
    
    return{
        "gameDuration": match_doc["info"]["gameDuration"],
        "championName": [p["championName"] for p in participants],
        "individualPosition": [p["individualPosition"]for p in participants],
        "kills": [p["kills"] for p in participants],
        "deaths": [p["deaths"] for p in participants],
        "assists": [p["assists"] for p in participants],
        "goldEarned": [p["goldEarned"] for p in participants],
        "totalDamageDealtToChampions": [p["totalDamageDealtToChampions"] for p in participants],
        "totalMinionsKilled": [p["totalMinionsKilled"] for p in participants],
        "visionScore": [p["visionScore"] for p in participants],
        "wardsPlaced": [p["wardsPlaced"] for p in participants],
        "wardsKilled": [p["wardsKilled"] for p in participants],
        "win": [p["win"] for p in participants],
        "firstBloodKill": [p["firstBloodKill"] for p in participants],
    }