"""Money helpers. House rule: amounts arrive as decimal strings and are converted to integer minor
units with banker's rounding (ROUND_HALF_EVEN) at the currency exponent. Floats are never used."""
from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation

CURRENCY_EXPONENT = {"USD": 2, "UGX": 0}
ROUNDING = ROUND_HALF_EVEN


def to_minor(amount: str, currency: str) -> int:
    if not isinstance(amount, str):
        raise TypeError("amount must be a decimal string, never a float")
    if currency not in CURRENCY_EXPONENT:
        raise ValueError(f"unsupported currency {currency!r}")
    try:
        value = Decimal(amount.strip())
    except InvalidOperation as exc:
        raise ValueError(f"invalid amount {amount!r}") from exc
    if not value.is_finite():
        raise ValueError(f"invalid amount {amount!r}")
    exponent = CURRENCY_EXPONENT[currency]
    quantum = Decimal(1).scaleb(-exponent)
    return int(value.quantize(quantum, rounding=ROUNDING).scaleb(exponent))
