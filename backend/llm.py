"""
LLM module – all OpenRouter API calls live here.
Uses the OpenAI-compatible client pointed at OpenRouter.
Falls back to demo mode if API key is not configured.
"""

import os
import json
import logging
import re
from typing import List, Dict, Any
from openai import OpenAI, AuthenticationError
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

# Initialize client only if API key is provided
client = None
has_valid_api_key = False

if OPENROUTER_API_KEY and OPENROUTER_API_KEY != "":
    try:
        client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )
        has_valid_api_key = True
        logger.info("OpenRouter API key loaded. LLM mode: ENABLED")
    except Exception as e:
        logger.warning(f"Failed to initialize OpenRouter client: {e}")
        logger.info("Running in demo mode - database lookups only")
else:
    logger.warning("No OPENROUTER_API_KEY found in environment variables")
    logger.info("Running in demo mode - database lookups only")


def _call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
    """Low-level helper that calls OpenRouter and returns the assistant message."""
    if not has_valid_api_key or client is None:
        raise Exception(
            "LLM API not configured. Please set OPENROUTER_API_KEY environment variable. "
            "Get a free key at https://openrouter.ai"
        )
    
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
    except AuthenticationError as e:
        logger.error(f"Authentication failed: {e}")
        raise Exception("Invalid OpenRouter API key. Please check your credentials.")
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise


# ── 1. Extract drug names from free text ────────────────────────────────────

def extract_drugs(text: str) -> List[str]:
    """
    Use LLM to extract drug/medication names from text.
    Falls back to simple pattern matching if LLM is not available.
    """
    if has_valid_api_key and client:
        try:
            system_prompt = (
                "You are a pharmacology expert. Extract ALL drug and medication names "
                "from the user's text. Return ONLY a valid JSON array of strings, "
                "nothing else. Example: [\"Aspirin\", \"Metformin\"]"
            )
            raw = _call_llm(system_prompt, text)
            
            # Try to parse JSON array from the response
            try:
                cleaned = raw.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
                    cleaned = cleaned.rsplit("```", 1)[0].strip()
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:].strip()
                
                drugs = json.loads(cleaned)
                if isinstance(drugs, list):
                    result = [str(d).strip() for d in drugs if str(d).strip()]
                    logger.info(f"LLM extracted {len(result)} drugs: {result}")
                    return result
            except json.JSONDecodeError:
                logger.warning(f"Could not parse LLM drug extraction output: {raw}")
                # Fall through to pattern matching
        except Exception as e:
            logger.warning(f"LLM extraction failed: {e}. Using pattern matching.")
    
    # Demo mode: simple pattern matching
    logger.info("Using pattern matching for drug extraction (demo mode)")
    # Split by common delimiters and filter
    candidates = re.split(r'[,;]|\s+and\s+|\s+or\s+', text)
    drugs = [c.strip() for c in candidates if c.strip() and len(c.strip()) > 2]
    logger.info(f"Pattern matching extracted {len(drugs)} candidates: {drugs}")
    return drugs[:10]  # Limit to 10


def _parse_json_response(raw: str, drug_a: str, drug_b: str) -> Dict[str, Any]:
    """Helper to parse JSON response from LLM."""
    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
            cleaned = cleaned.rsplit("```", 1)[0].strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
        result = json.loads(cleaned)
        if isinstance(result, dict):
            return result
    except json.JSONDecodeError:
        logger.warning(f"Could not parse LLM JSON response: {raw}")
    
    # Default fallback
    return {
        "interaction": f"Potential interaction between {drug_a} and {drug_b}",
        "type": "unknown",
        "severity": "unknown",
        "explanation": "Unable to generate detailed explanation at this time.",
    }


# ── 2. Simplify a raw interaction description ───────────────────────────────

def simplify_interaction(drug_a: str, drug_b: str, raw_text: str) -> Dict[str, Any]:
    """
    Given a raw interaction description from the database, use LLM to produce
    a structured, simplified explanation. Falls back to demo response if LLM unavailable.
    """
    if not has_valid_api_key or not client:
        logger.info(f"Simplifying interaction in demo mode: {drug_a} × {drug_b}")
        return {
            "interaction": f"Potential interaction between {drug_a} and {drug_b}",
            "type": "pharmacokinetic",
            "severity": "moderate",
            "explanation": f"These medications may interact. Consult your healthcare provider about using {drug_a} and {drug_b} together.",
            "disclaimer": "This is a demonstration response. Please verify with your healthcare provider.",
        }
    
    try:
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
    except Exception as e:
        logger.warning(f"LLM simplification failed: {e}. Using default response.")
        return {
            "interaction": f"Potential interaction between {drug_a} and {drug_b}",
            "type": "unknown",
            "severity": "moderate",
            "explanation": f"These medications may interact. Please consult your healthcare provider.",
        }


# ── 3. Generate interaction when NOT found in database ──────────────────────

def generate_explanation(drug_a: str, drug_b: str) -> Dict[str, Any]:
    """
    When no database entry exists, ask the LLM to generate a plausible
    interaction explanation (clearly marked as AI-generated).
    Falls back to demo response if LLM is unavailable.
    """
    if not has_valid_api_key or not client:
        logger.info(f"Generating explanation in demo mode: {drug_a} × {drug_b}")
        return {
            "interaction": f"Potential interaction between {drug_a} and {drug_b}",
            "type": "pharmacodynamic",
            "severity": "moderate",
            "explanation": f"These medications may affect each other. Talk to your doctor or pharmacist before combining them.",
            "disclaimer": "This is an AI-generated assessment. Always consult a healthcare professional.",
        }
    
    try:
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
    except Exception as e:
        logger.warning(f"LLM generation failed: {e}. Using default response.")
        return {
            "interaction": f"Potential interaction between {drug_a} and {drug_b}",
            "type": "unknown",
            "severity": "moderate",
            "explanation": "Please consult your healthcare provider about potential interactions.",
        }


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
