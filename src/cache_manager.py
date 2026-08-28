from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache


# ============================================================
# IN-MEMORY CACHE
# ============================================================

def enable_in_memory_cache():
    """
    Enable RAM-based LangChain cache.

    The cache exists only while the application is running.

    Advantages:
    - Fast
    - No persistent database file
    - Automatically disappears when the application restarts

    Security:
    - No SQLite database is created
    - No cache file is written to disk
    """

    cache = InMemoryCache()

    set_llm_cache(cache)

    return "InMemoryCache"


# ============================================================
# DISABLE CACHE
# ============================================================

def disable_cache():
    """
    Disable LangChain LLM caching.

    This is the safest option for a public medical application
    because requests and responses are not intentionally stored
    in a persistent cache.
    """

    set_llm_cache(None)

    return "Cache disabled"


# ============================================================
# CONFIGURE CACHE
# ============================================================

def configure_cache(cache_type: str):
    """
    Configure the application's cache.

    Supported modes:
        - Disabled
        - InMemoryCache

    SQLiteCache is intentionally not supported in the public
    deployment version.
    """

    if cache_type == "InMemoryCache":
        return enable_in_memory_cache()

    # Anything else, including the old SQLiteCache option,
    # falls back to the safest configuration.
    return disable_cache()