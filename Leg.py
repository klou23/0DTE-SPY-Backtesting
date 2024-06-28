from enum import Enum
from typing import Optional


class OptionType(Enum):
    CALL = 1
    PUT = 2


class Position(Enum):
    LONG = 1
    SHORT = 2


class Leg:

    def __init__(self, option_type: OptionType, strike: float, position: Position, open_fee: float, close_fee):
        self.open_price: Optional[float] = None
        self.close_price: Optional[float] = None
        self.option_type: OptionType = option_type
        self.strike: float = strike
        self.position: Position = position
        self.open_fee: float = open_fee
        self.close_fee: float = close_fee

    def open(self, price: float):
        if self.position == Position.LONG:
            self.open_price = -price
        else:
            self.open_price = price

    def curr_pnl(self, price: float) -> float:
        if self.position == Position.LONG:
            liq_val = price
        else:
            liq_val = -price
        return liq_val + self.open_price

    def close(self, price: float):
        if self.position == Position.LONG:
            self.close_price = price
        else:
            self.close_price = -price

    def pnl(self):
        return self.open_price + self.close_price
