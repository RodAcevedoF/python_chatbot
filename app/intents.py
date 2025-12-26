def detect_intent(message: str) -> str:
    msg = message.lower()

    if any(w in msg for w in ["hola", "buenas", "hello"]):
        return "greeting"

    if any(w in msg for w in ["check-in", "checkout", "horario", "desayuno"]):
        return "horarios"

    if any(w in msg for w in ["wifi", "parking", "piscina", "spa", "gimnasio"]):
        return "servicios"

    if any(w in msg for w in ["habitacion", "habitaciones", "suite", "precio"]):
        return "habitaciones"

    if any(w in msg for w in [
        "recomienda",
        "recomendación",
        "recomendaciones",
        "dónde comer",
        "cenar",
        "restaurante"
    ]):
        return "recomendaciones"

    if any(w in msg for w in ["recepcion", "persona", "humano"]):
        return "humano"

    return "fallback"
