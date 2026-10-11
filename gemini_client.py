import json
import re
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_OUTPUT_TOKENS, TEMPERATURE, DEMO_MODE

_client = None

def get_client():
    global _client
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file, or set DEMO_MODE=true to test without Gemini.")
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def generate_text(prompt: str) -> str:
    client = get_client()

    response = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt,
    )

    result = (getattr(response, "output_text", None) or "").strip()

    if not result:
        raise RuntimeError(
            "Gemini returned an empty response. Please try again."
        )

    return result

def parse_json(text: str):
    cleaned = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text, flags=re.I)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}|\[.*\]", cleaned, flags=re.S)
        if not match:
            raise ValueError("The AI response was not valid JSON. Please try again.")
        return json.loads(match.group(0))
