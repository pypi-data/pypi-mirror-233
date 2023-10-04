from typing import TYPE_CHECKING, Any, Generic, TypeVar

from sympy import Symbol

from classiq.interface.generator.functions.classical_type import (
    ClassicalList,
    ClassicalType,
    Struct,
)

from classiq import StructDeclaration
from classiq.pyqmod.model_state_container import ModelStateContainer

_T = TypeVar("_T")


if TYPE_CHECKING:

    class QParam(Generic[_T], Symbol):  # expose to mypy all operators
        pass

else:

    class QParam(Generic[_T]):
        pass


class QParamScalar(QParam, Symbol):
    pass


class QParamList(QParam):
    def __init__(self, expr_str: str, list_type: ClassicalList) -> None:
        self._expr_str = expr_str
        self._list_type = list_type

    def __str__(self) -> str:
        return self._expr_str

    def __getitem__(self, key: Any) -> QParam:
        return create_param(
            f"{self._expr_str}[{str(key)}]", self._list_type.element_type
        )

    def __len__(self) -> int:
        raise ValueError(
            "len(<expr>) is not supported for QMod lists - use <expr>.len() instead"
        )

    def len(self) -> "QParamScalar":
        return QParamScalar(name=f"len({self._expr_str})")


class QParamStruct(QParam):
    def __init__(self, expr_str: str, struct_type: Struct) -> None:
        self._expr_str = expr_str
        self._struct_type = struct_type

    def __str__(self) -> str:
        return self._expr_str

    def __getattr__(self, field_name: str) -> QParam:
        struct_decl = StructDeclaration.BUILTIN_STRUCT_DECLARATIONS.get(
            self._struct_type.name
        )
        if struct_decl is None:
            struct_decl = ModelStateContainer.TYPE_DECLS.get(self._struct_type.name)
        assert struct_decl is not None
        field_type = struct_decl.variables.get(field_name)
        if field_type is None:
            raise ValueError(
                f"Struct {self._struct_type.name!r} doesn't have field {field_name!r}"
            )

        return create_param(f"get_field({self._expr_str},{field_name!r})", field_type)


def create_param(expr_str: str, ctype: ClassicalType) -> QParam:
    if isinstance(ctype, ClassicalList):
        return QParamList(expr_str, ctype)
    elif isinstance(ctype, Struct):
        return QParamStruct(expr_str, ctype)
    else:
        return QParamScalar(expr_str)
