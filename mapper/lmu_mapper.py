from typing import Any

from pandas import DataFrame

from domain.mapped_session import MappedSession
from domain.session import ChannelInfo, Session
from domain.signal import Signal
from domain.telemetry_feature import TelemetryFeature
from mapper.lmu_feature_map import LMU_FEATURE_MAP


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

            signals[feature] = self._create_signal(
                feature=feature,
                channel_info=info,
                data=channel_data[channel_name],
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
