from __future__ import annotations

from typing import Generic, TypeVar

ValueT_co = TypeVar("ValueT_co", covariant=True)

__all__ = ["SecretValue"]


class SecretValue(Generic[ValueT_co]):  # noqa: D101
    _secret_value: ValueT_co

    def __init__(self, value: ValueT_co) -> None:
        self._secret_value = value

    def __repr__(self) -> str:
        return "*******"

    def __str__(self) -> str:
        return "*******"

    def get_value(self) -> ValueT_co:  # noqa: D102
        return self._secret_value
