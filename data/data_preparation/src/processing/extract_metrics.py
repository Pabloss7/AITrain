def extract_metrics(match_doc):
    rows = []
    participants = match_doc["json"]["info"]["participants"]
    for i in range(10):
        row = {
            "gameDuration": match_doc["json"]["info"]["gameDuration"],
            "championName": participants[i]["championName"],
            "individualPosition": participants[i]["individualPosition"],
            "kills": participants[i]["kills"],
            "deaths": participants[i]["deaths"],
            "assists": participants[i]["assists"],
            "goldEarned": participants[i]["goldEarned"],
            "totalDamageDealtToChampions": participants[i]["totalDamageDealtToChampions"],
            "totalMinionsKilled": participants[i]["totalMinionsKilled"],
            "visionScore": participants[i]["visionScore"],
            "wardsPlaced": participants[i]["wardsPlaced"],
            "wardsKilled": participants[i]["wardsKilled"],
            "win": participants[i]["win"],
            "firstBloodKill": participants[i]["firstBloodKill"],
        }
        rows.append(row)

    return rows