from __future__ import annotations

import operator
import typing
from typing import Protocol, Sequence, Type, TypeVar

import graphql
import graphql.type
from graphql.language import ast as gql_ast
import graphql.utilities

if typing.TYPE_CHECKING:
    from _typeshed import StrPath

from ._objects import (
    GraphQLDirective,
    GraphQLEnum,
    GraphQLEnumValue,
    GraphQLInput,
    GraphQLInputField,
    GraphQLInterface,
    GraphQLInterfaceField,
    GraphQLScalar,
    GraphQLSchema,
    GraphQLType,
    GraphQLTypeField,
    GraphQLUnion,
    SchemaChildTypes,
    NamedTypes,
)

T = TypeVar("T", GraphQLTypeField, GraphQLInterfaceField)


def _unparse_directives(ast_nodes: Sequence[gql_ast.ConstDirectiveNode]) -> str:
    result = ""

    for directive_node in ast_nodes:
        result += " @"

        result += directive_node.name.value
        result += _unparse_const_arguments(directive_node.arguments)

    return result


def _unparse_const_arguments(ast_nodes: Sequence[gql_ast.ConstArgumentNode]) -> str:
    result = ""

    if not ast_nodes:
        return result

    result += "("

    for i, argument_node in enumerate(ast_nodes):
        if i != 0:
            result += ", "

        result += argument_node.name.value
        result += ": "
        result += _unparse_literal(argument_node.value)

    result += ")"
    return result


def _unparse_input_values(
    ast_nodes: Sequence[gql_ast.InputValueDefinitionNode],
) -> str:
    result = ""
    if not ast_nodes:
        return result

    result += "("

    for i, argument_node in enumerate(ast_nodes):
        if i != 0:
            result += ", "

        result += argument_node.name.value
        result += ": "
        result += _unparse_type_reference(argument_node.type)
        result += _unparse_default_value(argument_node.default_value)
        result += _unparse_directives(argument_node.directives)

    result += ")"
    return result


def _unparse_default_value(ast_nodes: gql_ast.ConstValueNode | None) -> str:
    result = ""
    if not ast_nodes:
        return result

    result += " = "
    result += _unparse_literal(ast_nodes)
    return result


def _unparse_literal(ast_nodes: gql_ast.ConstValueNode | None) -> str:
    result = ""

    if isinstance(ast_nodes, gql_ast.ListValueNode):
        result += "["
        for i, item_node in enumerate(ast_nodes.values):
            if i != 0:
                result += ", "

            result += _unparse_literal(item_node)

        result += "]"

    elif isinstance(ast_nodes, gql_ast.ObjectValueNode):
        result += "{"
        for i, field_node in enumerate(ast_nodes.fields):
            if i != 0:
                result += ", "

            result += field_node.name.value
            result += ": "
            result += _unparse_literal(field_node.value)

        result += "}"

    elif isinstance(ast_nodes, (gql_ast.IntValueNode, gql_ast.FloatValueNode)):
        result += str(ast_nodes.value)
    elif isinstance(ast_nodes, gql_ast.StringValueNode):
        result += '"'
        result += ast_nodes.value
        result += '"'
    elif isinstance(ast_nodes, gql_ast.BooleanValueNode):
        result += str(ast_nodes.value).lower()
    elif isinstance(ast_nodes, gql_ast.NullValueNode):
        result += "null"
    elif isinstance(ast_nodes, gql_ast.EnumValueNode):
        result += ast_nodes.value
    # Variable values are a valid literal but not in schemas
    else:
        raise TypeError(f"Unknown literal node type '{type(ast_nodes)}'")

    return result


def _unparse_type_reference(
    ast_node: gql_ast.TypeNode,
) -> str:
    result = ""

    if isinstance(ast_node, gql_ast.NamedTypeNode):
        result += ast_node.name.value
    elif isinstance(ast_node, gql_ast.NonNullTypeNode):
        result += _unparse_type_reference(ast_node.type)
        result += "!"
    elif isinstance(ast_node, gql_ast.ListTypeNode):
        result += "["
        result += _unparse_type_reference(ast_node.type)
        result += "]"
    else:
        raise TypeError(f"Unknown type node '{type(ast_node)}")

    return result


class DefinitionNode(Protocol):
    @property
    def ast_node(self) -> graphql.DefinitionNode | None:
        ...


def _get_source_line(node: DefinitionNode) -> int | None:
    if node.ast_node and node.ast_node.loc:
        return node.ast_node.loc.start_token.line

    return None


