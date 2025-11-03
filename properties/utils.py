from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger('properties')

def get_all_properties():
    """
    Fetch all properties with low-level caching.
    
    This function implements a caching strategy:
    1. First, check if data exists in Redis cache
    2. If found (cache hit), return it immediately - FAST!
    3. If not found (cache miss), query the database - slower
    4. Store the result in cache for next time
    5. Return the data
    
    This cache lasts for 1 hour (3600 seconds).
    """
    cache_key = 'all_properties'
    
    # Try to get data from cache first
    cached_properties = cache.get(cache_key)
    
    if cached_properties is not None:
        logger.info("Cache HIT: Retrieved properties from Redis cache")
        return cached_properties
    
    # Cache miss - fetch from database
    logger.info("Cache MISS: Fetching properties from database")
    properties = list(Property.objects.all())
    
    # Store in cache for 1 hour (3600 seconds)
    cache.set(cache_key, properties, 3600)
    logger.info(f"Cached {len(properties)} properties for 1 hour")
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache performance metrics.
    
    This function helps you understand how well your cache is working:
    - Hit Ratio: Percentage of requests served from cache
    - High hit ratio (>80%) = Great caching!
    - Low hit ratio (<50%) = Cache isn't helping much
    
    Returns:
        dict: Dictionary containing hits, misses, and hit ratio
    """
    try:
        # Connect to Redis
        redis_client = get_redis_connection('default')
        
        # Get cache statistics from Redis
        info = redis_client.info('stats')
        
        # Extract metrics
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_requests = hits + misses
        
        # Calculate hit ratio (what percentage of requests used cache)
        hit_ratio = (hits / total_requests * 100) if total_requests > 0 else 0
        
        metrics = {
            'keyspace_hits': hits,
            'keyspace_misses': misses,
            'total_requests': total_requests,
            'hit_ratio_percentage': round(hit_ratio, 2)
        }
        
        # Log the metrics
        logger.info(f"Cache Metrics - Hits: {hits}, Misses: {misses}, "
                   f"Hit Ratio: {hit_ratio:.2f}%")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving cache metrics: {e}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio_percentage': 0
        }