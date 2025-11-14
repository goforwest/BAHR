"""
Redis caching utilities for the BAHR API.
"""

import hashlib
import json
import logging
from typing import Any, Optional

from redis.asyncio import Redis, from_url

from app.config import settings

logger = logging.getLogger(__name__)

# Global Redis connection
_redis_client: Optional[Redis] = None


async def get_redis() -> Redis:
    """
    Get or create Redis connection.

    Returns:
        Redis client instance
    """
    global _redis_client
    if _redis_client is None:
        _redis_client = from_url(
            settings.redis_url, encoding="utf-8", decode_responses=True
        )
    return _redis_client


async def close_redis():
    """Close Redis connection."""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None


async def cache_get(key: str) -> Optional[Any]:
    """
    Get value from cache.

    Args:
        key: Cache key

    Returns:
        Cached value (deserialized from JSON) or None if not found

    Example:
        >>> result = await cache_get("analysis:abc123")
    """
    try:
        redis = await get_redis()
        value = await redis.get(key)
        if value:
            logger.debug(f"Cache hit for key: {key}")
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to deserialize cached value for key {key}: {e}")
                # Delete corrupted cache entry
                try:
                    await redis.delete(key)
                except Exception:
                    pass
                return None
        logger.debug(f"Cache miss for key: {key}")
        return None
    except ConnectionError as e:
        logger.error(f"Redis connection error for key {key}: {e}")
        return None
    except TimeoutError as e:
        logger.error(f"Redis timeout for key {key}: {e}")
        return None
    except Exception as e:
        logger.error(f"Redis get error for key {key}: {e}")
        return None


async def cache_set(key: str, value: Any, ttl: int = 86400) -> bool:
    """
    Set value in cache with TTL.

    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time to live in seconds (default: 24 hours)

    Returns:
        True if successful, False otherwise

    Example:
        >>> await cache_set("analysis:abc123", {"result": "..."}, ttl=3600)
    """
    try:
        redis = await get_redis()
        try:
            serialized = json.dumps(value, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            logger.error(f"Failed to serialize value for key {key}: {e}")
            return False

        # Edge case: Validate TTL
        if ttl <= 0:
            logger.warning(f"Invalid TTL {ttl} for key {key}, using default 86400")
            ttl = 86400

        await redis.setex(key, ttl, serialized)
        logger.debug(f"Cached key: {key} with TTL: {ttl}s")
        return True
    except ConnectionError as e:
        logger.error(f"Redis connection error for key {key}: {e}")
        return False
    except TimeoutError as e:
        logger.error(f"Redis timeout for key {key}: {e}")
        return False
    except Exception as e:
        logger.error(f"Redis set error for key {key}: {e}")
        return False


async def cache_delete(key: str) -> bool:
    """
    Delete value from cache.

    Args:
        key: Cache key

    Returns:
        True if successful, False otherwise

    Example:
        >>> await cache_delete("analysis:abc123")
    """
    try:
        redis = await get_redis()
        await redis.delete(key)
        logger.debug(f"Deleted cache key: {key}")
        return True
    except Exception as e:
        logger.error(f"Redis delete error for key {key}: {e}")
        return False


def generate_cache_key(
    text: str,
    detect_bahr: bool = True,
    suggest_corrections: bool = False,
    analyze_rhyme: bool = True,
) -> str:
    """
    Generate cache key from text and request parameters using SHA256 hash.

    Args:
        text: Normalized text to hash
        detect_bahr: Whether bahr detection was requested
        suggest_corrections: Whether corrections were requested
        analyze_rhyme: Whether rhyme analysis was requested

    Returns:
        Cache key string

    Example:
        >>> key = generate_cache_key("إذا غامرت في شرف مروم", detect_bahr=True)
        >>> key
        'analysis:abc123...'
    """
    # Include request parameters in cache key to avoid returning
    # cached results with different analysis options
    cache_data = f"{text}|{detect_bahr}|{suggest_corrections}|{analyze_rhyme}"
    text_hash = hashlib.sha256(cache_data.encode("utf-8")).hexdigest()
    return f"analysis:{text_hash}"
