from typing import Dict, List, Union

import pydantic

from classiq.interface.generator.parameters import ParameterFloatType, ParameterMap
from classiq.interface.model.arithmetic_operation import ArithmeticOperation
from classiq.interface.model.local_handle import LocalHandle
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)
from classiq.interface.model.validations.handles_to_wires_reduction import HandleReducer

from classiq.exceptions import ClassiqValueError

ConcreteQuantumStatement = Union[QuantumFunctionCall, ArithmeticOperation]


class NativeFunctionDefinition(QuantumFunctionDeclaration):
    """
    Facilitates the creation of a user-defined composite function

    This class sets extra to forbid so that it can be used in a Union and not "steal"
    objects from other classes.
    """

    parameters: List[ParameterMap] = pydantic.Field(
        default_factory=list,
        description="The parameters (name and mapped parameter or value) of the function",
    )

    body: List[ConcreteQuantumStatement] = pydantic.Field(
        default_factory=list, description="List of function calls to perform."
    )

    local_handles: List[LocalHandle] = pydantic.Field(
        default_factory=list, description="List of local handles."
    )

    def validate_body(self) -> None:
        handle_reducer = HandleReducer(self.port_declarations, self.local_handles)

        for call in self.body:
            handle_reducer.reduce_call(call)

        handle_reducer.report_errored_handles(ClassiqValueError)

    @property
    def parameters_mapping(self) -> Dict[str, ParameterFloatType]:
        return {
            parameter.original: parameter.new_parameter for parameter in self.parameters
        }
