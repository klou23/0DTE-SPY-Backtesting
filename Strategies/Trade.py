from dataclasses import dataclass
from datetime import time
from Data.OptionType import OptionType


@dataclass
class Trade:
    timestamp: time
    position: int
    strike: int
    option_type: OptionType
    price: float
