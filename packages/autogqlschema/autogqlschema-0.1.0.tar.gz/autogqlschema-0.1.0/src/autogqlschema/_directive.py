from __future__ import annotations

import pathlib
import typing

from docutils import nodes
from docutils.nodes import Node
from docutils.parsers.rst import directives
from docutils.parsers.rst.states import RSTState
from docutils.statemachine import StringList
from sphinx.util.docutils import SphinxDirective, switch_source_input

if typing.TYPE_CHECKING:
    from _typeshed import StrPath

from ._parser import Parser
from ._renderer import JinjaRenderer


def validate_source_files(
    source_files: list[str], confdir: StrPath
) -> list[pathlib.Path]:
    result = []

    path = pathlib.Path(confdir)
    for pattern in source_files:
        for source_file in path.glob(pattern):
            result.append(source_file)

    return result


def parse_generated_content(state: RSTState, content: StringList) -> list[Node]:
    with switch_source_input(state, content):
        node = nodes.paragraph()
        node.document = state.document
        state.nested_parse(content, 0, node)

        return node.children


def csv_required(argument: str | None) -> list[str]:
    """Return the argument text split by commas.

    Raises:
        ValueError: If no argument is found.
    """
    if argument is None:
        raise ValueError("argument required but none supplied")

    entries = []
    for entry in argument.split(","):
        entry = entry.strip()
        if not entry:
            continue

        entries.append(entry)

    if not entries:
        raise ValueError("argument contains no entries")

    return entries


class AutoGQLSchemaDirective(SphinxDirective):
    has_content = False
    optional_arguments = 1
    option_spec = {
        "debug": directives.flag,
        "root-dir": directives.unchanged,
        "source-files": csv_required,
    }

    def run(self) -> list[Node]:
        root_dir = self.options.get("root-dir")
        if root_dir:
            root_dir = pathlib.Path(root_dir)
            if not root_dir.is_absolute:
                root_dir = pathlib.Path(self.env.app.confdir) / root_dir
        else:
            root_dir = self.env.app.confdir

        source_files = validate_source_files(self.options["source-files"], root_dir)
        schema = Parser.parse_from_source(*source_files)
        schema.name = self.arguments[0] if self.arguments else "__gqlschema__"

        renderer = JinjaRenderer()
        rst_source = renderer.render(schema)

        if "debug" in self.options:
            debug_path = pathlib.Path(self.env.app.outdir) / f"{schema.name}.rst"
            with (debug_path).open("w") as out_f:
                out_f.write(rst_source)

        result = parse_generated_content(
            self.state, StringList(rst_source.splitlines())
        )
        return result
