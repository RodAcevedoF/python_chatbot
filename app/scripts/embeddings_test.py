import argparse
import sys
from app.data_loader import load_hotel_info
from langchain_openai import OpenAIEmbeddings

try:
    from app.core.config.supabase_client import supabase
    supabase_import_error = None
except Exception as e:
    supabase = None
    supabase_import_error = e


def build_documents(info: dict) -> list:
    docs = [
        f"Wifi del hotel: {info['hotel']['wifi']}",
        f"Parking: {info['hotel']['parking']}",
        f"Check-in: {info['hotel']['checkin']}",
        f"Check-out: {info['hotel']['checkout']}",
    ]

    for s in info.get("services", []):
        docs.append(f"Servicio del hotel: {s}")

    for r in info.get("rooms", []):
        docs.append(f"Habitación {r['type']} para {r['capacity']} personas")

    for a in info.get("general_activities", {}).get("rainy_day", []):
        docs.append(f"Actividad en día de lluvia: {a}")

    for a in info.get("general_activities", {}).get("with_kids", []):
        docs.append(f"Actividad para niños: {a}")

    if "address" in info:
        addr = info["address"]
        docs.append(f"Dirección: {addr.get('street', '')}, {addr.get('city', '')} {addr.get('postal_code', '')}, {addr.get('country', '')}")
        docs.append(f"Coordenadas: lat {addr.get('lat')}, lng {addr.get('lng')}")

    if "photos" in info:
        for p in info["photos"]:
            docs.append(f"Foto del hotel: {p}")

    if "rating" in info:
        docs.append(f"Valoración media: {info['rating'].get('average')}")
        for rev in info['rating'].get('reviews', []):
            docs.append(f"Reseña: {rev.get('user')} puntuación {rev.get('score')}: {rev.get('text')}")

    if "policies" in info:
        for k, v in info['policies'].items():
            docs.append(f"Política {k}: {v}")

    if "faqs" in info:
        for f in info['faqs']:
            docs.append(f"FAQ: {f.get('q')} - {f.get('a')}")

    if "hours" in info:
        for k, v in info['hours'].items():
            docs.append(f"Horario {k}: {v}")

    if "payment_methods" in info:
        docs.append("Métodos de pago: " + ", ".join(info["payment_methods"]))

    if "amenities" in info:
        for a in info['amenities']:
            docs.append(f"Amenidad: {a.get('name')} - {a.get('description', '')}")

    if "accessibility" in info:
        acc = info['accessibility']
        acc_items = [k for k, v in acc.items() if v]
        docs.append("Accesibilidad: " + ", ".join(acc_items))

    if "transport" in info:
        for k, v in info['transport'].items():
            docs.append(f"Transporte {k}: {v}")

    if "languages_spoken" in info:
        docs.append("Idiomas hablados: " + ", ".join(info['languages_spoken']))

    if "special_offers" in info:
        for s in info['special_offers']:
            docs.append(f"Oferta: {s.get('title')} - {s.get('description')} (validez: {s.get('valid_until')})")

    return docs


def main(dry_run: bool = False, compute_embeddings: bool = False):
    info = load_hotel_info()
    documents = build_documents(info)

    if dry_run:
        print(f"Dry run: {len(documents)} documents to index\n")
        for i, d in enumerate(documents, start=1):
            print(f"{i}. {d}\n")

        if compute_embeddings:
            print("\nComputing embeddings for first 3 documents (preview)...")
            try:
                emb = OpenAIEmbeddings(model="text-embedding-3-small")
                for d in documents[:3]:
                    v = emb.embed_query(d)
                    print(f"- doc[0:60]: {d[:60]!r} -> embedding length: {len(v)}")
            except Exception as e:
                print("Failed to compute embeddings (are API keys set?):", e)
        return

    if supabase is None:
        raise RuntimeError(f"Supabase client not available: {supabase_import_error}")

    emb = OpenAIEmbeddings(model="text-embedding-3-small")

    insert_count = 0
    for doc in documents:
        vec = emb.embed_query(doc)
        supabase.table("hotel_knowledge").insert({
            "content": doc,
            "embedding": vec
        }).execute()
        insert_count += 1
        print(f"Inserted {insert_count}: {doc[:80]}")

    print(f"Done. Inserted {insert_count} documents into Supabase.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index hotel info into Supabase (or dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="Print documents without inserting to Supabase")
    parser.add_argument("--compute-embeddings", action="store_true", help="Compute embeddings during dry-run (may require API keys)")
    args = parser.parse_args()

    try:
        main(dry_run=args.dry_run, compute_embeddings=args.compute_embeddings)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)
