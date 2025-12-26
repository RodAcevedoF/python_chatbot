from app.core.config.supabase_client import supabase
import logging

logger = logging.getLogger(__name__)

def add_message(session_id: str, sender: str, message: str):
    try:
        result = supabase.table("chat_messages").insert({
            "session_id": session_id,
            "sender": sender,
            "message": message
        }).execute()
        return result
    except Exception as e:
        logger.error(f"Failed to add message to Supabase: {e}")
        # Return None to allow the app to continue without DB
        return None


def get_history(session_id: str):
    try:
        response = (
            supabase
            .table("chat_messages")
            .select("sender, message, created_at")
            .eq("session_id", session_id)
            .order("created_at")
            .execute()
        )
        return response.data
    except Exception as e:
        logger.error(f"Failed to get history from Supabase: {e}")
        # Return empty list if DB fails
        return []
