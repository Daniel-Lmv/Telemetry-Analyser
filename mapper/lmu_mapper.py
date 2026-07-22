from typing import Any

import numpy as np
from pandas import DataFrame, Index

from domain.mapped_session import MappedSession
from domain.session import ChannelInfo, Session
from domain.signal import Signal
from domain.telemetry_feature import TelemetryFeature
from mapper.lmu_feature_map import LMU_FEATURE_MAP

LMU_WHEEL_COLUMNS = {
    "value1": "FL",
    "value2": "FR",
    "value3": "RL",
    "value4": "RR",
}


class LMUMapper:
    def map(self, session: Session) -> MappedSession:
        metadata = self._map_metadata(session.metadata)
        signals = self._map_signals(session.channel_info, session.channel_data)
        return MappedSession(
            metadata=metadata,
            signals=signals,
        )

    def _map_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:
        return metadata

    def _map_signals(
        self, channel_info: dict[str, ChannelInfo], channel_data: dict[str, DataFrame]
    ) -> dict[TelemetryFeature, Signal]:
        signals: dict[TelemetryFeature, Signal] = {}

        for channel_name, info in channel_info.items():
            feature = LMU_FEATURE_MAP.get(channel_name)
            if feature is None:
                continue

            data = self._normalize_dataframe(channel_data[channel_name])
            data = self._index_dataframe(data, info.frequency)

            signals[feature] = self._create_signal(
                feature=feature,
                channel_info=info,
                data=data,
            )
        return signals

    def _create_signal(
        self, feature: TelemetryFeature, channel_info: ChannelInfo, data: DataFrame
    ) -> Signal:
        return Signal(
            feature=feature,
            frequency=channel_info.frequency,
            unit=channel_info.unit,
            data=data,
        )

    def _normalize_dataframe(self, data: DataFrame) -> DataFrame:
        df = data.copy()

        if all(column in df.columns for column in LMU_WHEEL_COLUMNS):
            df = df.rename(columns=LMU_WHEEL_COLUMNS)

        return df

    def _index_dataframe(self, data: DataFrame, frequency: int) -> DataFrame:
        df = data.copy()

        sample_period = 1 / frequency
        n_samples = len(df.index)

        time_index = Index(np.arange(n_samples) * sample_period, name="time")
        df.index = time_index
        return df
