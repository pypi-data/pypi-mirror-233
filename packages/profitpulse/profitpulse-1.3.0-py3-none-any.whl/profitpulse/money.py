from __future__ import annotations


class Money:
    def __init__(self, cents: int) -> None:
        self._cents = cents

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Money):
            return False
        return self._cents == __value._cents

    def __str__(self) -> str:
        return f"{self._cents / 100:.2f}"

    def __repr__(self) -> str:
        return f"Money({self._cents})"

    def __add__(self, other: Money) -> Money:
        return Money(self._cents + other._cents)

    @property
    def cents(self) -> int:
        return self._cents
