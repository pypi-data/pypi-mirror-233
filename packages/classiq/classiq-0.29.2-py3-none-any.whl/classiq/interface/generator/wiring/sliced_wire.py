from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)


class SlicedWire(HashablePydanticBaseModel):
    name: str
    start: Expression
    end: Expression

    def add_prefix(self, prefix: str) -> "SlicedWire":
        return self.copy(update={"name": prefix + self.name})

    class Config:
        frozen = True


class InoutSlicedWire(HashablePydanticBaseModel):
    input_name: str
    output_name: str
    start: Expression
    end: Expression

    @property
    def source_slice(self) -> SlicedWire:
        return SlicedWire(
            name=self.input_name,
            start=self.start,
            end=self.end,
        )

    @property
    def destination_slice(self) -> SlicedWire:
        return SlicedWire(
            name=self.output_name,
            start=self.start,
            end=self.end,
        )

    class Config:
        frozen = True
