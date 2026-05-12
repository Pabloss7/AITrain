from src.models.game_aspects import ASPECTS

def build_prompt_with_messages(role, top_features):
    if not top_features:
        return f" Player({role}): No negative aspects detected for this game.", "none"

    aspects_seen = set()
    aspect_list = []

    for feature, value, shap_value, aspect in top_features:
        if aspect not in aspects_seen:
            aspects_seen.add(aspect)
            message = ASPECTS.get(aspect, f"There's no predefined message for aspect: {aspect}.")
            aspect_list.append(
                f"- {aspect.replace('_', ' ').capitalize()} ({feature}): {message} "
                f"(value: {value}, SHAP impact: {shap_value:.3f})"
            )

    # Construir prompt final en formato Instruct para Gemma
    prompt = f"""<start_of_turn>user
You are an expert League of Legends coach.

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
{chr(10).join(aspect_list)}<end_of_turn>
<start_of_turn>model
"""
    return prompt.strip(), list(aspects_seen)[0]
