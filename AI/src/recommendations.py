def generate_recommendation(feature, value, shap_val):
    if feature == "deaths":
        if shap_val < 0:
            return "Has muerto demasiado. Intenta jugar más seguro para mejorar tu impacto."
    
    if feature == "kills":
        if shap_val < 0:
            return "Has conseguido pocas kills. Busca mejores oportunidades de tradeo y presión."
        else:
            return "Buen número de kills. Tu agresividad ha sido beneficiosa."

    if feature == "assists":
        if shap_val < 0:
            return "Participa más en las peleas para aumentar tu número de asistencias."
        else:
            return "Gran participación en peleas. Sigue así."

    if feature == "goldMin":
        if shap_val < 0:
            return "Tu oro por minuto es bajo. Intenta mejorar tu farmeo o eficiencia en mapa."
        else:
            return "Excelente oro por minuto. Está siendo clave en tus victorias."

    if feature == "visionMin":
        if shap_val < 0:
            return "Tu score de visión es bajo. Mejora tu control de wards."
        else:
            return "Buen control de visión. Sigue manteniendo la presión."

    return None