from app.core.config.supabase_client import supabase
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def retrieve_relevant_context(query: str, k: int = 4) -> str:
    query_embedding = embeddings.embed_query(query)

    response = supabase.rpc(
        "match_hotel_knowledge",
        {
            "query_embedding": query_embedding,
            "match_count": k
        }
    ).execute()

    data = response.data

    if data is None:
        return ""

    if isinstance(data, dict):
        rows = [data]
    elif isinstance(data, (list, tuple)):
        rows = list(data)
    else:
        return ""

    contents = []
    for row in rows:
        if isinstance(row, dict):
            content = row.get("content")
            if content is not None:
                contents.append(str(content))

    return "\n".join(contents)
