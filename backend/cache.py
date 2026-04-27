"""
In-memory cache for drug interaction results.
Uses frozenset of drug pairs as keys so (A,B) == (B,A).
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

_cache: Dict[frozenset, Dict[str, Any]] = {}


def get_cache_key(drug_a: str, drug_b: str) -> frozenset:
    """Create an order-independent cache key from two drug names."""
    return frozenset([drug_a.lower(), drug_b.lower()])


def get_from_cache(drug_a: str, drug_b: str) -> Optional[Dict[str, Any]]:
    """Retrieve a cached interaction result, or None if not cached."""
    key = get_cache_key(drug_a, drug_b)
    result = _cache.get(key)
    if result:
        logger.info(f"Cache HIT for ({drug_a}, {drug_b})")
    else:
        logger.debug(f"Cache MISS for ({drug_a}, {drug_b})")
    return result


def set_cache(drug_a: str, drug_b: str, value: Dict[str, Any]) -> None:
    """Store an interaction result in the cache."""
    key = get_cache_key(drug_a, drug_b)
    _cache[key] = value
    logger.info(f"Cached result for ({drug_a}, {drug_b})")


def clear_cache() -> None:
    """Clear the entire cache."""
    _cache.clear()
    logger.info("Cache cleared")
