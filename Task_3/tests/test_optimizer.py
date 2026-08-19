from backend.app.models import ScrollData
from backend.app.optimizer import optimize_placement


def test_low_scroll_depth():
    data = ScrollData(
        user_id="U101",
        page_id="P101",
        scroll_depth=10,
        time_on_page=10,
        device_type="desktop",
        page_type="news"
    )

    result = optimize_placement(data)

    assert result["recommended_position"] == "top_content"
    assert result["ad_format"] == "display"


def test_middle_scroll_depth():
    data = ScrollData(
        user_id="U102",
        page_id="P102",
        scroll_depth=60,
        time_on_page=45,
        device_type="mobile",
        page_type="technology"
    )

    result = optimize_placement(data)

    assert result["recommended_position"] == "middle_content"
    assert result["ad_format"] == "native"
    assert result["predicted_viewability"] > 0.80


def test_high_scroll_depth():
    data = ScrollData(
        user_id="U103",
        page_id="P103",
        scroll_depth=90,
        time_on_page=20,
        device_type="desktop",
        page_type="sports"
    )

    result = optimize_placement(data)

    assert result["recommended_position"] == "bottom_content"