"""Firestore client and tools for AI Personal Stylist (100% Aritzia Catalog)."""

import datetime
from typing import Any, Dict, List, Optional
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-1106e44fd3f9"

_db: Optional[firestore.Client] = None

def get_firestore_client() -> firestore.Client:
    """Lazy initialize and return the Firestore client using hardcoded PROJECT_ID."""
    global _db
    if _db is None:
        _db = firestore.Client(project=PROJECT_ID)
    return _db


def search_catalog(
    category: Optional[str] = None,
    season: Optional[str] = None,
    vibe: Optional[str] = None,
    max_price: Optional[float] = None,
    color: Optional[str] = None,
    store: Optional[str] = "Aritzia",
) -> List[Dict[str, Any]]:
    """Search the 100% Aritzia clothing and accessories catalog.

    Args:
        category: Optional category filter: 'top', 'bottom', 'outerwear', 'shoes', or 'accessories'.
        season: Optional season filter: 'fall', 'winter', 'spring', or 'summer'.
        vibe: Optional style/vibe filter (e.g., 'elevated', 'tailored', 'chic', 'minimalist', 'dinner').
        max_price: Optional maximum price in dollars.
        color: Optional color keyword (e.g., 'black', 'oatmeal', 'charcoal', 'camel').
        store: Store filter (defaults to 'Aritzia').

    Returns:
        A list of matching Aritzia clothing/accessory item dictionaries.
    """
    db = get_firestore_client()
    query = db.collection("catalog")

    if store:
        query = query.where("store", "==", store.strip())

    if category:
        query = query.where("category", "==", category.lower())

    results: List[Dict[str, Any]] = []
    docs = query.stream()

    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id

        if max_price is not None and item.get("price", 0) > max_price:
            continue

        if season:
            item_seasons = [s.lower() for s in item.get("season", [])]
            if "all" not in item_seasons and season.lower() not in item_seasons:
                continue

        if vibe:
            vibe_lower = vibe.lower()
            item_vibes = [v.lower() for v in item.get("vibe", [])]
            item_tags = [t.lower() for t in item.get("tags", [])]
            if not any(vibe_lower in v for v in item_vibes) and not any(vibe_lower in t for t in item_tags):
                continue

        if color:
            color_lower = color.lower()
            if color_lower not in item.get("color", "").lower():
                continue

        results.append(item)

    return results


def save_look(
    look_name: str,
    item_ids: List[str],
    occasion: str,
    styling_notes: Optional[str] = None,
) -> Dict[str, Any]:
    """Save an Aritzia outfit look to user's saved looks in Firestore.

    Args:
        look_name: Catchy name for the outfit look (e.g. 'Aritzia Effortless Dinner Look').
        item_ids: List of Aritzia catalog item IDs included in the outfit.
        occasion: The occasion and styling context for this outfit.
        styling_notes: Explanation of why this look works or special styling tips.

    Returns:
        A confirmation dict with look_id, look_name, total_price, and status.
    """
    db = get_firestore_client()
    items_ref = db.collection("catalog")

    selected_items: List[Dict[str, Any]] = []
    total_price = 0.0

    for item_id in item_ids:
        doc = items_ref.document(item_id).get()
        if doc.exists:
            item_data = doc.to_dict()
            item_data["id"] = doc.id
            selected_items.append(item_data)
            total_price += item_data.get("price", 0.0)

    look_record = {
        "look_name": look_name,
        "name": look_name,
        "store": "Aritzia",
        "occasion": occasion,
        "item_ids": item_ids,
        "items": selected_items,
        "total_price": round(total_price, 2),
        "styling_notes": styling_notes or "",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    doc_ref = db.collection("saved_looks").add(look_record)
    look_id = doc_ref[1].id

    return {
        "status": "success",
        "look_id": look_id,
        "look_name": look_name,
        "total_price": round(total_price, 2),
        "item_count": len(selected_items),
        "message": f"Successfully saved Aritzia look '{look_name}' with {len(selected_items)} pieces ($ {round(total_price, 2)} total)."
    }


def get_saved_looks() -> List[Dict[str, Any]]:
    """Retrieve all previously saved looks from Firestore.

    Returns:
        A list of previously saved outfit looks with their items, prices, and notes.
    """
    db = get_firestore_client()
    docs = db.collection("saved_looks").order_by("created_at", direction=firestore.Query.DESCENDING).stream()

    saved_list: List[Dict[str, Any]] = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        saved_list.append(data)

    return saved_list
