from domain.mapped_session import MappedSession
from domain.signal import Signal


class Synchronizer:
    def __init__(self, target_frequency: int = 100):
        self.target_frequency = target_frequency

    def synchronize(self, session: MappedSession) -> MappedSession:
        return session

    def _reference_signal(self):
        pass

    def _synchronize_signal(self):
        pass

    def _foward_fill(self, signal: Signal) -> Signal:
        return signal
