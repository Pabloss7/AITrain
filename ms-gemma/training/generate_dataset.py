import json
import random

ASPECTS_DATA = {
    "combat_efficiency": {
        "name": "Combat Efficiency",
        "desc": "Capacity to win trades and fights",
        "explanation": [
            "you are taking unfavorable trades",
            "your damage output in teamfights is lower than expected",
            "you are not prioritizing high-value targets",
            "you are engaging without your key cooldowns"
        ],
        "advice": [
            "Wait for your team updates before committing to a fight.",
            "Focus on hitting the enemy carries instead of the frontline.",
            "Track enemy cooldowns to find the best window to engage.",
            "Practice your combo execution to maximize burst damage."
        ]
    },
    "frontline_value": {
        "name": "Frontline Value",
        "desc": "Capacity to receive damage and keep alive in fights",
        "explanation": [
            "you are not positioning yourself to absorb damage for your team",
            "you are getting caught out before the fight begins",
            "you are not peeling for your carries effectively",
            "you are engaging too deep without team support"
        ],
        "advice": [
            "Position yourself between the enemy and your carries.",
            "Use your defensive cooldowns to mitigate burst damage.",
            "Don't chase kills; focus on zoning the enemy team.",
            "Coordinate your engage with your team's follow-up."
        ]
    },
    "lane_scaling": {
        "name": "Lane Scaling",
        "desc": "Capacity to scale through gold and experience",
        "explanation": [
            "inefficient wave management is causing you to miss CS",
            "you are recalling at poor times and losing tower plates",
            "you are spending too much time roaming without results",
            "you are missing easy last-hits under pressure"
        ],
        "advice": [
            "Focus on last-hitting fundamentals in practice tool.",
            "Push the wave before recalling to minimize gold loss.",
            "Don't roam unless your wave is crashed into the enemy tower.",
            "Prioritize farming safe camps when the lane is dangerous."
        ]
    },
    "objective_pressure": {
        "name": "Objective Pressure",
        "desc": "Contribution in achieving objectives",
        "explanation": [
            "you are not rotating to Dragon or Herald fights",
            "you are splitting when an objective is spawning",
            "you are not helping to secure vision around objectives",
            "you are conceding towers without trading for other advantages"
        ],
        "advice": [
            "Setup vision around the objective 1 minute before it spawns.",
            "Push your lane and rotate first to the objective.",
            "Don't start an objective if the enemy jungler is alive and near.",
            "Look to cross-map (take tower) if you cannot contest the objective."
        ]
    },
    "vision_control": {
        "name": "Vision Control",
        "desc": "Map and vision control",
        "explanation": [
            "your vision score is significantly below average",
            "you are walking into unwarded areas and dying",
            "you are not buying Control Wards for key objectives",
            "you are not clearing enemy vision effectively"
        ],
        "advice": [
            "Buy a Control Ward on every back if you have the gold.",
            "Place wards in deep jungle entrances to track the enemy jungler.",
            "Use your sweeper lens before face-checking brushes.",
            "Ward the river pixel brush to protect your lane from ganks."
        ]
    },
    "utility_control": {
        "name": "Utility Control",
        "desc": "CC and utility contribution for the team",
        "explanation": [
            "you are not using your crowd control to lock down enemies",
            "you are wasting key utility spells on non-threatening targets",
            "you are overlapping CC chains with your teammates",
            "your ability usage in fights is reactive rather than proactive"
        ],
        "advice": [
            "Save your CC for the enemy's main threat (e.g., Assassin).",
            "Chain your crowd control with your teammates' abilities.",
            "Use your utility spells to peel for your ADC.",
            "Look for picks with your CC when enemies act out of position."
        ]
    },
    "survivability": {
        "name": "Survivability",
        "desc": "Capacity to survive on dangerous situationships",
        "explanation": [
            "you are dying too often in the early game",
            "you are overextending without vision",
            "you are disrespecting the enemy's kill threat",
            "you are taking unnecessary tower shots"
        ],
        "advice": [
            "Play safer when your summoner spells are on cooldown.",
            "Respect the enemy's level and item spikes.",
            "Don't greed for plates if you don't know where the jungler is.",
            "Stay behind your frontline during late-game sieges."
        ]
    }
}


# This maps Roles to the KEYS in ASPECTS_DATA
ROLE_ASPECTS = {
    "JUNGLE": ["objective_pressure", "vision_control", "utility_control", "combat_efficiency", "survivability", "lane_scaling"],
    "ADC": ["combat_efficiency", "survivability", "lane_scaling", "objective_pressure"],
    "UTILITY": ["vision_control", "utility_control", "combat_efficiency", "survivability", "frontline_value"], # UTILITY likely means SUPPORT here
    "MID": ["combat_efficiency", "lane_scaling", "survivability", "objective_pressure"],
    "TOP": ["frontline_value", "survivability", "lane_scaling", "combat_efficiency", "objective_pressure"]
}


ROLE_MAP_NORMALIZED = {
    "TOP": "TOP",
    "JUNGLE": "JUNGLE",
    "MID": "MID",
    "ADC": "ADC",
    "SUPPORT": "UTILITY" # Mapping SUPPORT to the UTILITY key in our logic
}

PROMPT_TEMPLATE = """You are an expert League of Legends coach.

Your task is to transform a technical performance analysis into clear and actionable gameplay advice.

Use the information below to:
- Explain WHY each aspect negatively impacts the player's performance
- Provide concrete in-game advice
- Adapt recommendations to the player's role

Avoid generic tips. Be specific and practical.

ANALYSIS DATA:
Player analyzed:
- Role: {role}

In-game aspects with negative impact detected:
{aspects}
"""

def generate_example():
    role_display = random.choice(["TOP", "JUNGLE", "MID", "ADC", "SUPPORT"])
    role_key = ROLE_MAP_NORMALIZED[role_display]
    
    possible_aspects = ROLE_ASPECTS.get(role_key, list(ASPECTS_DATA.keys()))
    
    num_aspects = random.randint(1, 3)

    num_aspects = min(num_aspects, len(possible_aspects))
    selected_keys = random.sample(possible_aspects, num_aspects)
    
    aspects_text_lines = []
    explanations = []
    advices = []
    
    for key in selected_keys:
        aspect = ASPECTS_DATA[key]
        
       
        value = round(random.uniform(-0.5, 0.5), 2) 
        shap = round(random.uniform(-1.5, -0.1), 3) # Negative SHAP implies negative impact
        
        # Build the prompt line
        line = f"- {aspect['name']}: {aspect['desc']} (value: {value}, SHAP impact: {shap})"
        aspects_text_lines.append(line)
        
        explanations.append(random.choice(aspect["explanation"]))
        advices.append(random.choice(aspect["advice"]))
        
    aspects_block = "\n".join(aspects_text_lines)
    
    input_text = PROMPT_TEMPLATE.format(role=role_display, aspects=aspects_block)
    
    advice_body = " ".join(advices)
    explanation_body = f"As a {role_display}, " + " Also, ".join(explanations) + "."
    
    output_text = f"{explanation_body}\n\nTo improve your gameplay: {advice_body}"
    
    return {
        "input": input_text,
        "output": output_text
    }

def main():
    print("Generating 350 examples...")
    with open("train.jsonl", "w", encoding="utf-8") as f:
        for _ in range(350):
            ex = generate_example()
            f.write(json.dumps(ex) + "\n")
    print("Done! Saved to train.jsonl")

if __name__ == "__main__":
    main()
