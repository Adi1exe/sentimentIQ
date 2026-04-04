import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure the OpenAI API client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are an expert Sentiment Analysis engine for a B2B sales intelligence platform.

Given a raw customer complaint, review, feedback, or business text, you must output a structured JSON object with EXACTLY these fields:

{
  "sentiment": "<Positive | Negative | Neutral | Mixed>",
  "score": <integer 1-5, where 1=very negative, 3=neutral, 5=very positive>,
  "confidence": <float 0.0 to 1.0>,
  "root_issue": "<one concise phrase describing the core problem or topic>",
  "key_themes": ["<theme1>", "<theme2>", "<theme3>"],
  "urgency": "<Low | Medium | High | Critical>",
  "draft_response": "<A professional, empathetic draft reply addressing the root issue in 2-3 sentences>"
}

Rules:
- Output ONLY valid JSON. No markdown, no backticks, no extra text.
- sentiment must be one of: Positive, Negative, Neutral, Mixed
- urgency is based on emotional intensity and business impact
- draft_response should match the sentiment — empathetic for negative, grateful for positive
- key_themes should be 2-4 short phrases (e.g., "delivery delay", "billing error", "product quality")
"""

def analyze_single(text: str) -> dict:
    """Analyze a single piece of text and return structured sentiment data using the OpenAI API."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analyze the sentiment of this text:\n\n{text}"}
        ],
        response_format={ "type": "json_object" },
        temperature=0.0
    )
    
    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if any
    raw = re.sub(r"```json|```", "", raw, flags=re.IGNORECASE).strip()
    result = json.loads(raw)
    result["input_text"] = text
    return result

def analyze_batch(texts: list[str]) -> list[dict]:
    """Analyze multiple texts and return list of results."""
    results = []
    for text in texts:
        try:
            result = analyze_single(text)
            results.append(result)
        except Exception as e:
            results.append({
                "input_text": text,
                "sentiment": "Error",
                "score": 0,
                "confidence": 0.0,
                "root_issue": f"Analysis failed: {str(e)}",
                "key_themes": [],
                "urgency": "Low",
                "draft_response": ""
            })
    return results
