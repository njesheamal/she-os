# app/database/constraints.py
from enum import StrEnum


def status_in(enum_cls: type[StrEnum]) -> str:
    values = ", ".join(f"'{member.value}'" for member in enum_cls)
    return f"status IN ({values})"
