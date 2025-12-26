from app.data_loader import load_hotel_info

hotel_info = load_hotel_info()

def greeting_response():
    return (
        f"Hola 👋 Soy el asistente virtual del {hotel_info['hotel']['name']} 🏖️\n"
        "¿En qué puedo ayudarte?"
    )

def horarios_response():
    h = hotel_info["hotel"]
    hours = hotel_info.get("hours", {})
    response = (
        f"📅 Check-in: desde las {h['checkin']}\n"
        f"📅 Check-out: hasta las {h['checkout']}\n\n"
        f"🍳 Desayuno: {h['breakfast']}\n"
    )
    
    if hours:
        response += "\n🕐 Horarios de servicios:\n"
        if "spa" in hours:
            response += f"• Spa: {hours['spa']}\n"
        if "pool" in hours:
            response += f"• Piscina: {hours['pool']}\n"
        if "reception" in hours:
            response += f"• Recepción: {hours['reception']}\n"
    
    return response

def servicios_response():
    services = "\n".join(f"✔️ {s}" for s in hotel_info["services"])
    response = (
        "Nuestros servicios principales:\n"
        f"{services}\n\n"
        f"📶 Wifi: {hotel_info['hotel']['wifi']}\n"
        f"🚗 Parking: {hotel_info['hotel']['parking']}\n"
    )
    
    # Add detailed amenities if available
    amenities = hotel_info.get("amenities", [])
    if amenities:
        response += "\n🏊 Detalles de nuestros servicios:\n"
        for amenity in amenities:
            response += f"• {amenity['name']}: {amenity.get('description', '')}\n"
    
    # Add accessibility info
    accessibility = hotel_info.get("accessibility", {})
    if accessibility:
        response += "\n♿ Accesibilidad:\n"
        if accessibility.get('elevator'):
            response += "• Ascensor disponible\n"
        if accessibility.get('accessible_rooms'):
            response += "• Habitaciones adaptadas\n"
        if accessibility.get('ramp'):
            response += "• Rampa de acceso\n"
    
    return response

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
    response = "📞 Te ponemos en contacto con recepción.\n\n"
    
    if "phone" in contact:
        response += f"📱 Teléfono: {contact['phone']}\n"
    if "email" in contact:
        response += f"📧 Email: {contact['email']}\n"
    
    hours = hotel_info.get("hours", {})
    if "reception" in hours:
        response += f"\n🕐 Horario: {hours['reception']}\n"
    
    if "human_message" in contact:
        response += f"\n{contact['human_message']}"
    
    return response

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
