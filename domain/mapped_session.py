from dataclasses import dataclass
from typing import Any

from domain.signal import Signal
from domain.telemetry_feature import TelemetryFeature


@dataclass
class MappedSession:
    metadata: dict[str, Any]
    signals: dict[TelemetryFeature, Signal]
