from dataclasses import Field, MISSING
from typing import Any


def get_default(field: Field, default=None) -> Any:
    if field.default_factory and field.default_factory != MISSING:
        return field.default_factory()
    if field.default and field.default != MISSING:
        return field.default
    return default
