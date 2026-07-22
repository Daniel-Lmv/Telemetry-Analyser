from domain.session import Session
from domain.telemetry import Telemetry
from mapper.telemetry_mapper import TelemetryMapper
from transform.synchronizer import Synchronizer
from transform.telemetry_builder import TelemetryBuilder


class TelemetryPipeline:
    def __init__(
        self,
        mapper: TelemetryMapper,
        synchronizer: Synchronizer,
        builder: TelemetryBuilder,
    ):

        self._mapper: TelemetryMapper = mapper
        self._synchronizer: Synchronizer = synchronizer
        self._builder: TelemetryBuilder = builder

    def run(self, session: Session) -> Telemetry:
        mapped_session = self._mapper.map(session)
        synchronized_session = self._synchronizer.synchronize(mapped_session)
        telemetry = self._builder.build(synchronized_session)
        return telemetry
