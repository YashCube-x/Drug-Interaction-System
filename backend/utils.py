"""
Utility functions for drug name normalization, validation, and pair generation.
"""

import os
import logging
import csv
from itertools import combinations
from typing import List, Tuple, Optional

# import pandas as pd
from rapidfuzz import process, fuzz

logger = logging.getLogger(__name__)

# ── Load dataset and build drug name index ──────────────────────────────────

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "interactions.csv")

_interactions: List[Tuple[str, str, str]] = []
_all_drug_names: List[str] = []

# Common synonym mapping (extend as needed)
SYNONYM_MAP = {
    "tylenol": "acetaminophen",
    "advil": "ibuprofen",
    "motrin": "ibuprofen",
    "aleve": "naproxen",
    "lipitor": "atorvastatin",
    "zocor": "simvastatin",
    "glucophage": "metformin",
    "prilosec": "omeprazole",
    "nexium": "esomeprazole",
    "zantac": "ranitidine",
    "plavix": "clopidogrel",
    "coumadin": "warfarin",
    "xanax": "alprazolam",
    "valium": "diazepam",
    "ambien": "zolpidem",
    "prozac": "fluoxetine",
    "zoloft": "sertraline",
    "lexapro": "escitalopram",
    "synthroid": "levothyroxine",
    "norvasc": "amlodipine",
    "lasix": "furosemide",
    "viagra": "sildenafil",
    "cialis": "tadalafil",
}


def _load_data() -> List[Tuple[str, str, str]]:
    """Load the interactions CSV lazily and build drug name index."""
    global _interactions, _all_drug_names
    if not _interactions:
        logger.info(f"Loading interaction dataset from {DATA_PATH}")
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            _interactions = [(row[0].strip(), row[1].strip(), row[2].strip()) for row in reader]

        # Build set of all known drug names (lowered for matching)
        all_names = set()
        for drug1, drug2, _ in _interactions:
            all_names.add(drug1.lower())
            all_names.add(drug2.lower())
        _all_drug_names = sorted(all_names)
        logger.info(f"Loaded {len(_interactions)} interactions, {len(_all_drug_names)} unique drugs")
    return _interactions


def get_all_drug_names() -> List[str]:
    """Return sorted list of all drug names in the dataset (lowercase)."""
    _load_data()
    return _all_drug_names


# ── Normalization ───────────────────────────────────────────────────────────

def normalize_drug_name(name: str) -> str:
    """
    Normalize a drug name:
    1. Lowercase + strip
    2. Synonym mapping
    3. Fuzzy match against dataset drug names
    """
    name = name.strip().lower()

    # Synonym lookup
    if name in SYNONYM_MAP:
        mapped = SYNONYM_MAP[name]
        logger.info(f"Synonym mapped: {name} → {mapped}")
        return mapped

    # Check exact match in dataset
    all_names = get_all_drug_names()
    if name in all_names:
        return name

    # Fuzzy match (threshold 80)
    result = process.extractOne(name, all_names, scorer=fuzz.ratio, score_cutoff=80)
    if result:
        matched_name, score, _ = result
        logger.info(f"Fuzzy matched: {name} → {matched_name} (score={score})")
        return matched_name

    # No match found – return as-is (title-cased for display)
    logger.warning(f"No fuzzy match for: {name}")
    return name


def normalize_drugs(drugs: List[str]) -> List[str]:
    """Normalize a list of drug names."""
    return [normalize_drug_name(d) for d in drugs]


# ── Validation ──────────────────────────────────────────────────────────────

def deduplicate(drugs: List[str]) -> List[str]:
    """Remove duplicate drug names (case-insensitive, preserve order)."""
    seen = set()
    result = []
    for d in drugs:
        key = d.lower()
        if key not in seen:
            seen.add(key)
            result.append(d)
    return result


def validate_drugs(drugs: List[str]) -> List[str]:
    """Deduplicate and validate that at least 2 drugs remain."""
    unique = deduplicate(drugs)
    if len(unique) < 2:
        raise ValueError(
            f"At least 2 unique drugs are required, but only found: {unique}"
        )
    return unique


# ── Pair generation ─────────────────────────────────────────────────────────

def generate_pairs(drugs: List[str]) -> List[Tuple[str, str]]:
    """Generate all unique pairs (nC2) from a list of drug names."""
    pairs = list(combinations(drugs, 2))
    logger.info(f"Generated {len(pairs)} pairs from {len(drugs)} drugs")
    return pairs


# ── Dataset lookup ──────────────────────────────────────────────────────────

def lookup_interaction(drug_a: str, drug_b: str) -> Optional[str]:
    """
    Look up a drug pair in the CSV dataset.
    Returns the interaction description if found, else None.
    Checks both (A,B) and (B,A) orderings.
    """
    interactions = _load_data()
    a_low = drug_a.lower()
    b_low = drug_b.lower()

    for d1, d2, desc in interactions:
        if (d1.lower() == a_low and d2.lower() == b_low) or (d1.lower() == b_low and d2.lower() == a_low):
            logger.info(f"DB HIT for ({drug_a}, {drug_b})")
            return desc

    logger.info(f"DB MISS for ({drug_a}, {drug_b})")
    return None
