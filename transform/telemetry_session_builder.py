from typing import Any

from domain.telemetry import Telemetry
from domain.telemetry_session import TelemetrySession


class TelemetrySessionBuilder:
    def build(self, metadata: dict[str, Any], telemetry: Telemetry) -> TelemetrySession:
        return TelemetrySession(metadata=metadata, telemetry=telemetry)
