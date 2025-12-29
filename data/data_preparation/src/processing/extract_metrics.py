def extract_metrics(match_doc):
    rows = []
    info = match_doc["json"]["info"]
    participants = info["participants"]
    game_duration = info["gameDuration"]

    for p in participants:
        row = {
            # --- CONTEXTO PARTIDA ---
            "gameDuration": game_duration,
            "teamId": p["teamId"],
            "win": p["win"],

            # --- IDENTIDAD ---
            "championName": p["championName"],
            "individualPosition": p["individualPosition"],
            "teamPosition": p["teamPosition"],
            "lane": p["lane"],
            "role": p["role"],

            # --- COMBATE ---
            "kills": p["kills"],
            "deaths": p["deaths"],
            "assists": p["assists"],
            "doubleKills": p["doubleKills"],
            "tripleKills": p["tripleKills"],
            "quadraKills": p["quadraKills"],
            "pentaKills": p["pentaKills"],
            "largestKillingSpree": p["largestKillingSpree"],
            "largestMultiKill": p["largestMultiKill"],

            # --- DAÑO ---
            "totalDamageDealtToChampions": p["totalDamageDealtToChampions"],
            "physicalDamageDealtToChampions": p["physicalDamageDealtToChampions"],
            "magicDamageDealtToChampions": p["magicDamageDealtToChampions"],
            "trueDamageDealtToChampions": p["trueDamageDealtToChampions"],
            "totalDamageTaken": p["totalDamageTaken"],
            "damageSelfMitigated": p["damageSelfMitigated"],
            "totalHeal": p["totalHeal"],
            "totalHealsOnTeammates": p["totalHealsOnTeammates"],
            "totalTimeCCDealt": p["totalTimeCCDealt"],
            "timeCCingOthers": p["timeCCingOthers"],

            # --- ECONOMÍA ---
            "goldEarned": p["goldEarned"],
            "goldSpent": p["goldSpent"],
            "totalMinionsKilled": p["totalMinionsKilled"],
            "neutralMinionsKilled": p["neutralMinionsKilled"],
            "totalAllyJungleMinionsKilled": p["totalAllyJungleMinionsKilled"],
            "totalEnemyJungleMinionsKilled": p["totalEnemyJungleMinionsKilled"],

            # --- VISIÓN ---
            "visionScore": p["visionScore"],
            "wardsPlaced": p["wardsPlaced"],
            "wardsKilled": p["wardsKilled"],

            # --- OBJETIVOS ---
            "damageDealtToObjectives": p["damageDealtToObjectives"],
            "damageDealtToBuildings": p["damageDealtToBuildings"],
            "turretKills": p["turretKills"],
            "inhibitorKills": p["inhibitorKills"],
            "dragonKills": p["dragonKills"],
            "baronKills": p["baronKills"],
            "objectivesStolen": p["objectivesStolen"],
            "objectivesStolenAssists": p["objectivesStolenAssists"],

            # --- EARLY GAME ---
            "firstBloodKill": p["firstBloodKill"],
            "firstBloodAssist": p["firstBloodAssist"],
            "firstTowerKill": p["firstTowerKill"],
            "firstTowerAssist": p["firstTowerAssist"],

            # --- DERIVADAS ---
            "csPerMinute": p["totalMinionsKilled"] / (game_duration / 60),
            "goldPerMinute": p["goldEarned"] / (game_duration / 60),
            "visionScorePerMinute": p["visionScore"] / (game_duration / 60),
        }

        rows.append(row)

    return rows
