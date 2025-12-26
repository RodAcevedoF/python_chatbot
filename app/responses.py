from app.data_loader import load_hotel_info

hotel_info = load_hotel_info()

def greeting_response():
    return (
        f"Hola 👋 Soy el asistente virtual del {hotel_info['hotel']['name']} 🏖️\n"
        "¿En qué puedo ayudarte?"
    )

def horarios_response():
    h = hotel_info["hotel"]
    return (
        f"📅 Check-in: desde las {h['checkin']}\n"
        f"📅 Check-out: hasta las {h['checkout']}\n"
        f"🍳 Desayuno: {h['breakfast']}"
    )

def servicios_response():
    services = "\n".join(f"✔️ {s}" for s in hotel_info["services"])
    return (
        "Nuestros servicios principales:\n"
        f"{services}\n\n"
        f"📶 Wifi: {hotel_info['hotel']['wifi']}\n"
        f"🚗 Parking: {hotel_info['hotel']['parking']}"
    )

def habitaciones_response():
    lines = []
    for room in hotel_info["rooms"]:
        desayuno = "con desayuno" if room["breakfast_included"] else "sin desayuno"
        lines.append(
            f"🛏️ {room['type']} – {room['capacity']} personas ({desayuno})"
        )
    return "Disponemos de:\n" + "\n".join(lines)

def recomendaciones_response():
    places = "\n".join(f"🌴 {p}" for p in hotel_info["recommendations"]["places"])
    restaurants = "\n".join(
        f"🍽️ {r}" for r in hotel_info["recommendations"]["restaurants"]
    )
    return (
        "Cerca del hotel te recomendamos:\n\n"
        f"{places}\n\n"
        "Para comer o cenar:\n"
        f"{restaurants}"
    )

def humano_response():
    contact = hotel_info["contact"]
    return (
        "📞 Te ponemos en contacto con recepción.\n"
        f"Teléfono: {contact['phone']}\n"
        f"{contact['human_message']}"
    )

def fallback_response():
    return (
        "Lo siento 😅, no he entendido tu pregunta.\n\n"
        "Puedo ayudarte con:\n"
        "• Servicios del hotel\n"
        "• Horarios\n"
        "• Habitaciones\n"
        "• Recomendaciones\n"
        "• Hablar con recepción"
    )
