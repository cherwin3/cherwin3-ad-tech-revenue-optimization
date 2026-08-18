import redis
import json
import hashlib


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


def test_redis():

    try:
        redis_client.ping()
        return True

    except redis.ConnectionError:
        return False


def generate_cache_key(data):

    raw_key = (
        f"{data.page_id}:"
        f"{data.scroll_depth}:"
        f"{data.time_on_page}:"
        f"{data.device_type}:"
        f"{data.page_type}"
    )

    hashed_key = hashlib.sha256(
        raw_key.encode()
    ).hexdigest()

    return f"adplacement:{hashed_key}"


def get_cached_result(key):

    try:
        result = redis_client.get(key)

        if result:
            return json.loads(result)

    except redis.ConnectionError:
        pass

    return None


def save_to_cache(
    key,
    result,
    expiry=300
):

    try:
        redis_client.setex(
            key,
            expiry,
            json.dumps(result)
        )

    except redis.ConnectionError:
        pass