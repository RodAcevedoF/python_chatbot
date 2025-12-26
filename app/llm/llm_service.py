from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage
from app.llm.vector_store import retrieve_relevant_context
from app.llm.history_context import build_history_context
from app.utils.llm_utils import normalize_response

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)

def llm_fallback_answer(user_message: str, history: list) -> str:
    # 1️⃣ Recuperar conocimiento relevante (RAG)
    knowledge = retrieve_relevant_context(user_message)

    # 2️⃣ Construir contexto conversacional
    history_ctx = build_history_context(history)

    system_prompt = (
        "Eres el asistente virtual oficial del Hotel Costa Azul.\n\n"

        "REGLAS IMPORTANTES:\n"
        "- Responde SOLO usando la información proporcionada.\n"
        "- NO inventes servicios, horarios ni precios.\n"
        "- Puedes combinar y reformular la información existente.\n"
        "- Si no hay información suficiente, deriva amablemente a recepción.\n\n"

        "CONOCIMIENTO DEL HOTEL (relevante para esta pregunta):\n"
        f"{knowledge}\n\n"

        "CONTEXTO DE LA CONVERSACIÓN (reciente):\n"
        f"{history_ctx}\n"
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]

    response = llm.invoke(messages).content
    return normalize_response(response)