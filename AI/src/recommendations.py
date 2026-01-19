from src.models.game_aspects import ASPECTS

def build_prompt_with_messages(role, top_features):
    if not top_features:
        return f"{player_name} ({role}): No negative aspects detected for this game."

    aspects_seen = set()
    aspect_list = []

    for feature, value, shap_value, aspect in top_features:
        if aspect not in aspects_seen:
            aspects_seen.add(aspect)
            # Obtener mensaje predefinido
            message = ASPECTS.get(aspect, f"There's no predefined message for aspect: {aspect}.")
            # Añadir feature, valor y SHAP al mensaje
            aspect_list.append(
                f"- {aspect.replace('_', ' ').capitalize()} ({feature}): {message} "
                f"(value: {value}, SHAP impact: {shap_value:.3f})"
            )

    # Construir prompt final
    prompt = f"""
    Player analyzed:
    - Role: {role}

    In-game aspects with negative impact detected:
    {chr(10).join(aspect_list)}

    Instructions:
    Generate additional recommendations with a higher explainable level and detail of the player's performance.
    Focus on practical and clear gameplay advice for the player.
    """
    return prompt.strip()
