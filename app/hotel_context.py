from app.data_loader import load_hotel_info

def build_hotel_context() -> str:
    info = load_hotel_info()

    lines = []

    hotel = info["hotel"]
    lines.append(f"Hotel: {hotel['name']}")
    lines.append(f"Check-in: {hotel['checkin']}")
    lines.append(f"Check-out: {hotel['checkout']}")
    lines.append(f"Wifi: {hotel['wifi']}")
    lines.append(f"Parking: {hotel['parking']}")
    lines.append(f"Mascotas: {hotel['pets']}")

    lines.append("\nServicios:")
    for s in info["services"]:
        lines.append(f"- {s}")

    lines.append("\nHabitaciones:")
    for r in info["rooms"]:
        desayuno = "con desayuno" if r["breakfast_included"] else "sin desayuno"
        lines.append(f"- {r['type']} ({r['capacity']} personas, {desayuno})")

    lines.append("\nRecomendaciones:")
    for p in info["recommendations"]["places"]:
        lines.append(f"- {p}")
    for r in info["recommendations"]["restaurants"]:
        lines.append(f"- {r}")
    activities = info.get("general_activities", {})

    if activities:
        lines.append("\nActividades generales cercanas:")

        if "rainy_day" in activities:
            lines.append("En días de lluvia:")
            for a in activities["rainy_day"]:
                lines.append(f"- {a}")

        if "with_kids" in activities:
            lines.append("Actividades para niños:")
            for a in activities["with_kids"]:
                lines.append(f"- {a}")

    return "\n".join(lines)
