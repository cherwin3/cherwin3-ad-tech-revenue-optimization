from models import ScrollData


def optimize_placement(data: ScrollData):

    scroll = data.scroll_depth
    time = data.time_on_page

    if scroll < 20:
        position = "top_content"
        ad_format = "display"
        viewability = 0.62
        reason = "User is near the top of the page."

    elif scroll < 50:
        position = "upper_middle_content"
        ad_format = "native"
        viewability = 0.76
        reason = "User has moderate engagement."

    elif scroll < 80:
        position = "middle_content"
        ad_format = "native"
        viewability = 0.87
        reason = "User has high engagement."

    else:
        position = "bottom_content"
        ad_format = "display"
        viewability = 0.73
        reason = "User is near the bottom of the page."

    if time >= 60:
        viewability += 0.08

    elif time >= 30:
        viewability += 0.05

    elif time < 5:
        viewability -= 0.08

    if data.device_type == "mobile":
        viewability += 0.02

    viewability = min(
        max(viewability, 0),
        1
    )

    estimated_rpm = round(
        2 + viewability * 4,
        2
    )

    return {
        "user_id": data.user_id,
        "page_id": data.page_id,
        "recommended_position": position,
        "ad_format": ad_format,
        "predicted_viewability": round(viewability, 2),
        "estimated_rpm": estimated_rpm,
        "reason": reason
    }