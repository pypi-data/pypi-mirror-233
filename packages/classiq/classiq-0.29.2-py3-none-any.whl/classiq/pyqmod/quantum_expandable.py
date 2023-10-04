import itertools
from abc import ABC
from functools import cached_property
from typing import Any, Callable, ClassVar, Dict, List

from classiq.interface.model.local_handle import LocalHandle
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)

from classiq.pyqmod.qmod_parameter import QParam, create_param
from classiq.pyqmod.qmod_variable import QVar
from classiq.pyqmod.quantum_callable import QCallable, QExpandableInterface
from classiq.pyqmod.utilities import mangle_keyword


class QExpandable(QCallable, QExpandableInterface, ABC):
    QCALLABLE_STACK: ClassVar[List["QExpandable"]] = list()

    def __init__(self, py_callable: Callable) -> None:
        self._py_callable = py_callable
        self._local_handles: List[LocalHandle] = list()
        self._body: List[QuantumFunctionCall] = list()

    @property
    def local_handles(self) -> List[LocalHandle]:
        return self._local_handles

    @cached_property
    def body(self) -> List[QuantumFunctionCall]:
        self._expand()
        return self._body

    def __enter__(self) -> "QExpandable":
        QExpandable.QCALLABLE_STACK.append(self)
        QCallable.CURRENT_EXPANDABLE = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        assert QExpandable.QCALLABLE_STACK.pop() is self
        QCallable.CURRENT_EXPANDABLE = (
            QExpandable.QCALLABLE_STACK[-1] if QExpandable.QCALLABLE_STACK else None
        )

    def _expand(self) -> None:
        with self:
            self._py_callable(
                **self._get_qvars_from_port_decls(),
                **self._get_qparams_from_param_decls(),
                **self._get_qexpandables_from_operand_decls(),
            )

    def infer_rename_params(self) -> Dict[str, str]:
        return {
            decl_name: actual_name
            for decl_name, actual_name in list(
                zip(
                    self.func_decl.param_decls.keys(),
                    self._py_callable.__annotations__.keys(),
                )
            )
            if decl_name != actual_name
        }

    def _add_local_handle(self, qfunc_call: QuantumFunctionCall) -> None:
        for binding in itertools.chain(
            qfunc_call.inputs.values(),
            qfunc_call.inouts.values(),
            qfunc_call.outputs.values(),
        ):
            if binding.name not in self.func_decl.port_declarations and not any(
                lh.name == binding.name for lh in self._local_handles
            ):
                self._local_handles.append(LocalHandle(name=binding.name))

    def append_call_to_body(self, qfunc_call: QuantumFunctionCall) -> None:
        self._add_local_handle(qfunc_call)
        self._body.append(qfunc_call)

    def _get_qvars_from_port_decls(self) -> Dict[str, QVar]:
        return {
            mangle_keyword(name): QVar(name=name)
            for name in self.func_decl.port_declarations
        }

    def _get_qparams_from_param_decls(self) -> Dict[str, QParam]:
        result: Dict[str, QParam] = {}
        rename_dict = self.infer_rename_params()
        for name, ctype in self.func_decl.param_decls.items():
            actual_name = rename_dict[name] if name in rename_dict else name
            result[actual_name] = create_param(actual_name, ctype)
        return result

    def _get_qexpandables_from_operand_decls(self) -> Dict[str, QCallable]:
        return {
            name: QTerminalCallable(decl)
            for name, decl in self.func_decl.operand_declarations.items()
        }

    def prepare_operands(self, kwargs: Dict[str, Any]) -> None:
        _prepare_operands(self.func_decl, kwargs)


class QOperandDecl(QExpandable):
    def __init__(self, decl: QuantumFunctionDeclaration, py_callable: Callable) -> None:
        super().__init__(py_callable)
        self._decl = decl

    @property
    def func_decl(self) -> QuantumFunctionDeclaration:
        return self._decl


class QTerminalCallable(QCallable):
    def __init__(self, decl: QuantumFunctionDeclaration) -> None:
        self._decl = decl

    @property
    def func_decl(self) -> QuantumFunctionDeclaration:
        return self._decl

    def prepare_operands(self, kwargs: Dict[str, Any]) -> None:
        _prepare_operands(self.func_decl, kwargs)


def _prepare_operands(decl, kwargs: Dict[str, Any]) -> None:
    kwargs.update(
        {
            mangle_keyword(name): QOperandDecl(decl, kwargs[mangle_keyword(name)])
            for name, decl in decl.operand_declarations.items()
            if not isinstance(kwargs[mangle_keyword(name)], QExpandable)
        }
    )
