def generate_recommendation(feature, value, shap_val):

    # --- MUERTES ---
    if feature == "deaths" and shap_val < 0:
        return "Has muerto demasiado. Jugar más seguro aumentará tu impacto en la partida."

    # --- KILLS ---
    if feature == "kills":
        if shap_val < 0:
            return "Has conseguido pocas kills. Busca mejores oportunidades de tradeo y presión."
        else:
            return "Buen número de kills. Tu agresividad ha sido beneficiosa."

    # --- ASSISTS ---
    if feature == "assists":
        if shap_val < 0:
            return "Participa más en peleas de equipo para aumentar tu impacto."
        else:
            return "Gran participación en peleas. Sigue apoyando a tu equipo."

    # --- ORO ---
    if feature == "goldMin":
        if shap_val < 0:
            return "Tu oro por minuto es bajo. Mejora el farmeo y la toma de objetivos."
        else:
            return "Excelente gestión del oro. Está siendo clave en la partida."

    # --- VISIÓN ---
    if feature == "visionMin":
        if shap_val < 0:
            return "El control de visión es bajo. Coloca más wards y limpia visión enemiga."
        else:
            return "Buen control de visión. Aporta mucha información a tu equipo."

    # --- CS ---
    if feature == "csPerMinute" and shap_val < 0:
        return "Tu farmeo es bajo. Intenta optimizar la recogida de súbditos entre rotaciones."

    # --- DAÑO ---
    if feature == "physicalDamageDealtToChampions" and shap_val < 0:
        return "Tu daño físico es bajo. Participa más en intercambios y peleas."

    if feature == "magicDamageDealtToChampions" and shap_val < 0:
        return "Tu daño mágico es bajo. Aprovecha mejor tus habilidades en teamfights."

    if feature == "trueDamageDealtToChampions" and shap_val < 0:
        return "Tu daño verdadero es bajo. Quizá no estás explotando bien tu kit."

    # --- SUPERVIVENCIA ---
    if feature == "totalDamageTaken" and shap_val < 0:
        return "Recibes demasiado daño. Revisa tu posicionamiento en las peleas."

    if feature == "damageSelfMitigated" and shap_val < 0:
        return "Mitigas poco daño. Puede que estés entrando mal a las peleas o itemizando mal."

    if feature == "totalHeal" and shap_val < 0:
        return "Tu curación es baja. Aprovecha mejor tus recursos defensivos."

    # --- CONTROL ---
    if feature == "totalTimeCCDealt" and shap_val < 0:
        return "Aportas poco control de masas. Intenta usar mejor tus habilidades clave."

    # --- PELEAS ---
    if feature == "largestKillingSpree" and shap_val < 0:
        return "No encadenas kills. Jugar más seguro tras una kill puede mejorar tu racha."

    if feature == "largestMultiKill" and shap_val < 0:
        return "Te cuesta rematar peleas. Busca mejor posicionamiento en teamfights."

    return None
