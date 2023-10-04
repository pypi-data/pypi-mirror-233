import dataclasses
from enum import Enum
from typing import List, Mapping, Optional, Set

from classiq.interface.model.handle_binding import HandleBinding

from classiq.exceptions import ClassiqError


class HandleState(Enum):
    INITIALIZED = 0
    UNINITIALIZED = 1
    ERRORED = 2


@dataclasses.dataclass
class Handle:
    errors: List[str] = dataclasses.field(default_factory=list)
    _wire_name: Optional[str] = None

    def __init__(
        self, wire_name: Optional[str] = None, errors: Optional[List[str]] = None
    ) -> None:
        self._wire_name = wire_name
        self.errors = errors or []

    @property
    def state(self) -> HandleState:
        if self.errors:
            return HandleState.ERRORED
        elif self._wire_name is not None:
            return HandleState.INITIALIZED
        else:
            return HandleState.UNINITIALIZED

    def initialize(self, wire_name: str) -> None:
        self._wire_name = wire_name

    def uninitialize(self) -> None:
        self._wire_name = None

    def append_error(self, error: str) -> None:
        self.errors.append(error)

    @property
    def wire_name(self) -> str:
        if self._wire_name is None:
            raise ClassiqError("Invalid access to wire of not initialized handle")

        return self._wire_name


def get_unique_handle_names(io_dict: Mapping[str, HandleBinding]) -> Set[str]:
    return {handle_binding.name for handle_binding in io_dict.values()}
