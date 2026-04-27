"""
Drug-Drug Interaction API – FastAPI entry point.
"""

import logging
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from llm import extract_drugs, simplify_interaction, generate_explanation
from utils import normalize_drugs, validate_drugs, generate_pairs, lookup_interaction
from cache import get_from_cache, set_cache

# ── Logging setup ───────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

# ── FastAPI app ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="Drug-Drug Interaction Analyzer",
    description="Analyze potential drug-drug interactions from free-text input.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request / Response schemas ──────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    text: str


class InteractionResult(BaseModel):
    pair: List[str]
    interaction: str
    type: str
    severity: str
    explanation: str
    confidence: str
    source: str
    disclaimer: Optional[str] = None


class AnalyzeResponse(BaseModel):
    detected_drugs: List[str]
    normalized_drugs: List[str]
    pairs: List[List[str]]
    results: List[InteractionResult]


# ── Severity ranking helper ─────────────────────────────────────────────────

SEVERITY_ORDER = {"high": 0, "moderate": 1, "low": 2, "unknown": 3}
CONFIDENCE_ORDER = {"high": 0, "low": 1}


def _rank_key(r: InteractionResult):
    """Sort by severity (high first), then by confidence (high first)."""
    return (
        SEVERITY_ORDER.get(r.severity.lower(), 3),
        CONFIDENCE_ORDER.get(r.confidence.lower(), 1),
    )


# ── Main endpoint ──────────────────────────────────────────────────────────

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    logger.info(f"Received analysis request: {text[:120]}...")

    try:
        # 1. Extract drug names via LLM
        raw_drugs = extract_drugs(text)
        logger.info(f"Extracted drugs: {raw_drugs}")

        if len(raw_drugs) < 2:
            raise HTTPException(
                status_code=422,
                detail=f"Could not detect at least 2 drugs. Detected: {raw_drugs}",
            )

        # 2. Normalize
        normalized = normalize_drugs(raw_drugs)
        logger.info(f"Normalized drugs: {normalized}")
    except Exception as e:
        error_str = str(e).lower()
        if "rate" in error_str or "429" in error_str:
            logger.error(f"Rate limit error: {e}")
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later or consider upgrading your API plan.")
        logger.error(f"Error in drug extraction/normalization: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

    # 3. Validate (deduplicate, ensure ≥ 2)
    try:
        validated = validate_drugs(normalized)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # 4. Generate pairs
    pairs = generate_pairs(validated)

    # 5. Process each pair
    results: List[InteractionResult] = []

    for drug_a, drug_b in pairs:
        # Check cache first
        cached = get_from_cache(drug_a, drug_b)
        if cached:
            results.append(InteractionResult(**cached))
            continue

        # Lookup in dataset
        db_text = lookup_interaction(drug_a, drug_b)

        if db_text:
            # FOUND in database → simplify via LLM
            llm_data = simplify_interaction(drug_a, drug_b, db_text)
            result_data = {
                "pair": [drug_a, drug_b],
                "interaction": llm_data["interaction"],
                "type": llm_data["type"],
                "severity": llm_data["severity"],
                "explanation": llm_data["explanation"],
                "confidence": "high",
                "source": "database",
            }
        else:
            # NOT FOUND → generate via LLM
            llm_data = generate_explanation(drug_a, drug_b)
            result_data = {
                "pair": [drug_a, drug_b],
                "interaction": llm_data["interaction"],
                "type": llm_data["type"],
                "severity": llm_data["severity"],
                "explanation": llm_data["explanation"],
                "confidence": "low",
                "source": "llm",
                "disclaimer": (
                    "This interaction was generated by an AI model and is NOT "
                    "from a verified database. Always consult a healthcare "
                    "professional before making medical decisions."
                ),
            }

        # Cache the result
        set_cache(drug_a, drug_b, result_data)
        results.append(InteractionResult(**result_data))

    # 6. Rank results: severity (high first) > confidence (high first)
    results.sort(key=_rank_key)

    return AnalyzeResponse(
        detected_drugs=raw_drugs,
        normalized_drugs=validated,
        pairs=[[a, b] for a, b in pairs],
        results=results,
    )


# ── Health check ────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok"}


# ── Run with uvicorn ────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=1001, reload=False)
