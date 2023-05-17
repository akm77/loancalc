from enum import Enum


class CalculatorForm(str, Enum):
    SELECT_LEASE_PERIOD = "cf00"
    SELECT_MARKET = "cf01"
    AMOUNT_COUNTER = "cf02"
    ENTER_AMOUNT = "cf03"
    LOAN_MONTH_COUNTER = "cf04"
    INTEREST_RATE_COUNTER = "cf05"

    def __str__(self) -> str:
        return str.__str__(self)
