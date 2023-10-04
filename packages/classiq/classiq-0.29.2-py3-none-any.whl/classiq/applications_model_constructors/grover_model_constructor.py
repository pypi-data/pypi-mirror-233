from typing import Dict, List, Tuple

from classiq.interface.generator.arith.arithmetic_expression_abc import (
    UncomputationMethods,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclaration,
    PortDeclarationDirection,
)
from classiq.interface.generator.oracles import ArithmeticOracle
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.local_handle import LocalHandle
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_call import (
    QuantumFunctionCall,
    QuantumLambdaFunction,
)

from classiq import RegisterUserInput

_OUTPUT_VARIABLE_NAME = "result"


def split_registers(
    register_names: List[str],
    register_sizes: List[int],
    input_wire_name: str,
) -> List[QuantumFunctionCall]:
    if len(register_names) == 0:
        return []
    wires = (
        [input_wire_name]
        + [f"split{i}" for i in range(len(register_names) - 2)]
        + [register_names[-1]]
    )
    return [
        QuantumFunctionCall(
            function="split",
            params={
                "out1_size": Expression(expr=f"{int(register_sizes[i])}"),
                "out2_size": Expression(expr=f"{int(sum(register_sizes[i + 1:]))}"),
            },
            inputs={"in": HandleBinding(name=wires[i])},
            outputs={
                "out1": HandleBinding(name=register),
                "out2": HandleBinding(name=wires[i + 1]),
            },
        )
        for i, register in enumerate(register_names[:-1])
    ]


def _arithmetic_oracle_io_dict(
    definitions: List[Tuple[str, RegisterUserInput]], handle_name: str
) -> Dict[str, SlicedHandleBinding]:
    cursor = 0
    ios = dict()
    for reg_name, reg in definitions:
        ios[reg_name] = SlicedHandleBinding(
            name=handle_name,
            start=Expression(expr=f"{cursor}"),
            end=Expression(expr=f"{cursor + reg.size}"),
        )
        cursor += reg.size
    return ios


def _construct_arithmetic_oracle(
    expression: str,
    definitions: List[Tuple[str, RegisterUserInput]],
    uncomputation_method: UncomputationMethods,
) -> QuantumFunctionCall:
    return QuantumFunctionCall(
        function="ArithmeticOracle",
        function_params=ArithmeticOracle(
            expression=expression,
            definitions={name: reg for name, reg in definitions},
            uncomputation_method=uncomputation_method,
        ),
        inouts=_arithmetic_oracle_io_dict(definitions, "oq"),
    )


def grover_main_port_declarations(
    definitions: List[Tuple[str, RegisterUserInput]]
) -> Dict[str, PortDeclaration]:
    return {
        name: PortDeclaration(
            name=name,
            size=Expression(expr=f"{reg.size}"),
            is_signed=Expression(expr=f"{reg.is_signed}"),
            fraction_places=Expression(expr=f"{reg.fraction_places}"),
            direction=PortDeclarationDirection.Output,
        )
        for name, reg in definitions
    }


def construct_grover_model(
    definitions: List[Tuple[str, RegisterUserInput]],
    expression: str,
    uncomputation_method: UncomputationMethods = UncomputationMethods.optimized,
    num_reps: int = 1,
) -> SerializedModel:
    grover_model = Model(
        functions=[
            NativeFunctionDefinition(
                name="main",
                port_declarations=grover_main_port_declarations(definitions),
                local_handles=[
                    LocalHandle(name="gsq"),
                    *[
                        LocalHandle(name=f"split{i}")
                        for i in range(len(definitions) - 2)
                    ],
                ],
                body=[
                    QuantumFunctionCall(
                        function="grover_search",
                        params={
                            "num_qubits": Expression(
                                expr=f"{sum(reg.size for _, reg in definitions)}"
                            ),
                            "reps": Expression(expr=f"{num_reps}"),
                        },
                        outputs={"gsq": HandleBinding(name="gsq")},
                        operands={
                            "oracle_op": QuantumLambdaFunction(
                                body=[
                                    _construct_arithmetic_oracle(
                                        expression,
                                        definitions,
                                        uncomputation_method,
                                    )
                                ]
                            )
                        },
                    ),
                    *split_registers(
                        [name for name, _ in definitions],
                        [reg.size for _, reg in definitions],
                        "gsq",
                    ),
                ],
            ),
        ],
        classical_execution_code=f"""
{_OUTPUT_VARIABLE_NAME} = sample()
save({{{_OUTPUT_VARIABLE_NAME!r}: {_OUTPUT_VARIABLE_NAME}}})
""",
    )
    return grover_model.get_model()
