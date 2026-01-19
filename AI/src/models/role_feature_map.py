ROLE_FEATURE_MAP = {

    "JUNGLE": {
        "deaths": "risk_management",
        "visionMin": "map_control",
        "assists": "map_impact",
        "kills": "map_impact",
        "csPerMinute": "resource_efficiency",
    },

    "ADC": {
        "deaths": "positioning",
        "csPerMinute": "scaling",
        "goldMin": "scaling",
        "physicalDamageDealtToChampions": "teamfight_damage",
        "assists": "teamfight_presence",
    },

    "SUPPORT": {
        "visionMin": "vision_control",
        "assists": "teamfight_presence",
        "totalTimeCCDealt": "utility",
        "deaths": "positioning",
    },

    "MID": {
        "kills": "pressure",
        "assists": "pressure",
        "visionMin": "map_control",
        "magicDamageDealtToChampions": "damage_output",
        "deaths": "risk_management",
    },

    "TOP": {
        "deaths": "lane_survival",
        "csPerMinute": "lane_scaling",
        "damageSelfMitigated": "frontline_value",
        "totalDamageTaken": "frontline_value",
    }
}
