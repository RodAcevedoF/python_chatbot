import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / 'data' / 'hotel_info.json'

def load_hotel_info() -> dict:
    """Load hotel information from a JSON file."""
    with open(DATA_PATH, 'r', encoding='utf-8') as file:
        hotel_info = json.load(file)
    return hotel_info