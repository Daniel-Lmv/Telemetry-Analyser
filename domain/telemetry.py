from dataclasses import dataclass

from pandas import DataFrame


@dataclass(slots=True)
class Telemetry:
    data: DataFrame
