
from unittest.mock import patch

from backend.app.redis_service import (
    create_cache_key,
    get_cached_result,
    save_cached_result
)


def test_create_cache_key():
    data = {
        "user_id": "U101",
        "page_id": "P501"
    }

    key = create_cache_key(data)

    assert key.startswith("adstream:recommendation:")


@patch("backend.app.redis_service.redis_client")
def test_save_cached_result(mock_redis):
    request_data = {
        "user_id": "U101"
    }

    result = {
        "recommended_position": "middle_content"
    }

    success = save_cached_result(
        request_data,
        result
    )

    assert success is True
    mock_redis.setex.assert_called_once()


@patch("backend.app.redis_service.redis_client")
def test_get_cached_result(mock_redis):
    mock_redis.get.return_value = (
        '{"recommended_position": "middle_content"}'
    )

    result = get_cached_result(
        {"user_id": "U101"}
    )

    assert result["recommended_position"] == "middle_content"
