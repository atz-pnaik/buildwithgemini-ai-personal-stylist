"""Visual lookbook generation tool for AI Personal Stylist."""

import datetime
from typing import Any, Dict, List, Optional
from google.cloud import firestore, storage
from google import genai

PROJECT_ID = "qwiklabs-gcp-04-1106e44fd3f9"
BUCKET_NAME = "ai-personal-stylist-assets-1106e44f"

_db = None
_storage_client = None

def get_firestore_client():
    global _db
    if _db is None:
        _db = firestore.Client(project=PROJECT_ID)
    return _db

def get_storage_client():
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client(project=PROJECT_ID)
    return _storage_client


def generate_lookbook_visual(
    look_name: str,
    item_ids: List[str],
    occasion: str,
    vibe_description: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate an editorial lookbook visual description and mock render card for an outfit ensemble.

    Args:
        look_name: Name of the outfit (e.g. 'Toronto Evening Cashmere Look').
        item_ids: List of catalog item IDs comprising the look.
        occasion: Event occasion and setting (e.g. 'Birthday Dinner in Toronto').
        vibe_description: Optional custom vibe notes or aesthetic direction.

    Returns:
        A dictionary containing the visual lookbook preview details and public image link.
    """
    db = get_firestore_client()
    items_ref = db.collection("catalog")
    
    item_names = []
    item_colors = []
    item_photos = []
    total_price = 0.0

    for item_id in item_ids:
        doc = items_ref.document(item_id).get()
        if doc.exists:
            data = doc.to_dict()
            item_names.append(data.get("name", item_id))
            item_colors.append(f"{data.get('color', '')} {data.get('category', '')}".strip())
            total_price += data.get("price", 0.0)
            if data.get("image_url"):
                item_photos.append(data.get("image_url"))

    # Select representative hero image from catalog items if available, or fallback to an aesthetic lookbook asset
    hero_image_url = item_photos[0] if item_photos else "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800"

    lookbook_entry = {
        "look_name": look_name,
        "occasion": occasion,
        "items": item_names,
        "palette": item_colors,
        "total_cost": round(total_price, 2),
        "visual_concept": (
            f"Editorial studio lookbook photograph featuring {', '.join(item_names)}. "
            f"Styled for a {occasion} with an aesthetic focused on {vibe_description or 'refined minimalism'}."
        ),
        "lookbook_image_url": hero_image_url,
        "status": "ready"
    }

    return lookbook_entry
