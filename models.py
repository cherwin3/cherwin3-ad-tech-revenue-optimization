from typing import Literal
from pydantic import BaseModel, Field


class ScrollData(BaseModel):
    user_id: str = Field(min_length=1)
    page_id: str = Field(min_length=1)

    scroll_depth: float = Field(
        ge=0,
        le=100
    )

    time_on_page: float = Field(
        ge=0
    )

    device_type: Literal[
        "mobile",
        "desktop",
        "tablet"
    ]

    page_type: Literal[
        "news",
        "sports",
        "technology",
        "entertainment",
        "finance",
        "other"
    ] = "other"