from typing import Any, Dict

from .models import ScrollData


def optimize_placement(data: ScrollData) -> Dict[str, Any]:
    if data.scroll_depth < 20:
        position = "top_content"
        ad_format = "display"
        viewability = 0.62

    elif data.scroll_depth < 50:
        position = "upper_middle"
        ad_format = "native"
        viewability = 0.76

    elif data.scroll_depth < 80:
        position = "middle_content"
        ad_format = "native"
        viewability = 0.87

    else:
        position = "bottom_content"
        ad_format = "display"
        viewability = 0.73

    if data.time_on_page >= 60:
        viewability += 0.08
    elif data.time_on_page >= 30:
        viewability += 0.05
    elif data.time_on_page < 5:
        viewability -= 0.08

    if data.device_type == "mobile":
        viewability += 0.02
    elif data.device_type == "tablet":
        viewability += 0.01

    viewability = max(0.0, min(viewability, 0.99))
    rpm = round(2.0 + viewability * 4.0, 2)

    return {
        "recommended_position": position,
        "ad_format": ad_format,
        "predicted_viewability": round(viewability, 2),
        "estimated_rpm": rpm,
        "reason": (
            f"{position} was selected based on a scroll depth of "
            f"{data.scroll_depth}% and {data.time_on_page} seconds of engagement."
        )
    }