import hashlib
import json
import os
from typing import Any, Dict, Optional

import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CACHE_EXPIRY = int(os.getenv("CACHE_EXPIRY", "300"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2
)


def create_cache_key(data: Dict[str, Any]) -> str:
    serialized_data = json.dumps(data, sort_keys=True)
    key_hash = hashlib.sha256(serialized_data.encode()).hexdigest()

    return f"adstream:recommendation:{key_hash}"


def get_cached_result(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        cache_key = create_cache_key(data)
        cached_value = redis_client.get(cache_key)

        if cached_value:
            return json.loads(cached_value)

        return None

    except redis.RedisError as error:
        print(f"Redis read error: {error}")
        return None


def save_cached_result(
    request_data: Dict[str, Any],
    result: Dict[str, Any]
) -> bool:
    try:
        cache_key = create_cache_key(request_data)

        redis_client.setex(
            cache_key,
            CACHE_EXPIRY,
            json.dumps(result)
        )

        return True

    except redis.RedisError as error:
        print(f"Redis write error: {error}")
        return False


def check_redis_connection() -> bool:
    try:
        return bool(redis_client.ping())
    except redis.RedisError:
        return False