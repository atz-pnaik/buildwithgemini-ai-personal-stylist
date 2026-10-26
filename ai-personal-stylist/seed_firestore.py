"""Seed script for Aritzia-focused AI Personal Stylist Firestore database."""

import sys
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-1106e44fd3f9"

ARITZIA_CATALOG = [
    # Tops / Knitwear
    {
        "id": "aritzia_top_01",
        "name": "Babaton Contour Crew Longsleeve",
        "brand": "Babaton (Aritzia)",
        "store": "Aritzia",
        "category": "top",
        "color": "Black",
        "price": 58.00,
        "season": ["fall", "winter", "spring", "all"],
        "vibe": ["minimalist", "elevated", "sleek", "dinner"],
        "tags": ["contour", "double-layer", "fitted", "layering", "dinner", "birthday"],
        "description": "Double-layered luxe fabric engineered for an ultra-smoothing, second-skin fit.",
        "image_url": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500"
    },
    {
        "id": "aritzia_top_02",
        "name": "Sunday Best Peggy Crewneck Sweater",
        "brand": "Sunday Best (Aritzia)",
        "store": "Aritzia",
        "category": "top",
        "color": "Oatmeal Heather",
        "price": 98.00,
        "season": ["fall", "winter", "spring"],
        "vibe": ["cozy", "elevated casual", "chic"],
        "tags": ["sweater", "knit", "crewneck", "warm", "dinner"],
        "description": "Fluffy ribbed crewneck sweater spun from ultra-soft wool and alpaca blend.",
        "image_url": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=500"
    },
    {
        "id": "aritzia_top_03",
        "name": "Wilfred Novella Silk Blouse",
        "brand": "Wilfred (Aritzia)",
        "store": "Aritzia",
        "category": "top",
        "color": "Champagne / Birch",
        "price": 128.00,
        "season": ["all", "fall", "spring"],
        "vibe": ["romantic", "elevated", "dinner", "formal"],
        "tags": ["silk", "blouse", "corset-inspired", "birthday", "evening"],
        "description": "Delicate draped neckline blouse crafted from 100% mulberry silk with slight stretch.",
        "image_url": "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=500"
    },
    {
        "id": "aritzia_top_04",
        "name": "Babaton Sculpt Knit Squareneck Tank",
        "brand": "Babaton (Aritzia)",
        "store": "Aritzia",
        "category": "top",
        "color": "Bone / Off-White",
        "price": 68.00,
        "season": ["all", "fall", "spring", "summer"],
        "vibe": ["minimalist", "tailored", "elevated"],
        "tags": ["sculpt knit", "layering", "tank", "dinner", "blazer-base"],
        "description": "Signature medium-compression ribbed knit tank designed to hold and sculpt your shape.",
        "image_url": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500"
    },

    # Bottoms (Pants & Trousers)
    {
        "id": "aritzia_bottom_01",
        "name": "The Effortless Pant™ Wide-Leg",
        "brand": "Wilfred (Aritzia)",
        "store": "Aritzia",
        "category": "bottom",
        "color": "Charcoal Grey",
        "price": 148.00,
        "season": ["all", "fall", "winter", "spring"],
        "vibe": ["tailored", "elevated", "chic", "effortless", "dinner"],
        "tags": ["effortless pant", "pants", "trousers", "pleated", "wide-leg", "bestseller"],
        "description": "Aritzia's iconic high-rise tailored trousers with a relaxed wide leg and fluid Japanese crepette drape.",
        "image_url": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500"
    },
    {
        "id": "aritzia_bottom_02",
        "name": "Babaton Agency Pant Tailored",
        "brand": "Babaton (Aritzia)",
        "store": "Aritzia",
        "category": "bottom",
        "color": "Matte Black",
        "price": 138.00,
        "season": ["fall", "winter", "spring"],
        "vibe": ["sharp", "tailored", "modern", "formal"],
        "tags": ["pants", "straight-leg", "wool-blend", "minimalist", "dinner"],
        "description": "High-waisted tailored straight-leg pants crafted from refined crease-resistant fabric.",
        "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=500"
    },
    {
        "id": "aritzia_bottom_03",
        "name": "Denim Forum The Joni High-Rise Loose",
        "brand": "Denim Forum (Aritzia)",
        "store": "Aritzia",
        "category": "bottom",
        "color": "Stay Black",
        "price": 110.00,
        "season": ["all", "fall", "winter", "spring"],
        "vibe": ["elevated casual", "cool", "relaxed"],
        "tags": ["denim", "jeans", "organic cotton", "casual"],
        "description": "Vintage-inspired 90s relaxed straight fit denim in rich non-fade black.",
        "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500"
    },

    # Outerwear / Blazers
    {
        "id": "aritzia_outer_01",
        "name": "Babaton The Slouch™ Wool-Cashmere Coat",
        "brand": "Babaton (Aritzia)",
        "store": "Aritzia",
        "category": "outerwear",
        "color": "Camel / Gold Camel",
        "price": 398.00,
        "season": ["fall", "winter"],
        "vibe": ["elevated", "sophisticated", "warm", "luxury"],
        "tags": ["the slouch", "coat", "wool", "cashmere", "winter", "toronto", "iconic"],
        "description": "Aritzia's hallmark relaxed oversized tailored coat crafted from double-faced virgin wool and cashmere.",
        "image_url": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=500"
    },
    {
        "id": "aritzia_outer_02",
        "name": "Wilfred Destiny Oversized Blazer",
        "brand": "Wilfred (Aritzia)",
        "store": "Aritzia",
        "category": "outerwear",
        "color": "Total Eclipse Navy",
        "price": 198.00,
        "season": ["all", "fall", "spring", "winter"],
        "vibe": ["tailored", "smart-casual", "elevated", "dinner"],
        "tags": ["blazer", "oversized", "jacket", "layering", "birthday"],
        "description": "Single-breasted relaxed menswear-inspired blazer cut from fluid suiting twill.",
        "image_url": "https://images.unsplash.com/photo-1551232864-3f0890e580d9?w=500"
    },

    # Shoes & Footwear (Aritzia Curated)
    {
        "id": "aritzia_shoes_01",
        "name": "Aritzia Curated Sleek Pointed Leather Ankle Boot",
        "brand": "Aritzia Footwear",
        "store": "Aritzia",
        "category": "shoes",
        "color": "Black Leather",
        "price": 160.00,
        "season": ["fall", "winter", "spring"],
        "vibe": ["elevated", "sleek", "dinner", "evening"],
        "tags": ["boots", "leather", "pointed", "ankle-boot"],
        "description": "Smooth calfskin ankle boots with an architectural low block heel and elongated toe.",
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500"
    },
    {
        "id": "aritzia_shoes_02",
        "name": "Aritzia Curated Lug-Sole Penny Loafer",
        "brand": "Aritzia Footwear",
        "store": "Aritzia",
        "category": "shoes",
        "color": "Deep Cherry / Oxblood",
        "price": 140.00,
        "season": ["fall", "spring", "winter"],
        "vibe": ["smart-casual", "trendy", "elevated"],
        "tags": ["loafers", "lug-sole", "leather", "comfortable"],
        "description": "Polished box-leather loafers with a chunky lightweight tread sole.",
        "image_url": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500"
    },

    # Accessories
    {
        "id": "aritzia_acc_01",
        "name": "Babaton Twisted Chunky Gold Hoops",
        "brand": "Babaton (Aritzia)",
        "store": "Aritzia",
        "category": "accessories",
        "color": "14k Gold Vermeil",
        "price": 45.00,
        "season": ["all"],
        "vibe": ["elevated", "chic", "dinner", "minimalist"],
        "tags": ["earrings", "gold", "jewelry", "hoops"],
        "description": "Twisted silhouette tubular hoop earrings plated in heavy 14k gold vermeil.",
        "image_url": "https://images.unsplash.com/photo-1630019852942-f89202989a59?w=500"
    },
    {
        "id": "aritzia_acc_02",
        "name": "Auxiliary Box Minimal Leather Crossbody",
        "brand": "Auxiliary (Aritzia)",
        "store": "Aritzia",
        "category": "accessories",
        "color": "Rich Cognac",
        "price": 98.00,
        "season": ["all"],
        "vibe": ["elevated", "casual", "dinner"],
        "tags": ["bag", "crossbody", "leather", "clean"],
        "description": "Structured smooth leather shoulder bag with understated brushed gold hardware.",
        "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500"
    }
]

def seed():
    print(f"Connecting to Firestore for project '{PROJECT_ID}'...")
    db = firestore.Client(project=PROJECT_ID)
    catalog_ref = db.collection("catalog")

    # Clear previous seeded test items
    for doc in catalog_ref.stream():
        doc.reference.delete()

    for item in ARITZIA_CATALOG:
        catalog_ref.document(item["id"]).set(item)
        print(f"  ✓ Seeded Aritzia item: {item['name']} ({item['brand']} - ${item['price']})")

    print(f"\nSuccessfully seeded {len(ARITZIA_CATALOG)} 100% Aritzia catalog items to Firestore!")

if __name__ == "__main__":
    try:
        seed()
    except Exception as e:
        print(f"Error seeding Firestore: {e}", file=sys.stderr)
        sys.exit(1)
