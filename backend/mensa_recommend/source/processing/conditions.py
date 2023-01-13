from abc import abstractmethod, ABC
from datetime import timedelta, datetime
from typing import Optional


class Condition(ABC):
    @abstractmethod
    def holds(self) -> bool:
        pass


class TimeCondition(Condition):
    def __init__(self, lifetime: timedelta):
        self._lifetime = lifetime.total_seconds()
        self._timestamp: Optional[datetime] = None

    def holds(self) -> bool:
        now = datetime.now()
        result = self._timestamp is not None and (now - self._timestamp) \
            .seconds < self._lifetime

        if not result:
            self._timestamp = now

        return result
