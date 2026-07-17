import numpy as np
from pandas import DataFrame, Index

from domain.mapped_session import MappedSession
from domain.signal import Signal
from domain.telemetry_feature import TelemetryFeature


class Synchronizer:
    def synchronize(self, session: MappedSession) -> MappedSession:
        reference_signal = self._reference_signal(session.signals)
        reference_index = self._create_time_index(reference_signal)

        synchronized_signals: dict[TelemetryFeature, Signal] = {}

        for feature, signal in session.signals.items():
            synchronized_signals[feature] = self._synchronize_signal(
                reference_signal, reference_index, signal
            )

        return MappedSession(metadata=session.metadata, signals=synchronized_signals)

    def _reference_signal(self, signals: dict[TelemetryFeature, Signal]) -> Signal:
        reference_signal = signals.get(TelemetryFeature.SESSION_TIME)
        if reference_signal is None:
            raise ValueError("MappedSession must contain the SESSION_TIME signal!")
        return reference_signal

    def _synchronize_signal(
        self, reference_signal: Signal, reference_index: Index, signal: Signal
    ) -> Signal:
        if reference_signal.frequency == signal.frequency:
            return signal
        signal_index = self._create_time_index(signal)
        data = signal.data.copy()
        data.index = signal_index
        data = self._reindex_signal(data, reference_index)
        data = self._foward_fill(data)
        return self._create_synchronized_signal(
            signal, reference_signal.frequency, data
        )

    def _create_time_index(self, signal: Signal) -> Index:
        sample_period = 1 / signal.frequency
        n_samples = len(signal.data.index)

        time_index = Index(np.arange(n_samples) * sample_period, name="time")
        return time_index

    def _reindex_signal(self, data: DataFrame, reference_index: Index) -> DataFrame:
        return data.reindex(reference_index)

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
