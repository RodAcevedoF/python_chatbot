def build_history_context(history: list, limit: int = 4) -> str:
    if not history:
        return ""

    recent = history[-limit:]
    lines = []

    for m in recent:
        role = "Usuario" if m["sender"] == "user" else "Asistente"
        lines.append(f"{role}: {m['message']}")

    return "\n".join(lines)
