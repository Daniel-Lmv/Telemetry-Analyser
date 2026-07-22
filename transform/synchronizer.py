from pandas import DataFrame, Index

from domain.mapped_session import MappedSession
from domain.signal import Signal
from domain.telemetry_feature import TelemetryFeature


class Synchronizer:
    def synchronize(self, session: MappedSession) -> MappedSession:
        reference_signal = self._reference_signal(session.signals)

        synchronized_signals: dict[TelemetryFeature, Signal] = {}

        for feature, signal in session.signals.items():
            synchronized_signals[feature] = self._synchronize_signal(
                reference_signal, signal
            )

        return MappedSession(metadata=session.metadata, signals=synchronized_signals)

    def _reference_signal(self, signals: dict[TelemetryFeature, Signal]) -> Signal:
        reference_signal = signals.get(TelemetryFeature.SESSION_TIME)
        if reference_signal is None:
            raise ValueError("MappedSession must contain the SESSION_TIME signal!")
        return reference_signal

    def _synchronize_signal(self, reference_signal: Signal, signal: Signal) -> Signal:
        if reference_signal.frequency == signal.frequency:
            return signal
        data = signal.data.copy()
        data = self._reindex_signal(data, reference_signal.data.index)
        data = self._foward_fill(data)
        return self._create_synchronized_signal(
            signal, reference_signal.frequency, data
        )

    def _reindex_signal(self, data: DataFrame, reference_index: Index) -> DataFrame:
        positions = data.index.get_indexer(reference_index, method="pad")
        df = data.iloc[positions].copy()
        df.index = reference_index
        return df

    def _foward_fill(self, data: DataFrame) -> DataFrame:
        return data.ffill()

    def _create_synchronized_signal(
        self, original_signal: Signal, reference_frequency: int, data: DataFrame
    ) -> Signal:
        return Signal(
            feature=original_signal.feature,
            frequency=reference_frequency,
            unit=original_signal.unit,
            data=data,
        )
