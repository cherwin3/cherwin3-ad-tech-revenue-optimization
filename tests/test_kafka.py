from unittest.mock import MagicMock, patch

from backend.app.kafka_producer import publish_ad_event


@patch("backend.app.kafka_producer.get_producer")
def test_publish_ad_event(mock_get_producer):
    mock_producer = MagicMock()
    mock_future = MagicMock()
    mock_metadata = MagicMock()

    mock_metadata.topic = "ad-events"
    mock_metadata.partition = 0
    mock_metadata.offset = 1

    mock_future.get.return_value = mock_metadata
    mock_producer.send.return_value = mock_future
    mock_get_producer.return_value = mock_producer

    event = {
        "user_id": "U101",
        "page_id": "P501",
        "recommended_position": "middle_content"
    }

    result = publish_ad_event(event)

    assert result is True

    mock_producer.send.assert_called_once_with(
        "ad-events",
        value=event
    )