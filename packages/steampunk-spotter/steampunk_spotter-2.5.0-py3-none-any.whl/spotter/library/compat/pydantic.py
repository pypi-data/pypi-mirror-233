"""Pydantic compatibility shims."""

from typing import Any

try:
    from pydantic_core import to_jsonable_python

    def compat_to_jsonable_python(value: Any) -> Any:
        """Compat shim."""
        return to_jsonable_python(value)

except ImportError:
    from pydantic.json import pydantic_encoder

    def compat_to_jsonable_python(value: Any) -> Any:
        """Compat shim."""
        return pydantic_encoder(value)
