"""Input validation — all validation lives here, nowhere else."""

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


class ValidationError(ValueError):
    pass


def validate_symbol(value: str) -> str:
    s = value.strip().upper()
    if not s.isalnum():
        raise ValidationError(
            f"Invalid symbol '{value}'. Use alphanumeric only, e.g. BTCUSDT."
        )
    return s


def validate_side(value: str) -> str:
    s = value.strip().upper()
    if s not in VALID_SIDES:
        raise ValidationError(
            f"Invalid side '{value}'. Must be BUY or SELL."
        )
    return s


def validate_order_type(value: str) -> str:
    ot = value.strip().upper()
    if ot not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{value}'. Choose: MARKET, LIMIT, STOP_MARKET."
        )
    return ot


def validate_quantity(value) -> float:
    try:
        q = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"Quantity '{value}' is not a valid number.")
    if q <= 0:
        raise ValidationError(f"Quantity must be > 0, got {q}.")
    return q


def validate_price(value, order_type: str):
    if order_type == "LIMIT":
        if value is None:
            raise ValidationError("--price is required for LIMIT orders.")
        try:
            p = float(value)
        except (TypeError, ValueError):
            raise ValidationError(f"Price '{value}' is not a valid number.")
        if p <= 0:
            raise ValidationError(f"Price must be > 0, got {p}.")
        return p
    return None


def validate_stop_price(value, order_type: str):
    if order_type == "STOP_MARKET":
        if value is None:
            raise ValidationError("--stop-price is required for STOP_MARKET orders.")
        try:
            sp = float(value)
        except (TypeError, ValueError):
            raise ValidationError(f"Stop price '{value}' is not a valid number.")
        if sp <= 0:
            raise ValidationError(f"Stop price must be > 0, got {sp}.")
        return sp
    return None
