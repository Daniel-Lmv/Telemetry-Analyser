from abc import ABC, abstractmethod

from domain.session import Session


class TelemetryReader(ABC):
    """Interface for telemetry readers"""

    @abstractmethod
    def load(self) -> Session:
        """Read one session and returns an object Session"""
        pass
