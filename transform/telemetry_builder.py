from pandas import DataFrame, Series

from domain.mapped_session import MappedSession
from domain.signal import Signal
from domain.telemetry import Telemetry


class TelemetryBuilder:
    def build(self, session: MappedSession) -> Telemetry:
        dataframe = self._build_dataframe(session)
        return Telemetry(data=dataframe)

    def _build_dataframe(self, session: MappedSession) -> DataFrame:
        series_dict = {}

        for signal in session.signals.values():
            series_dict.update(self._extract_series(signal))

        return DataFrame(series_dict)

    def _extract_series(self, signal: Signal) -> dict[str, Series]:
        series = {}

        for column in signal.data.columns:
            if column == "value":
                name = signal.feature.name
            else:
                name = f"{signal.feature.name}_{column}"

            s = signal.data[column]
            s.name = name
            series[name] = s

        return series
