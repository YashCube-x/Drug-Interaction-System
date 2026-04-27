"""
LLM module – all OpenRouter API calls live here.
Uses the OpenAI-compatible client pointed at OpenRouter.
"""

import os
import json
import logging
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


def _call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
    """Low-level helper that calls OpenRouter and returns the assistant message."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=1024,
        )
        content = response.choices[0].message.content.strip()
        logger.debug(f"LLM response: {content[:200]}...")
        return content
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise


# ── 1. Extract drug names from free text ────────────────────────────────────

def extract_drugs(text: str) -> List[str]:
    """Use LLM to extract drug / medication names from a sentence."""
    system_prompt = (
        "You are a pharmacology expert. Extract ALL drug and medication names "
        "from the user's text. Return ONLY a valid JSON array of strings, "
        "nothing else. Example: [\"Aspirin\", \"Metformin\"]"
    )
    raw = _call_llm(system_prompt, text)

    # Try to parse JSON array from the response
    try:
        # Handle cases where LLM wraps in markdown code blocks
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
            cleaned = cleaned.rsplit("```", 1)[0].strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()

        drugs = json.loads(cleaned)
        if isinstance(drugs, list):
            return [str(d).strip() for d in drugs if str(d).strip()]
    except json.JSONDecodeError:
        logger.warning(f"Could not parse LLM drug extraction output: {raw}")

    # Fallback: split by commas / newlines
    fallback = [d.strip().strip('"').strip("'") for d in raw.replace("\n", ",").split(",")]
    return [d for d in fallback if d and len(d) > 1]


# ── 2. Simplify a raw interaction description ───────────────────────────────

def simplify_interaction(drug_a: str, drug_b: str, raw_text: str) -> Dict[str, Any]:
    """
    Given a raw interaction description from the database, use LLM to produce
    a structured, simplified explanation.
    """
    system_prompt = (
        "You are a clinical pharmacology expert explaining drug interactions to patients. "
        "Given a raw drug interaction description, return a JSON object with EXACTLY these keys:\n"
        '  "interaction": a one-line summary of the interaction,\n'
        '  "type": the pharmacological type (e.g. pharmacokinetic, pharmacodynamic, additive, synergistic, antagonistic),\n'
        '  "severity": one of "high", "moderate", or "low",\n'
        '  "explanation": a 2-3 sentence explanation using VERY SIMPLE language. '
        'Avoid all medical jargon and technical terms. Explain concepts like a doctor would to a patient with no medical background. '
        'Use everyday words and short sentences.\n'
        "Return ONLY the JSON object, no markdown, no extra text."
    )
    user_prompt = (
        f"Drug A: {drug_a}\nDrug B: {drug_b}\n"
        f"Raw interaction text: {raw_text}"
    )
    raw = _call_llm(system_prompt, user_prompt)
    return _parse_json_response(raw, drug_a, drug_b)


# ── 3. Generate interaction when NOT found in database ──────────────────────

def generate_explanation(drug_a: str, drug_b: str) -> Dict[str, Any]:
    """
    When no database entry exists, ask the LLM to generate a plausible
    interaction explanation (clearly marked as AI-generated).
    """
    system_prompt = (
        "You are a clinical pharmacology expert explaining drug interactions to patients. "
        "The user asks about a potential drug-drug interaction that is NOT in our verified database. "
        "Based on your pharmacological knowledge, provide your best assessment. "
        "Return a JSON object with EXACTLY these keys:\n"
        '  "interaction": a one-line summary,\n'
        '  "type": pharmacological type,\n'
        '  "severity": one of "high", "moderate", or "low",\n'
        '  "explanation": a 2-3 sentence explanation using VERY SIMPLE language. '
        'Avoid all medical jargon and technical terms. Explain concepts like a doctor would to a patient with no medical background. '
        'Use everyday words and short sentences.\n'
        "Return ONLY the JSON object, no markdown, no extra text."
    )
    user_prompt = f"What is the potential interaction between {drug_a} and {drug_b}?"
    raw = _call_llm(system_prompt, user_prompt)
    return _parse_json_response(raw, drug_a, drug_b)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _parse_json_response(raw: str, drug_a: str, drug_b: str) -> Dict[str, Any]:
    """Parse the LLM JSON response with graceful fallback."""
    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
            cleaned = cleaned.rsplit("```", 1)[0].strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()

        data = json.loads(cleaned)
        if isinstance(data, dict):
            return {
                "interaction": data.get("interaction", "Unknown interaction"),
                "type": data.get("type", "unknown"),
                "severity": data.get("severity", "moderate"),
                "explanation": data.get("explanation", "No explanation available."),
            }
    except json.JSONDecodeError:
        logger.warning(f"Could not parse LLM JSON for ({drug_a}, {drug_b}): {raw[:200]}")

    # Fallback
    return {
        "interaction": f"Potential interaction between {drug_a} and {drug_b}",
        "type": "unknown",
        "severity": "moderate",
        "explanation": raw[:500] if raw else "Could not generate explanation.",
    }
