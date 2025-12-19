def extract_metrics(match_doc):
    rows = []
    participants = match_doc["json"]["info"]["participants"]
    for i in range(10):
        row = {
            "gameDuration": match_doc["json"]["info"]["gameDuration"],
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

def extract_metrics_player(info,metadata, puuid):
    row = []
    position = metadata.participants.index(puuid)
    player = info.participants[position]
    row = {
          "gameDuration": info.gameDuration,
            "kills": player.kills,
            "deaths": player.deaths,
            "assists": player.assists,
            "goldEarned": player.goldEarned,
            "totalDamageDealtToChampions": player.totalDamageDealtToChampions,
            "totalMinionsKilled": player.totalMinionsKilled,
            "visionScore": player.visionScore,
            "wardsPlaced": player.wardsPlaced,
            "wardsKilled": player.wardsKilled,
            "win": player.win,
            "firstBloodKill": player.firstBloodKill,
    }
    print("Metrics from player:\n",row)
    return row