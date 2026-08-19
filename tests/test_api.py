from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert "running" in response.json()["message"]


@patch(
    "backend.app.main.publish_ad_event",
    return_value=True
)
@patch(
    "backend.app.main.save_cached_result",
    return_value=True
)
@patch(
    "backend.app.main.get_cached_result",
    return_value=None
)
@patch(
    "backend.app.main.generate_llm_reason",
    return_value=None
)
def test_optimize_placement(
    mock_llm,
    mock_cache_get,
    mock_cache_save,
    mock_kafka
):
    request_data = {
        "user_id": "U101",
        "page_id": "P501",
        "scroll_depth": 65,
        "time_on_page": 45,
        "device_type": "mobile",
        "page_type": "technology"
    }

    response = client.post(
        "/optimize-placement",
        json=request_data
    )

    assert response.status_code == 200

    body = response.json()

    assert body["recommended_position"] == "middle_content"
    assert body["source"] == "optimization_engine"
    assert body["llm_used"] is False


def test_invalid_scroll_depth():
    request_data = {
        "user_id": "U101",
        "page_id": "P501",
        "scroll_depth": 120,
        "time_on_page": 45,
        "device_type": "mobile",
        "page_type": "technology"
    }

    response = client.post(
        "/optimize-placement",
        json=request_data
    )

    assert response.status_code == 422