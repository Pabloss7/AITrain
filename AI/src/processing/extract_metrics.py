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
    game_duration = info.gameDuration
    row = {
        # --- CONTEXTO PARTIDA ---
        "gameDuration": game_duration,
        "teamId": player.teamId,
        "win": player.win,

        # --- IDENTIDAD ---
        "championName": player.championName,
        "individualPosition": player.individualPosition,
        "teamPosition": player.teamPosition,
        "lane": player.lane,
        "role": player.role,

        # --- COMBATE ---
        "kills": player.kills,
        "deaths": player.deaths,
        "assists": player.assists,
        "doubleKills": player.doubleKills,
        "tripleKills": player.tripleKills,
        "quadraKills": player.quadraKills,
        "pentaKills": player.pentaKills,
        "largestKillingSpree": player.largestKillingSpree,
        "largestMultiKill": player.largestMultiKill,

        # --- DAÑO ---
        "totalDamageDealtToChampions": player.totalDamageDealtToChampions,
        "physicalDamageDealtToChampions": player.physicalDamageDealtToChampions,
        "magicDamageDealtToChampions": player.magicDamageDealtToChampions,
        "trueDamageDealtToChampions": player.trueDamageDealtToChampions,
        "totalDamageTaken": player.totalDamageTaken,
        "damageSelfMitigated": player.damageSelfMitigated,
        "totalHeal": player.totalHeal,
        "totalHealsOnTeammates": player.totalHealsOnTeammates,
        "totalTimeCCDealt": player.totalTimeCCDealt,
        "timeCCingOthers": player.timeCCingOthers,

        # --- ECONOMÍA ---
        "goldEarned": player.goldEarned,
        "goldSpent": player.goldSpent,
        "totalMinionsKilled": player.totalMinionsKilled,
        "neutralMinionsKilled": player.neutralMinionsKilled,
        "totalAllyJungleMinionsKilled": player.totalAllyJungleMinionsKilled,
        "totalEnemyJungleMinionsKilled": player.totalEnemyJungleMinionsKilled,

        # --- VISIÓN ---
        "visionScore": player.visionScore,
        "wardsPlaced": player.wardsPlaced,
        "wardsKilled": player.wardsKilled,

        # --- OBJETIVOS ---
        "damageDealtToObjectives": player.damageDealtToObjectives,
        "damageDealtToBuildings": player.damageDealtToBuildings,
        "turretKills": player.turretKills,
        "inhibitorKills": player.inhibitorKills,
        "dragonKills": player.dragonKills,
        "baronKills": player.baronKills,
        "objectivesStolen": player.objectivesStolen,
        "objectivesStolenAssists": player.objectivesStolenAssists,

        # --- EARLY GAME ---
        "firstBloodKill": player.firstBloodKill,
        "firstBloodAssist": player.firstBloodAssist,
        "firstTowerKill": player.firstTowerKill,
        "firstTowerAssist": player.firstTowerAssist,

        # --- DERIVADAS ---
        "csPerMinute": player.totalMinionsKilled / (game_duration / 60),
        "goldPerMinute": player.goldEarned / (game_duration / 60),
        "visionScorePerMinute": player.visionScore / (game_duration / 60),
    }
    
    return row, row["individualPosition"]