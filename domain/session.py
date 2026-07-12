from dataclasses import dataclass
from typing import Any

from pandas import DataFrame


@dataclass(slots=True)
class ChannelInfo:
    frequency: int
    unit: str


@dataclass(slots=True)
class EventInfo:
    unit: str


@dataclass(slots=True)
class Session:
    metadata: dict[str, Any]
    channel_info: dict[str, ChannelInfo]
    channel_data: dict[str, DataFrame]
    event_info: dict[str, EventInfo]
    event_data: dict[str, DataFrame]
