from unittest.mock import MagicMock

from backend.app.consumer.kafka_consumer import (
    convert_timestamp,
    insert_event
)


def test_convert_timestamp():
    timestamp = "2026-08-19T15:00:00+00:00"

    result = convert_timestamp(timestamp)

    assert result.year == 2026
    assert result.month == 8
    assert result.day == 19


def test_insert_event():
    mock_client = MagicMock()

    event = {
        "user_id": "U101",
        "page_id": "P501",
        "recommended_position": "middle_content",
        "ad_format": "native",
        "predicted_viewability": 0.94,
        "estimated_rpm": 5.76,
        "source": "optimization_engine",
        "llm_used": True,
        "latency_ms": 100,
        "timestamp": "2026-08-19T15:00:00+00:00"
    }

    insert_event(mock_client, event)

    mock_client.execute.assert_called_once()