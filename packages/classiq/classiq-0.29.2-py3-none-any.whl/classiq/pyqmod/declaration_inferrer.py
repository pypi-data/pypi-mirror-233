import dataclasses
import inspect
import sys
from typing import Any, Callable, Dict, Optional, Type, get_args, get_origin

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.function_params import IOName
from classiq.interface.generator.functions import PortDeclaration
from classiq.interface.generator.functions.classical_type import (
    Bool,
    ClassicalList,
    ConcreteClassicalType,
    Integer,
    QStructBase,
    Real,
    Struct,
)
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
    QuantumOperandDeclaration,
)

from classiq import StructDeclaration
from classiq.pyqmod.model_state_container import ModelStateContainer
from classiq.pyqmod.qmod_parameter import QParam
from classiq.pyqmod.qmod_variable import QVar
from classiq.pyqmod.quantum_callable import QCallable
from classiq.pyqmod.utilities import unmangle_keyword

OPERAND_ARG_NAME = "arg{i}"


def _python_type_to_qmod(py_type: type) -> Optional[ConcreteClassicalType]:
    if py_type == int:
        return Integer()
    elif py_type == float:
        return Real()
    elif py_type == bool:
        return Bool()
    elif get_origin(py_type) == list:
        return ClassicalList(element_type=_python_type_to_qmod(get_args(py_type)[0]))
    elif inspect.isclass(py_type) and issubclass(py_type, QStructBase):
        _add_qmod_struct(py_type)
        return Struct(name=py_type.__name__)
    return None


def _add_qmod_struct(py_type: Type[QStructBase]) -> None:
    if (
        py_type.__name__ in StructDeclaration.BUILTIN_STRUCT_DECLARATIONS
        or py_type.__name__ in ModelStateContainer.TYPE_DECLS.keys()
    ):
        return

    ModelStateContainer.TYPE_DECLS[py_type.__name__] = StructDeclaration(
        name=py_type.__name__,
        variables={
            f.name: _python_type_to_qmod(f.type) for f in dataclasses.fields(py_type)
        },
    )


def _extract_param_decls(args: Dict[str, Any]) -> Dict[str, ConcreteClassicalType]:
    result: Dict[str, ConcreteClassicalType] = {}
    for name, py_type in args.items():
        name = unmangle_keyword(name)
        if get_origin(py_type) == QParam:
            if len(get_args(py_type)) != 1:
                raise ValueError("QParam takes exactly one generic argument")
            py_type = get_args(py_type)[0]
        qmod_type = _python_type_to_qmod(py_type)
        if qmod_type is not None:
            result[name] = qmod_type
    return result


def _extract_port_decls(args: Dict[str, Any]) -> Dict[IOName, PortDeclaration]:
    result: Dict[IOName, PortDeclaration] = {}
    for name, py_type in args.items():
        name = unmangle_keyword(name)
        if QVar.is_qvar_type(py_type):
            result[name] = PortDeclaration(
                name=name,
                direction=QVar.port_direction(py_type),
                size=Expression(expr=QVar.size_expr(py_type)),
            )
    return result


def _extract_operand_declarations(
    args: Dict[str, Any]
) -> Dict[str, QuantumOperandDeclaration]:
    result: Dict[str, QuantumOperandDeclaration] = {}
    for name, py_type in args.items():
        name = unmangle_keyword(name)
        if get_origin(py_type) == QCallable:
            if sys.version_info[0:2] < (3, 10):
                qc_args = get_args(py_type)  # The result of __class_getitem__
            else:
                qc_args = get_args(py_type)[0]
            arg_dict = {
                OPERAND_ARG_NAME.format(i=i): arg_type
                for i, arg_type in enumerate(qc_args)
            }
            result[name] = QuantumOperandDeclaration(
                name=name,
                param_decls=_extract_param_decls(arg_dict),
                port_declarations=_extract_port_decls(arg_dict),
            )
    return result


def infer_func_decl(py_func: Callable) -> QuantumFunctionDeclaration:
    return QuantumFunctionDeclaration(
        name=py_func.__name__,
        param_decls=_extract_param_decls(py_func.__annotations__),
        port_declarations=_extract_port_decls(py_func.__annotations__),
        operand_declarations=_extract_operand_declarations(py_func.__annotations__),
    )
