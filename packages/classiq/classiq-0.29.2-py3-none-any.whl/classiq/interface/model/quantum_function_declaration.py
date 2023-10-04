from typing import Any, ClassVar, Dict, List, Mapping, Sequence, Set, Type, Union

import pydantic

from classiq.interface.generator.function_params import (
    ArithmeticIODict,
    IOName,
    PortDirection,
)
from classiq.interface.generator.functions.function_declaration import (
    FunctionDeclaration,
)
from classiq.interface.generator.functions.port_declaration import PortDeclaration
from classiq.interface.generator.functions.quantum_function_declaration import (
    _ports_to_registers,
)
from classiq.interface.helpers.pydantic_model_helpers import Nameable
from classiq.interface.helpers.validation_helpers import (
    validate_nameables_mapping,
    validate_nameables_no_overlap,
)
from classiq.interface.model.classical_parameter_declaration import (
    ClassicalParameterDeclaration,
)

from classiq.exceptions import ClassiqValueError


def _is_equiv_kw_and_pos_decl(kw_decl: Nameable, pos_decl: Nameable) -> bool:
    if isinstance(pos_decl, ClassicalParameterDeclaration):
        return pos_decl.classical_type == kw_decl
    return pos_decl == kw_decl


def _populate_declaration_dicts_with_positional_lists(
    pos_decls: Sequence[Nameable],
    kw_decls: Dict[str, Nameable],
    param_type: Type[Nameable],
) -> None:
    for pos_decl in pos_decls:
        if not isinstance(pos_decl, param_type):
            continue
        kw_decl = kw_decls.get(pos_decl.name)
        if kw_decl is not None and not _is_equiv_kw_and_pos_decl(kw_decl, pos_decl):
            raise ClassiqValueError(
                f"{param_type.__name__} parameter with name {pos_decl.name} already declared"
            )
        kw_decls[pos_decl.name] = (
            pos_decl.classical_type  # type:ignore[assignment]
            if isinstance(pos_decl, ClassicalParameterDeclaration)
            else pos_decl
        )


class QuantumFunctionDeclaration(FunctionDeclaration):
    """
    Facilitates the creation of a common quantum function interface object.
    """

    port_declarations: Dict[IOName, PortDeclaration] = pydantic.Field(
        description="The input and output ports of the function.",
        default_factory=dict,
    )

    operand_declarations: Mapping[str, "QuantumOperandDeclaration"] = pydantic.Field(
        description="The expected interface of the quantum function operands",
        default_factory=dict,
    )

    positional_param_declarations: List[
        Union[
            ClassicalParameterDeclaration, "QuantumOperandDeclaration", PortDeclaration
        ]
    ] = pydantic.Field(default_factory=list)

    BUILTIN_FUNCTION_DECLARATIONS: ClassVar[
        Dict[str, "QuantumFunctionDeclaration"]
    ] = {}

    @property
    def input_set(self) -> Set[IOName]:
        return set(self.inputs.keys())

    @property
    def output_set(self) -> Set[IOName]:
        return set(self.outputs.keys())

    @property
    def inputs(self) -> ArithmeticIODict:
        return _ports_to_registers(self.port_declarations, PortDirection.Input)

    @property
    def outputs(self) -> ArithmeticIODict:
        return _ports_to_registers(self.port_declarations, PortDirection.Output)

    def update_logic_flow(
        self, function_dict: Mapping[str, "QuantumFunctionDeclaration"]
    ) -> None:
        pass

    def ports_by_direction(
        self, direction: PortDirection
    ) -> Mapping[str, PortDeclaration]:
        return {
            name: port
            for name, port in self.port_declarations.items()
            if port.direction.includes_port_direction(direction)
        }

    @pydantic.validator("operand_declarations")
    def _validate_operand_declarations_names(
        cls, operand_declarations: Dict[str, "QuantumOperandDeclaration"]
    ) -> Dict[str, "QuantumOperandDeclaration"]:
        validate_nameables_mapping(operand_declarations, "Operand")
        return operand_declarations

    @pydantic.validator("port_declarations")
    def _validate_port_declarations_names(
        cls, port_declarations: Dict[IOName, PortDeclaration]
    ) -> Dict[IOName, PortDeclaration]:
        validate_nameables_mapping(port_declarations, "Port")
        return port_declarations

    @pydantic.root_validator()
    def _validate_params_and_operands_uniqueness(
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        operand_declarations = values.get("operand_declarations")
        parameter_declarations = values.get("param_decls")
        port_declarations = values.get("port_declarations")
        operand_parameter = validate_nameables_no_overlap(
            operand_declarations, parameter_declarations, "operand", "parameter"
        )
        operand_port = validate_nameables_no_overlap(
            operand_declarations, port_declarations, "operand", "port"
        )
        parameter_port = validate_nameables_no_overlap(
            parameter_declarations, port_declarations, "parameter", "port"
        )
        error_message = ",".join(
            msg
            for msg in [operand_parameter, operand_port, parameter_port]
            if msg is not None
        )

        if error_message:
            raise ClassiqValueError(error_message)

        return values

    @pydantic.root_validator()
    def _reduce_positional_declarations_to_keyword(
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        operand_declarations = values.get("operand_declarations", dict())
        parameter_declarations = values.get("param_decls", dict())
        port_declarations = values.get("port_declarations", dict())

        positional_param_declarations = values.get(
            "positional_param_declarations", list()
        )

        _populate_declaration_dicts_with_positional_lists(
            positional_param_declarations,
            parameter_declarations,
            ClassicalParameterDeclaration,
        )
        _populate_declaration_dicts_with_positional_lists(
            positional_param_declarations,
            operand_declarations,
            QuantumOperandDeclaration,
        )
        _populate_declaration_dicts_with_positional_lists(
            positional_param_declarations, port_declarations, PortDeclaration
        )

        values["operand_declarations"] = operand_declarations
        values["param_decls"] = parameter_declarations
        values["port_declarations"] = port_declarations

        return values


class QuantumOperandDeclaration(QuantumFunctionDeclaration):
    is_list: bool = pydantic.Field(
        description="Indicate whether the operand expects an unnamed list of lambdas",
        default=False,
    )


QuantumFunctionDeclaration.update_forward_refs()
