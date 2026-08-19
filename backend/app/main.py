import time
from datetime import datetime, timezone

from fastapi import FastAPI

from .audit_logger import log_audit
from .kafka_producer import publish_ad_event
from .llm_service import generate_llm_reason
from .models import OptimizationResponse, ScrollData
from .optimizer import optimize_placement
from .redis_service import (
    check_redis_connection,
    get_cached_result,
    save_cached_result
)

app = FastAPI(
    title="AdStream Revenue Optimization API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AdStream Revenue Optimization API is running"
    }


@app.get("/health")
def health():
    return {
        "api": "healthy",
        "redis": (
            "connected"
            if check_redis_connection()
            else "disconnected"
        )
    }


@app.post(
    "/optimize-placement",
    response_model=OptimizationResponse
)
def optimize_ad_placement(data: ScrollData):
    start_time = time.perf_counter()
    request_data = data.model_dump()

    cached_result = get_cached_result(request_data)

    # ----------------------------
    # REDIS CACHE HIT
    # ----------------------------
    if cached_result:
        latency_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

        cached_result["source"] = "redis_cache"
        cached_result["latency_ms"] = latency_ms

        event = {
            **cached_result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        publish_ad_event(event)

        # Audit log
        log_audit(
            user_id=data.user_id,
            action="OPTIMIZE_PLACEMENT_CACHE_HIT",
            status="SUCCESS",
            latency_ms=latency_ms
        )

        return cached_result

    # ----------------------------
    # OPTIMIZATION ENGINE
    # ----------------------------
    result = optimize_placement(data)

    llm_reason = generate_llm_reason(
        position=result["recommended_position"],
        ad_format=result["ad_format"],
        scroll_depth=data.scroll_depth,
        time_on_page=data.time_on_page,
        viewability=result["predicted_viewability"]
    )

    llm_used = llm_reason is not None

    if llm_reason:
        result["reason"] = llm_reason

    latency_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2
    )

    response = {
        "user_id": data.user_id,
        "page_id": data.page_id,
        **result,
        "source": "optimization_engine",
        "llm_used": llm_used,
        "latency_ms": latency_ms
    }

    save_cached_result(request_data, response)

    event = {
        **response,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    publish_ad_event(event)

    # Audit log
    log_audit(
        user_id=data.user_id,
        action="OPTIMIZE_PLACEMENT",
        status="SUCCESS",
        latency_ms=latency_ms
    )

    return response