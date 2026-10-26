"""Weather tool for destination climate and forecasting in AI Personal Stylist."""

import json
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

# WMO Weather interpretation codes (http://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM)
WMO_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
}


def get_destination_weather(
    location: str,
    time_of_year: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch real-time weather and forecast data for an event destination or city.

    Args:
        location: City or destination name (e.g., 'Toronto', 'New York', 'Paris').
        time_of_year: Optional month or season (e.g. 'November', 'winter') for additional styling context.

    Returns:
        A dictionary containing destination temperature, conditions, recommendations for layers, and warmth notes.
    """
    try:
        encoded_loc = urllib.parse.quote(location)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_loc}&count=1&language=en&format=json"
        req = urllib.request.Request(geo_url, headers={"User-Agent": "AIPersonalStylist/1.0"})

        with urllib.request.urlopen(req, timeout=5) as resp:
            geo_data = json.loads(resp.read().decode())

        if not geo_data.get("results"):
            return {
                "location": location,
                "summary": f"Could not determine exact forecast for {location}. Fall/winter dressing recommended if in a temperate zone.",
                "season_hint": time_of_year or "unknown",
            }

        loc_match = geo_data["results"][0]
        lat = loc_match["latitude"]
        lon = loc_match["longitude"]
        resolved_name = f"{loc_match.get('name')}, {loc_match.get('country')}"

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,apparent_temperature,weather_code,wind_speed_10m"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
            f"&timezone=auto"
        )
        req_w = urllib.request.Request(weather_url, headers={"User-Agent": "AIPersonalStylist/1.0"})
        with urllib.request.urlopen(req_w, timeout=5) as resp:
            w_data = json.loads(resp.read().decode())

        current = w_data.get("current", {})
        daily = w_data.get("daily", {})

        current_temp_c = current.get("temperature_2m")
        feels_like_c = current.get("apparent_temperature")
        weather_code = current.get("weather_code", 0)
        condition = WMO_CODE_MAP.get(weather_code, "Variably cloudy")

        # Convert to Fahrenheit for user convenience as well
        current_temp_f = round((current_temp_c * 9 / 5) + 32, 1) if current_temp_c is not None else None
        feels_like_f = round((feels_like_c * 9 / 5) + 32, 1) if feels_like_c is not None else None

        high_c = daily.get("temperature_2m_max", [None])[0]
        low_c = daily.get("temperature_2m_min", [None])[0]
        high_f = round((high_c * 9 / 5) + 32, 1) if high_c is not None else None
        low_f = round((low_c * 9 / 5) + 32, 1) if low_c is not None else None
        rain_prob = daily.get("precipitation_probability_max", [None])[0]

        # Suggest styling/layering advice based on temp
        if current_temp_c is not None and current_temp_c < 5:
            styling_advice = "Freezing/very cold: Heavy wool coat, thermal knit or cashmere, boots, and warm trousers required."
        elif current_temp_c is not None and current_temp_c < 15:
            styling_advice = "Chilly/cool: Warm layers needed (sweater, blazer or mid-weight coat, closed-toe shoes)."
        elif current_temp_c is not None and current_temp_c < 22:
            styling_advice = "Mild: Light jacket or blazer, breathable shirts, comfortable pants or skirts."
        else:
            styling_advice = "Warm: Breathable fabrics (linen, silk, cotton), lighter layers."

        return {
            "resolved_location": resolved_name,
            "condition": condition,
            "current_temp": f"{current_temp_c}°C / {current_temp_f}°F",
            "feels_like": f"{feels_like_c}°C / {feels_like_f}°F",
            "daily_range": f"{low_c}°C ({low_f}°F) to {high_c}°C ({high_f}°F)",
            "rain_probability": f"{rain_prob}%" if rain_prob is not None else "0%",
            "styling_advice": styling_advice,
            "noted_time_of_year": time_of_year,
        }

    except Exception as e:
        return {
            "location": location,
            "error": str(e),
            "fallback_advice": "Check seasonal averages; prepare a light outer layer.",
        }
