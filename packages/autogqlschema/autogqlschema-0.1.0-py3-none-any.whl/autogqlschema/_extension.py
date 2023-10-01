from __future__ import annotations

import sphinx.application
import sphinx.util.logging

from ._directive import AutoGQLSchemaDirective

LOGGER = sphinx.util.logging.getLogger(__name__)


def setup(app: sphinx.application.Sphinx) -> dict[str, bool]:
    app.setup_extension("graphqldomain")
    app.add_directive("autogqlschema", AutoGQLSchemaDirective)

    return {
        "parallel_read_safe": True,
    }
