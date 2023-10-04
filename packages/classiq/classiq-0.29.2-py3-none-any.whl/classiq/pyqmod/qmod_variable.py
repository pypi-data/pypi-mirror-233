from typing import (
    TYPE_CHECKING,
    Any,
    ForwardRef,
    Generic,
    Literal,
    NoReturn,
    TypeVar,
    get_args,
    get_origin,
)

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding

ILLEGAL_MULTIPLE_SLICING_MSG = "Multiple slicing of a QVar is not supported"


_T = TypeVar("_T")


class QVar(Generic[_T]):
    def __init__(self, name: str) -> None:
        self._name = name

    def get_handle_binding(self) -> HandleBinding:
        return HandleBinding(name=self._name)

    def __getitem__(self, key) -> "QVarSlice":
        start, end = (key.start, key.stop) if isinstance(key, slice) else (key, key + 1)
        return QVarSlice(self._name, start, end)

    @staticmethod
    def is_qvar_type(type_hint: Any) -> bool:
        origin = get_origin(type_hint)
        return origin is not None and issubclass(origin, QVar)

    @staticmethod
    def size_expr(type_hint: Any) -> str:
        args = get_args(type_hint)
        if len(args) != 1:
            raise ValueError("QVar accepts exactly one generic parameter")

        if (
            get_origin(args[0]) == Literal
        ):  # mypy legit way to pass in a non-type argument
            return str(get_args(args[0])[0])
        if isinstance(args[0], ForwardRef):
            return str(args[0].__forward_arg__)

        return str(args[0])

    @staticmethod
    def port_direction(type_hint: Any) -> PortDeclarationDirection:
        origin = get_origin(type_hint)
        if TYPE_CHECKING:
            assert origin is not None
            assert issubclass(origin, QVar)
        return origin._get_port_direction()

    @classmethod
    def _get_port_direction(cls) -> PortDeclarationDirection:
        return PortDeclarationDirection.Inout


class OutputQVar(QVar, Generic[_T]):
    @classmethod
    def _get_port_direction(cls) -> PortDeclarationDirection:
        return PortDeclarationDirection.Output


class InputQVar(QVar, Generic[_T]):
    @classmethod
    def _get_port_direction(cls) -> PortDeclarationDirection:
        return PortDeclarationDirection.Input


class QVarSlice(QVar):
    def __init__(self, name: str, start: int, end: int) -> None:
        super().__init__(name)
        self._start = start
        self._end = end

    def __getitem__(self, key) -> NoReturn:
        raise NotImplementedError(ILLEGAL_MULTIPLE_SLICING_MSG)

    def get_handle_binding(self) -> SlicedHandleBinding:
        return SlicedHandleBinding(
            name=self._name,
            start=Expression(expr=str(self._start)),
            end=Expression(expr=str(self._end)),
        )
