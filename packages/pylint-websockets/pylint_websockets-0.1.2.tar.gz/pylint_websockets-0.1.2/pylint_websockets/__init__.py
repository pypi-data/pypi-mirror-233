"""A Pylint plugin for the Python websockets library"""
import inspect

import astroid
import websockets

__version__ = "0.1.2"


def register(_) -> None:
    """Needed for registering the plugin."""


def websockets_transform():
    module = astroid.parse(inspect.getsource(websockets))
    # fmt: off
    lazy_aliases = dict(
    	module
        .body[-1]
        .value  # Lazy load func call
        .keywords[0]  # 'aliases' argument
        .value  # The dict
        .items  # The [(key, value)...] stuff
    )
    # fmt: on
    output = "from .version import version as __version__  # noqa\n"

    output += f"__all__ = {[elt.value for elt in module.body[-2].value.elts]}\n"
    for name, path in lazy_aliases.items():
        output += f"from {path.value} import {name.value}\n"
    return astroid.parse(output)


astroid.register_module_extender(astroid.MANAGER, "websockets", websockets_transform)
