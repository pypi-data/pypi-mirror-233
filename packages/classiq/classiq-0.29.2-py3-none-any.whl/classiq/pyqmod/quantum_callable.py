import itertools
import sys
from abc import ABC, abstractmethod
from typing import _GenericAlias  # type: ignore[attr-defined]
from typing import Any, ClassVar, Dict, Generic, Iterable, List, Optional, Tuple

from typing_extensions import ParamSpec

from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)

from classiq.exceptions import ClassiqError
from classiq.pyqmod.call_constructor import create_quantum_function_call


def _add_args_to_kwargs(
    arg_names: List[str], args: Tuple[Any, ...], kwargs: Dict[str, Any]
) -> None:
    args_dict = dict(zip(arg_names, args))
    if not set(args_dict).isdisjoint(kwargs):
        raise ClassiqError("Attempted to pass same argument twice")
    kwargs.update(args_dict)


def all_decl_arg_names(decl: QuantumFunctionDeclaration) -> Iterable[str]:
    return itertools.chain(
        decl.param_decls.keys(),
        decl.operand_declarations.keys(),
        decl.port_declarations.keys(),
    )


P = ParamSpec("P")


class QExpandableInterface(ABC):
    @abstractmethod
    def append_call_to_body(self, qfunc_call: QuantumFunctionCall) -> None:
        raise NotImplementedError


class QCallable(Generic[P]):
    CURRENT_EXPANDABLE: ClassVar[Optional[QExpandableInterface]] = None

    def __call__(self, *args, **kwargs) -> None:
        _add_args_to_kwargs(list(all_decl_arg_names(self.func_decl)), args, kwargs)
        self.prepare_operands(kwargs)
        assert QCallable.CURRENT_EXPANDABLE is not None
        QCallable.CURRENT_EXPANDABLE.append_call_to_body(
            create_quantum_function_call(self.func_decl, **kwargs)
        )

    @property
    @abstractmethod
    def func_decl(self) -> QuantumFunctionDeclaration:
        raise NotImplementedError

    # Support comma-separated generic args in older Python versions
    if sys.version_info[0:2] < (3, 10):

        def __class_getitem__(cls, args) -> _GenericAlias:
            return _GenericAlias(cls, args)

    @abstractmethod
    def prepare_operands(self, kwargs: Dict[str, Any]) -> None:
        raise NotImplementedError
