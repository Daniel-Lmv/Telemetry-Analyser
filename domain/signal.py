from dataclasses import dataclass

from pandas import DataFrame

from domain.telemetry_feature import TelemetryFeature


@dataclass(slots=True)
class Signal:
    feature: TelemetryFeature
    frequency: int
    unit: str
    data: DataFrame
