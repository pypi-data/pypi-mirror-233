from typing import Any, Mapping

from classiq.interface.generator.classical_function_call import ClassicalFunctionCall
from classiq.interface.generator.quantum_invoker_call import QuantumInvokerCall
from classiq.interface.generator.visitor import Visitor
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)

from classiq import ClassicalFunctionDeclaration


class UserFunctionCallResolver(Visitor):
    def __init__(
        self,
        classical_function_dict: Mapping[str, ClassicalFunctionDeclaration],
        quantum_function_dict: Mapping[str, QuantumFunctionDeclaration],
    ) -> None:
        self._classical_function_dict = classical_function_dict
        self._quantum_function_dict = quantum_function_dict

    def visit_QuantumFunctionCall(self, fc: QuantumFunctionCall) -> None:
        fc.resolve_function_decl(self._quantum_function_dict)
        self.visit_BaseModel(fc)

    def visit_NativeFunctionDefinition(
        self, func_def: NativeFunctionDefinition
    ) -> None:
        curr_dict = self._quantum_function_dict
        self._quantum_function_dict = {
            **self._quantum_function_dict,
            **func_def.operand_declarations,
        }
        self.visit_BaseModel(func_def)
        self._quantum_function_dict = curr_dict

    def visit_ClassicalFunctionCall(self, fc: ClassicalFunctionCall) -> None:
        fc.resolve_function_decl(self._classical_function_dict)

    def visit_QuantumInvokerCall(self, fc: QuantumInvokerCall) -> None:
        self.visit_ClassicalFunctionCall(fc)
        fc.check_quantum_function_decl(self._quantum_function_dict)


class SynthesisFunctionCallResolver(Visitor):
    def __init__(
        self,
        classical_function_dict: Mapping[str, ClassicalFunctionDeclaration],
    ) -> None:
        self._classical_function_dict = classical_function_dict

    def visit_ClassicalFunctionCall(self, fc: ClassicalFunctionCall) -> None:
        fc.resolve_function_decl(self._classical_function_dict)

    def visit_QuantumInvokerCall(self, fc: QuantumInvokerCall) -> None:
        self.visit_ClassicalFunctionCall(fc)


def resolve_user_function_calls(
    root: Any,
    classical_function_dict: Mapping[str, ClassicalFunctionDeclaration],
    quantum_function_dict: Mapping[str, QuantumFunctionDeclaration],
) -> None:
    UserFunctionCallResolver(
        {
            **ClassicalFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS,
            **classical_function_dict,
        },
        {
            **QuantumFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS,
            **quantum_function_dict,
        },
    ).visit(root)


def resolve_synthesis_function_calls(
    root: Any,
    classical_function_dict: Mapping[str, ClassicalFunctionDeclaration],
) -> None:
    SynthesisFunctionCallResolver(
        {
            **ClassicalFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS,
            **classical_function_dict,
        },
    ).visit(root)
