from domain.session import Session
from domain.telemetry_session import TelemetrySession
from mapper.telemetry_mapper import TelemetryMapper
from transform.synchronizer import Synchronizer
from transform.telemetry_builder import TelemetryBuilder
from transform.telemetry_session_builder import TelemetrySessionBuilder


class TelemetryPipeline:
    def __init__(
        self,
        mapper: TelemetryMapper,
        synchronizer: Synchronizer,
        builder: TelemetryBuilder,
        telemetry_session_builder: TelemetrySessionBuilder,
    ):

        self._mapper: TelemetryMapper = mapper
        self._synchronizer: Synchronizer = synchronizer
        self._builder: TelemetryBuilder = builder
        self._telemetry_session_builder = telemetry_session_builder

    def run(self, session: Session) -> TelemetrySession:
        mapped_session = self._mapper.map(session)
        synchronized_session = self._synchronizer.synchronize(mapped_session)
        telemetry = self._builder.build(synchronized_session)
        telemetry_session = self._telemetry_session_builder.build(
            synchronized_session.metadata, telemetry
        )
        return telemetry_session
