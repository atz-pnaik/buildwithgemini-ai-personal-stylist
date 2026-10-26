"""Color palette and harmony tool for AI Personal Stylist using Colormind & TheColorAPI."""

import json
import urllib.request
from typing import Any, Dict, List, Optional

COLOR_MAP = {
    "black": [30, 30, 35],
    "charcoal": [54, 57, 63],
    "oatmeal": [214, 203, 185],
    "camel": [193, 154, 107],
    "champagne": [247, 231, 206],
    "navy": [26, 36, 56],
    "oxblood": [113, 28, 34],
    "gold": [212, 175, 55],
    "cream": [253, 246, 227],
}


def get_color_palette(
    anchor_color: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate a harmonious 5-color fashion palette to guide outfit coordination.

    Args:
        anchor_color: Optional starting color name (e.g. 'camel', 'navy', 'oatmeal', 'black')
                      to anchor the palette around.

    Returns:
        A dictionary with harmonious color recommendations, RGB values, and styling tips.
    """
    req_body: Dict[str, Any] = {"model": "default"}

    if anchor_color and anchor_color.lower() in COLOR_MAP:
        rgb = COLOR_MAP[anchor_color.lower()]
        req_body["input"] = [rgb, "N", "N", "N", "N"]

    try:
        url = "http://colormind.io/api/"
        data = json.dumps(req_body).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "AIPersonalStylist/1.0"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read().decode())
            palette = result.get("result", [])

        hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in palette]

        return {
            "anchor_color": anchor_color or "neutral foundation",
            "palette_rgb": palette,
            "palette_hex": hex_colors,
            "styling_tip": f"Pair dominant neutral tones ({hex_colors[0]}, {hex_colors[1]}) with accent highlights ({hex_colors[-1]}).",
        }
    except Exception as e:
        return {
            "anchor_color": anchor_color,
            "fallback_palette": ["#1a2438", "#c19a6b", "#d6cbb9", "#f7e7ce", "#711c22"],
            "error": str(e),
            "styling_tip": "Classic timeless harmony: Navy, Camel, Oatmeal, and Oxblood accents.",
        }
