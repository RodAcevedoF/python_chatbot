from app.core.config.supabase_client import supabase
from app.data_loader import load_hotel_info
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

info = load_hotel_info()

documents = [
    f"Wifi del hotel: {info['hotel']['wifi']}",
    f"Parking: {info['hotel']['parking']}",
    f"Check-in: {info['hotel']['checkin']}",
    f"Check-out: {info['hotel']['checkout']}",
]

for s in info["services"]:
    documents.append(f"Servicio del hotel: {s}")

for r in info["rooms"]:
    documents.append(
        f"Habitación {r['type']} para {r['capacity']} personas"
    )

for a in info["general_activities"]["rainy_day"]:
    documents.append(f"Actividad en día de lluvia: {a}")

for a in info["general_activities"]["with_kids"]:
    documents.append(f"Actividad para niños: {a}")

for doc in documents:
    vec = embeddings.embed_query(doc)

    supabase.table("hotel_knowledge").insert({
        "content": doc,
        "embedding": vec
    }).execute()
