from abc import ABC, abstractmethod

from domain.mapped_session import MappedSession
from domain.session import Session


class TelemetryMapper(ABC):
    """Interface for telemetry mappers"""

    @abstractmethod
    def map(self, session: Session) -> MappedSession:
        """Read one session and returns an object MappedSession"""
        pass
