from dataclasses import dataclass
from typing import Any

from domain.telemetry import Telemetry


@dataclass(slots=True)
class TelemetrySession:
    metadata: dict[str, Any]
    telemetry: Telemetry
