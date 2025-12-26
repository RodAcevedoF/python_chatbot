from app.intents import detect_intent
from app import responses
from app.llm.chat_history import add_message, get_history
from app.llm.llm_service import llm_fallback_answer


def process_message(message: str, session_id: str):
    add_message(session_id, "user", message)

    history = get_history(session_id) or []

    intent = detect_intent(message)

    match intent:
        case "greeting":
            reply = responses.greeting_response()
        case "horarios":
            reply = responses.horarios_response()
        case "servicios":
            reply = responses.servicios_response()
        case "habitaciones":
            reply = responses.habitaciones_response()
        case "recomendaciones":
            reply = responses.recomendaciones_response()
        case "humano":
            reply = responses.humano_response()
        case "fallback":
            reply = llm_fallback_answer(message, history)
        case _:
            reply = responses.fallback_response()

    add_message(session_id, "bot", reply)

    history = get_history(session_id) or []

    return reply, intent, history
