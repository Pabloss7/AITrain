ROLE_FEATURE_MAP = {

    "JUNGLE": {
        "dragonKills": "objective_pressure",
        "baronKills": "objective_pressure",
        "objectivesStolen": "objective_pressure",

        "visionScorePerMinute": "vision_control",

        "totalTimeCCDealt": "utility_control",
        "timeCCingOthers": "utility_control",

        "kills": "combat_efficiency",
        "deaths": "survivability",

        "goldPerMinute": "lane_scaling"
    },

    "ADC": {
        "kills": "combat_efficiency",
        "deaths": "survivability",

        "csPerMinute": "lane_scaling",
        "goldPerMinute": "lane_scaling",

        "damageDealtToObjectives": "objective_pressure",
        "turretKills": "objective_pressure"
    },

    "UTILITY": {
        "visionScorePerMinute": "vision_control",

        "totalTimeCCDealt": "utility_control",
        "timeCCingOthers": "utility_control",

        "assists": "combat_efficiency",
        "deaths": "survivability",

        "totalDamageTaken": "frontline_value"
    },

    "MID": {
        "kills": "combat_efficiency",
        "assists": "combat_efficiency",

        "csPerMinute": "lane_scaling",
        "goldPerMinute": "lane_scaling",

        "deaths": "survivability",

        "turretKills": "objective_pressure"
    },

    "TOP":{    
        "totalDamageTaken": "frontline_value",
        "damageSelfMitigated": "frontline_value",
        "totalHeal": "survivability",

        "csPerMinute": "lane_scaling",
        "goldPerMinute": "lane_scaling",

        "kills": "combat_efficiency",
        "deaths": "survivability",

        "turretKills": "objective_pressure",
        "inhibitorKills": "objective_pressure"
    }
}
