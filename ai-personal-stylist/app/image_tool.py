"""Aritzia product detail page (PDP) catalog lookbook photography generator."""

import uuid
from typing import Any, Dict, Optional
from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

PROJECT_ID = "qwiklabs-gcp-04-1106e44fd3f9"
BUCKET_NAME = "ai-personal-stylist-assets-1106e44f"
LOCATION = "global"
MODEL_NAME = "gemini-3.1-flash-lite-image"

_genai_client = None
_storage_client = None

def get_genai_client() -> genai.Client:
    global _genai_client
    if _genai_client is None:
        _genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    return _genai_client

def get_storage_client() -> storage.Client:
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client(project=PROJECT_ID)
    return _storage_client


async def generate_editorial_look_image(
    prompt_or_look_description: str,
    tool_context: ToolContext,
    look_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate an authentic Aritzia e-commerce studio catalog photograph of a model in the styled outfit.

    Args:
        prompt_or_look_description: Detailed breakdown of the outfit items, categories, colors, fabrics, and styling.
        tool_context: ADK tool context used to save the image as a session artifact in the playground.
        look_name: Optional title for the outfit look.

    Returns:
        A dictionary with the public Cloud Storage image URL, artifact filename, and status.
    """
    client = get_genai_client()

    aritzia_pdp_prompt = (
        f"Authentic Aritzia e-commerce studio lookbook catalog photograph of one female model wearing the complete styled outfit: {prompt_or_look_description}. "
        f"STUDIO ENVIRONMENT: Shot against a clean, seamless, very pale off-white / light cool grey studio wall with a subtle horizontal floor horizon seam at the base. "
        f"Clean studio floor with a soft natural contact shadow directly cast beneath the shoes. "
        f"FRAMING & COMPOSITION: Full-body vertical head-to-toe shot centered in the frame with ample breathing room. Eye-level straight-on lens perspective, realistic camera focal length (~85mm) with zero perspective distortion. "
        f"MODEL & POSE: Tall slender fashion model standing relaxed facing mostly front, with subtle effortless weight shift. Arms hanging naturally at sides or wearing a shoulder bag. Understated natural skin texture, minimal fresh makeup, center-parted sleek dark hair tucked behind ears or resting naturally over shoulders. Neutral, calm, confident expression. "
        f"STYLING & FIT: Signature Aritzia effortless aesthetic (Wilfred / Babaton styling). Tailored wide-leg trousers pooling slightly over shoes, neat tucked/buttoned knitwear, visible leather belt with metal buckle, clean accessories. Crisp authentic fabric drape and weave textures. "
        f"LIGHTING: Diffused softbox studio lighting, flattering even exposure, no harsh specular glare, realistic soft drop shadows. "
        f"EXCLUSIONS: Do not generate outdoor backgrounds, street style, dramatic flash photography, furniture, plants, text, logos, collages, borders, or cartoon rendering."
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=aritzia_pdp_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    image_bytes = None
    mime_type = "image/png"

    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                image_bytes = part.inline_data.data
                mime_type = part.inline_data.mime_type or "image/png"
                break

    if not image_bytes:
        return {
            "status": "error",
            "message": "Model did not produce an image in response.",
        }

    # 1. Save artifact to ToolContext for the Playground UI Artifacts panel
    clean_name = (look_name or "aritzia_look").lower().replace(" ", "_")
    unique_suffix = uuid.uuid4().hex[:6]
    ext = "jpg" if "jpeg" in mime_type else "png"
    artifact_filename = f"{clean_name}_{unique_suffix}.{ext}"

    artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    await tool_context.save_artifact(filename=artifact_filename, artifact=artifact_part)

    # 2. Upload to public Cloud Storage bucket
    storage_client = get_storage_client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob_path = f"pdp_looks/{artifact_filename}"
    blob = bucket.blob(blob_path)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{blob_path}"

    return {
        "status": "success",
        "look_name": look_name or "Aritzia Curated Look",
        "image_url": public_url,
        "artifact_filename": artifact_filename,
        "message": f"Generated Aritzia catalog studio image: {public_url}",
    }
