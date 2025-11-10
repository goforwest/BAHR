"""
Redis caching utilities for the BAHR API.
"""

import json
import hashlib
from typing import Optional, Any
from redis.asyncio import Redis, from_url
from app.config import settings
import logging

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
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True
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
            return json.loads(value)
        logger.debug(f"Cache miss for key: {key}")
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
        serialized = json.dumps(value, ensure_ascii=False)
        await redis.setex(key, ttl, serialized)
        logger.debug(f"Cached key: {key} with TTL: {ttl}s")
        return True
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


def generate_cache_key(text: str) -> str:
    """
    Generate cache key from text using SHA256 hash.
    
    Args:
        text: Normalized text to hash
        
    Returns:
        Cache key string
        
    Example:
        >>> key = generate_cache_key("إذا غامرت في شرف مروم")
        >>> key
        'analysis:abc123...'
    """
    text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return f"analysis:{text_hash}"
