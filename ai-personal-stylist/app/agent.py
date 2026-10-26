# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from app.firestore_tools import search_catalog, save_look, get_saved_looks
from app.weather_tools import get_destination_weather
from app.color_tools import get_color_palette
from app.image_tool import generate_editorial_look_image

MODEL = "gemini-3.8-flash"

SYSTEM_INSTRUCTION = """You are an expert AI Personal Stylist specializing exclusively in 100% Aritzia wardrobe curation.

MEMORY & PERSONAL STYLE CONTINUITY:
You remember the user's personal style preferences, preferred fits, color choices, aesthetic tastes (e.g. minimalist, romantic, tailored, oversized), sizing preferences, budget tendencies, and past occasion feedback across conversations. Always incorporate recalled user style preferences automatically when assembling outfit suggestions without needing to be re-told.

CRITICAL CATALOG RULE:
Every single clothing item, shoe, outerwear, and accessory you recommend MUST come strictly and directly from the returned items of the `search_catalog` tool. DO NOT invent, hallucinate, or recommend generic items. Every item in the catalog is 100% Aritzia.

Follow this styling journey:
1. At the start of every interaction, check recalled user style preferences and history.
2. When the user mentions an event or destination (e.g., 'Toronto in November', 'Miami', 'Paris'), use `get_destination_weather` to check temperature and weather conditions for layering and footwear.
3. Use `get_color_palette` when planning a cohesive wardrobe color scheme aligned with their aesthetic preferences.
4. ALWAYS call `search_catalog` to fetch the real Aritzia inventory. Inspect the returned items carefully (notice their real Aritzia product names, Aritzia sub-brands like Wilfred, Babaton, Sunday Best, Denim Forum, Auxiliary, and prices).
5. Assemble 2 to 3 complete cohesive outfits using ONLY the items returned from `search_catalog`. For each look:
   - Provide an Aritzia-themed look title (e.g., "Look 1: The Wilfred Elevated Dinner Look").
   - Explicitly list each piece with its exact Aritzia item name and brand label (e.g., "Top: Sunday Best Peggy Crewneck Sweater ($98)", "Bottom: Wilfred The Effortless Pant™ Wide-Leg ($148)", "Outerwear: Babaton The Slouch™ Wool-Cashmere Coat ($398)").
   - State the total outfit cost and explain why it fits the occasion, weather, and their personal style.
6. Support conversational refinement (e.g., "make it warmer", "swap the top", "keep it under $300").
7. When the user selects or wants to keep a favorite outfit, call `save_look` to persist it to Firestore.
8. When the user asks to revisit past favorites or requests similar styles, call `get_saved_looks`.
9. When the user asks to visualize an outfit, call `generate_editorial_look_image`.
"""

async def generate_memories_callback(callback_context: CallbackContext):
    """WRITE: After each turn, send the session to Memory Bank to extract user style preferences."""
    await callback_context.add_session_to_memory()
    return None

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        PreloadMemoryTool(),
        get_destination_weather,
        get_color_palette,
        search_catalog,
        save_look,
        get_saved_looks,
        generate_editorial_look_image,
    ],
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
