from fastapi import FastAPI

from models import ScrollData
from optimizer import optimize_placement

from redis_service import (
    generate_cache_key,
    get_cached_result,
    save_to_cache,
    test_redis
)

from llm_service import generate_llm_reason


app = FastAPI(
    title="AdStream Revenue Optimization API",
    description=(
        "Ad placement optimization using scroll behavior, "
        "Redis caching and Gemini LLM."
    ),
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "project": "AdStream Revenue Optimization",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health():

    return {
        "api": "healthy",
        "redis": (
            "connected"
            if test_redis()
            else "not_connected"
        )
    }


@app.post("/optimize-placement")
def optimize_ad(data: ScrollData):

    # Create cache key
    cache_key = generate_cache_key(data)

    # Check Redis
    cached_result = get_cached_result(
        cache_key
    )

    if cached_result:

        cached_result["source"] = "redis_cache"

        return cached_result

    # Run optimization
    result = optimize_placement(data)

    # Run Gemini LLM
    llm_result = generate_llm_reason(
        data,
        result
    )

    result["reason"] = llm_result["reason"]

    result["llm_used"] = llm_result["llm_used"]

    result["source"] = "optimization_engine"

    # Save in Redis
    save_to_cache(
        cache_key,
        result
    )

    return result