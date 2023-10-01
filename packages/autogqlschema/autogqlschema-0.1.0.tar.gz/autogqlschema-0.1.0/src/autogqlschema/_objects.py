from __future__ import annotations

from typing import Any, Generic, TypeVar, Union

import sphinx
from typing_extensions import Self, TypeGuard

NamedTypes = Union[
    "GraphQLEnum",
    "GraphQLInput",
    "GraphQLInterface",
    "GraphQLType",
    "GraphQLScalar",
    "GraphQLUnion",
]
SchemaChildTypes = Union["GraphQLDirective", NamedTypes]
T = TypeVar("T", bound="GraphQLObject")


class GraphQLObject:
    type: str

    def __init__(
        self,
        description: str | None,
        signature: str,
        line: int | None = None,
    ) -> None:
        self.description = description
        self.signature = signature
        self.line = line

    def __repr__(self) -> str:
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__
        return f"<{module}.{qualname}({repr(self.signature)}) at {hex(id(self))}>"

    def get_context_data(self) -> dict[str, Any]:
        return {
            "obj": self,
            "sphinx_version": sphinx.version_info,
            "description": self.description,
            "signature": self.signature,
        }

    def __eq__(self, other: object) -> TypeGuard[Self]:
        if not isinstance(other, GraphQLObject):
            return NotImplemented

        return (
            self.__class__ == other.__class__
            and self.description == other.description
            and self.signature == other.signature
            and self.line == other.line
        )


class GraphQLObjectWithChildren(GraphQLObject, Generic[T]):
    def __init__(
        self,
        children: list[T],
        description: str | None,
        signature: str,
        line: int | None = None,
    ) -> None:
        super().__init__(description, signature, line)

        self.children = children

    def get_context_data(self) -> dict[str, Any]:
        context_data = super().get_context_data()

        context_data["children"] = self.children

        return context_data

    def __eq__(self, other: object) -> TypeGuard[Self]:
        if not isinstance(other, GraphQLObjectWithChildren):
            return NotImplemented

        result = super().__eq__(other)
        if result is not True:
            return result

        return self.children == other.children


class GraphQLObjectWithArgs(GraphQLObject):
    def __init__(
        self,
        args: dict[str, str | None],
        description: str | None,
        signature: str,
        line: int | None = None,
    ) -> None:
        super().__init__(description, signature, line)

        self.args = args

    def get_context_data(self) -> dict[str, Any]:
        context_data = super().get_context_data()

        context_data["args"] = self.args

        return context_data

    def __eq__(self, other: object) -> TypeGuard[Self]:
        if not isinstance(other, GraphQLObjectWithArgs):
            return NotImplemented

        result = super().__eq__(other)
        if result is not True:
            return result

        return self.args == other.args


class GraphQLDirective(GraphQLObjectWithArgs):
    type = "directive"


class GraphQLEnum(GraphQLObjectWithChildren["GraphQLEnumValue"]):
    type = "enum"


class GraphQLEnumValue(GraphQLObject):
    type = "enum_value"


class GraphQLInput(GraphQLObjectWithChildren["GraphQLInputField"]):
    type = "input"


class GraphQLInputField(GraphQLObject):
    type = "input_field"


class GraphQLInterface(GraphQLObjectWithChildren["GraphQLInterfaceField"]):
    type = "interface"


class GraphQLInterfaceField(GraphQLObjectWithArgs):
    type = "interface_field"


class GraphQLScalar(GraphQLObject):
    type = "scalar"


class GraphQLSchema(GraphQLObjectWithChildren[SchemaChildTypes]):
    type = "schema"

    def __init__(
        self,
        children: list[SchemaChildTypes],
        description: str | None,
        signature: str,
        line: int | None = None,
    ) -> None:
        super().__init__(children, description, signature, line)

        self.name = "__gqlschema__"
        self.query_type: str | None = None
        self.mutation_type: str | None = None
        self.subscription_type: str | None = None

    def get_context_data(self) -> dict[str, Any]:
        context_data = super().get_context_data()

        context_data["name"] = self.name
        context_data["query_type"] = self.query_type
        context_data["mutation_type"] = self.mutation_type
        context_data["subscription_type"] = self.subscription_type

        return context_data

    def __eq__(self, other: object) -> TypeGuard[Self]:
        if not isinstance(other, GraphQLSchema):
            return NotImplemented

        result = super().__eq__(other)
        if result is not True:
            return result

        return (
            self.name == other.name
            and self.query_type == other.query_type
            and self.mutation_type == other.mutation_type
            and self.subscription_type == other.subscription_type
        )


class GraphQLType(GraphQLObjectWithChildren["GraphQLTypeField"]):
    type = "type"


class GraphQLTypeField(GraphQLObjectWithArgs):
    type = "type_field"


class GraphQLUnion(GraphQLObject):
    type = "union"
