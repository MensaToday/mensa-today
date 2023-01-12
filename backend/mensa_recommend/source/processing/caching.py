from abc import abstractmethod, ABC
from datetime import timedelta, datetime
from typing import Callable, TypeVar, Generic, Optional

T = TypeVar('T')


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
        result = self._timestamp is not None and \
                 (now - self._timestamp).seconds < self._lifetime

        if not result:
            self._timestamp = now

        return result


class Cache(Generic[T]):
    def __init__(self, update_condition: Condition, getter: Callable[[], T]):
        self._update_condition = update_condition
        self._getter = getter
        self._value: T = None

    def __check_value(self) -> None:
        if not self._update_condition.holds():
            self._value = self._getter()

    def get(self) -> T:
        self.__check_value()
        return self._value
