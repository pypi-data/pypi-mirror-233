import jinja2
import sphinx.util.logging

from ._objects import GraphQLObject

LOGGER = sphinx.util.logging.getLogger(__name__)


class JinjaRenderer:
    def __init__(self) -> None:
        self.env = jinja2.Environment(
            loader=jinja2.PackageLoader("autogqlschema", "_templates"),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, node: GraphQLObject) -> str:
        LOGGER.log("VERBOSE", "Rendering %s", node.signature)

        template = self.env.get_template(f"{node.type}.rst.jinja")
        ctx = node.get_context_data()
        ctx["renderer"] = self
        return template.render(**ctx)