class Parser:
    _DEFAULT_TYPES = {
        "Int",
        "Float",
        "String",
        "Boolean",
        "ID",
    }
    """The names of all default types.

    As documented in https://spec.graphql.org/June2018/#sec-Scalars
    """

    def _parse_directive(self, node: graphql.type.GraphQLDirective) -> GraphQLDirective:
        name = node.name

        arguments = ""
        args = {}
        assert node.ast_node, "Tried to parse a directive not from source"
        if node.ast_node.arguments:
            arguments = _unparse_input_values(node.ast_node.arguments)
            args = {name: arg.description for name, arg in node.args.items()}

        locations = " | ".join(location.name for location in node.locations)

        description = node.description
        signature = f"@{name}{arguments} on {locations}"
        line = _get_source_line(node)
        directive = GraphQLDirective(args, description, signature, line)
        return directive

    def _parse_enumtype(self, node: graphql.type.GraphQLEnumType) -> GraphQLEnum:
        name = node.name

        if not node.ast_node:
            raise RuntimeError(f"Enum '{name}' has no AST node, so cannot be parsed")

        directives = ""
        all_directives = list(node.ast_node.directives)
        for ast_node in node.extension_ast_nodes:
            all_directives.extend(ast_node.directives)

        if all_directives:
            directives = _unparse_directives(all_directives)

        children = []
        for value_name, value in node.values.items():
            obj = self._parse_enumvalue(value_name, value)
            children.append(obj)

        children.sort(key=operator.attrgetter("line"))
        description = node.description
        signature = f"{name}{directives}"
        line = _get_source_line(node)
        return GraphQLEnum(children, description, signature, line)

    def _parse_enumvalue(
        self, name: str, node: graphql.type.GraphQLEnumValue
    ) -> GraphQLEnumValue:
        if not node.ast_node:
            raise RuntimeError(
                f"Enum value '{name}' has not AST node, so cannot be parsed"
            )

        directives = ""
        if node.ast_node.directives:
            directives = _unparse_directives(node.ast_node.directives)

        description = node.description
        signature = f"{name}{directives}"
        line = _get_source_line(node)
        return GraphQLEnumValue(description, signature, line)

    def _parse_field(
        self, name: str, obj_type: Type[T], node: graphql.type.GraphQLField
    ) -> T:
        if not node.ast_node:
            raise RuntimeError(f"Field '{name}' has no AST node, so cannot be parsed")

        arguments = ""
        args = {}
        if node.ast_node.arguments:
            arguments = _unparse_input_values(node.ast_node.arguments)
            args = {arg_name: arg.description for arg_name, arg in node.args.items()}

        type_ = _unparse_type_reference(node.ast_node.type)

        directives = ""
        if node.ast_node.directives:
            directives = _unparse_directives(node.ast_node.directives)

        description = node.description
        signature = f"{name}{arguments}: {type_}{directives}"
        line = _get_source_line(node)
        field = obj_type(args, description, signature, line)
        return field

    def _parse_type_field(
        self, name: str, node: graphql.type.GraphQLField
    ) -> GraphQLTypeField:
        return self._parse_field(name, GraphQLTypeField, node)

    def _parse_interface_field(
        self, name: str, node: graphql.type.GraphQLField
    ) -> GraphQLInterfaceField:
        return self._parse_field(name, GraphQLInterfaceField, node)

    def _parse_input_field(
        self, name: str, node: graphql.type.GraphQLInputField
    ) -> GraphQLInputField:
        if not node.ast_node:
            raise RuntimeError(
                f"Input field '{name}' has no AST node and cannot be parsed"
            )

        type_ = _unparse_type_reference(node.ast_node.type)

        default_value = ""
        if node.ast_node.default_value:
            default_value = _unparse_default_value(node.ast_node.default_value)

        directives = ""
        if node.ast_node.directives:
            directives = _unparse_directives(node.ast_node.directives)

        description = node.description
        signature = f"{name}: {type_}{default_value}{directives}"
        line = _get_source_line(node)
        return GraphQLInputField(description, signature, line)

    def _parse_inputobjecttype(
        self, node: graphql.type.GraphQLInputObjectType
    ) -> GraphQLInput:
        name = node.name

        if not node.ast_node:
            raise RuntimeError(f"Input '{name}' has no AST node, so cannot be parsed")

        directives = ""
        all_directives = list(node.ast_node.directives)
        for ast_node in node.extension_ast_nodes:
            all_directives.extend(ast_node.directives)

        if all_directives:
            directives = _unparse_directives(all_directives)

        children = []
        for field_name, field in node.fields.items():
            obj = self._parse_input_field(field_name, field)
            children.append(obj)

        children.sort(key=operator.attrgetter("line"))
        description = node.description
        signature = f"{name}{directives}"
        line = _get_source_line(node)
        return GraphQLInput(children, description, signature, line)

    def _parse_interfacetype(
        self, node: graphql.type.GraphQLInterfaceType
    ) -> GraphQLInterface:
        name = node.name

        if not node.ast_node:
            raise RuntimeError(
                f"Interface '{name}' has no AST node, so cannot be parsed"
            )

        directives = ""
        all_directives = list(node.ast_node.directives)
        for ast_node in node.extension_ast_nodes:
            all_directives.extend(ast_node.directives)

        if all_directives:
            directives = _unparse_directives(all_directives)

        children = []
        for field_name, field in node.fields.items():
            obj = self._parse_interface_field(field_name, field)
            children.append(obj)

        children.sort(key=operator.attrgetter("line"))
        description = node.description
        signature = f"{name}{directives}"
        line = _get_source_line(node)
        return GraphQLInterface(children, description, signature, line)

    def _parse_named_type(self, node: graphql.type.GraphQLNamedType) -> NamedTypes:
        if isinstance(node, graphql.type.GraphQLEnumType):
            return self._parse_enumtype(node)

        if isinstance(node, graphql.type.GraphQLInputObjectType):
            return self._parse_inputobjecttype(node)

        if isinstance(node, graphql.type.GraphQLInterfaceType):
            return self._parse_interfacetype(node)

        if isinstance(node, graphql.type.GraphQLObjectType):
            return self._parse_objecttype(node)

        if isinstance(node, graphql.type.GraphQLScalarType):
            return self._parse_scalartype(node)

        if isinstance(node, graphql.type.GraphQLUnionType):
            return self._parse_uniontype(node)

        raise TypeError(f"Unknown named type: {type(node)}")

    def _parse_objecttype(self, node: graphql.type.GraphQLObjectType) -> GraphQLType:
        name = node.name

        interfaces = ""
        if node.interfaces:
            interfaces = " implements"
            for i, interface in enumerate(node.interfaces):
                if i != 0:
                    interfaces += " &"

                interfaces += " "
                interfaces += interface.name

        if not node.ast_node:
            raise RuntimeError(f"Type '{name}' has no AST node, so cannot be parsed")

        directives = ""
        all_directives = list(node.ast_node.directives)
        for ast_node in node.extension_ast_nodes:
            all_directives.extend(ast_node.directives)

        if all_directives:
            directives = _unparse_directives(all_directives)

        children = []
        for field_name, field in node.fields.items():
            obj = self._parse_type_field(field_name, field)
            children.append(obj)

        children.sort(key=operator.attrgetter("line"))
        description = node.description
        signature = f"{name}{interfaces}{directives}"
        line = _get_source_line(node)
        return GraphQLType(children, description, signature, line)

    def _parse_scalartype(self, node: graphql.type.GraphQLScalarType) -> GraphQLScalar:
        name = node.name

        if not node.ast_node:
            raise RuntimeError(f"Scalar '{name}' has no AST node, so cannot be parsed")

        directives = ""
        all_directives = list(node.ast_node.directives)
        for ast_node in node.extension_ast_nodes:
            all_directives.extend(ast_node.directives)

        if all_directives:
            directives = _unparse_directives(all_directives)

        description = node.description
        signature = f"{name}{directives}"
        line = _get_source_line(node)
        return GraphQLScalar(description, signature, line)

    def _parse_schema(self, node: graphql.type.GraphQLSchema) -> GraphQLSchema:
        directives = ""
        all_directives = list(node.ast_node.directives) if node.ast_node else []
        for ast_node in node.extension_ast_nodes:
            all_directives.extend(ast_node.directives)

        if all_directives:
            directives = _unparse_directives(all_directives).lstrip()

        children: list[SchemaChildTypes] = []
        for type_name, type_ in node.type_map.items():
            if type_name in self._DEFAULT_TYPES or type_name.startswith("__"):
                continue

            child_type = self._parse_named_type(type_)
            children.append(child_type)

        for directive in node.directives:
            # Don't document the default directives
            if not directive.ast_node:
                continue

            child_directive = self._parse_directive(directive)
            children.append(child_directive)

        children.sort(key=operator.attrgetter("line"))
        description = node.description
        signature = f"{directives}"
        schema = GraphQLSchema(children, description, signature)

        if node.query_type:
            schema.query_type = node.query_type.name
        if node.mutation_type:
            schema.mutation_type = node.mutation_type.name
        if node.subscription_type:
            schema.subscription_type = node.subscription_type.name

        return schema

    def _parse_uniontype(self, node: graphql.type.GraphQLUnionType) -> GraphQLUnion:
        name = node.name

        if not node.ast_node:
            raise RuntimeError(f"Union '{name}' has no AST node, so cannot be parsed")

        directives = ""
        all_directives = list(node.ast_node.directives)
        for ast_node in node.extension_ast_nodes:
            all_directives.extend(ast_node.directives)

        if all_directives:
            directives = _unparse_directives(all_directives)

        types = " | ".join(type_.name for type_ in node.types)

        description = node.description
        signature = f"{name}{directives} = {types}"
        line = _get_source_line(node)
        return GraphQLUnion(description, signature, line)

    @classmethod
    def parse(cls, node: graphql.type.GraphQLSchema) -> GraphQLSchema:
        return cls()._parse_schema(node)

    @classmethod
    def parse_from_source(cls, path: StrPath, *paths: StrPath) -> GraphQLSchema:
        with open(path) as in_f:
            schema = graphql.utilities.build_schema(in_f.read())

        for extension in paths:
            with open(extension) as in_f:
                document = graphql.parse(in_f.read())

            schema = graphql.utilities.extend_schema(schema, document)

        return cls.parse(schema)
