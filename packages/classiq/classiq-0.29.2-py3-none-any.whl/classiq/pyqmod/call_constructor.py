from typing import Dict

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.quantum_function_call import (
    QuantumFunctionCall,
    QuantumLambdaFunction,
)
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)

from classiq.pyqmod.utilities import mangle_keyword


def _create_port_bindings(
    decl: QuantumFunctionDeclaration, dir: PortDeclarationDirection, **kwargs
) -> Dict[str, Dict[str, HandleBinding]]:
    return {
        name: kwargs[mangle_keyword(name)].get_handle_binding()
        for name, port_decl in decl.port_declarations.items()
        if port_decl.direction == dir
    }


def _create_params(decl: QuantumFunctionDeclaration, **kwargs) -> Dict[str, Expression]:
    return {
        name: Expression(expr=str(kwargs[mangle_keyword(name)]))
        for name in decl.param_decls.keys()
    }


def _create_operands(
    decl: QuantumFunctionDeclaration, **kwargs
) -> Dict[str, QuantumLambdaFunction]:
    result: Dict[str, QuantumLambdaFunction] = {}
    for name in decl.operand_declarations.keys():
        operand = kwargs[mangle_keyword(name)]
        if operand.local_handles:
            raise ValueError("Locals are not supported in lambda functions")
        result[name] = QuantumLambdaFunction(
            rename_params=operand.infer_rename_params(), body=operand.body
        )
    return result


def create_quantum_function_call(
    decl: QuantumFunctionDeclaration, **kwargs
) -> QuantumFunctionCall:
    return QuantumFunctionCall(
        function=decl.name,
        params=_create_params(decl, **kwargs),
        operands=_create_operands(decl, **kwargs),
        inouts=_create_port_bindings(decl, PortDeclarationDirection.Inout, **kwargs),
        inputs=_create_port_bindings(decl, PortDeclarationDirection.Input, **kwargs),
        outputs=_create_port_bindings(decl, PortDeclarationDirection.Output, **kwargs),
    )
