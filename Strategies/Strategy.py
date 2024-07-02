from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import time

from Data.OptionData import OptionData
from Strategies.Trade import Trade


class Strategy(ABC):

    def __init__(self):
        self.option_data: Optional[OptionData] = None
        self.positions: List[Trade] = []
        self.pnl_history: List[float] = []
        self.net_cost_history: List[float] = []
        self.params: dict = {}
        self.daily_params: dict = {}
        self.pnl: Optional[float] = None
        self.net_cost: Optional[float] = None

    def setup(self, params: dict):
        self.params = params

    def day_reset(self, option_data: OptionData, daily_params: dict):
        if len(self.positions) > 0:
            print("Not all positions closed, should not day_reset")

        if self.pnl is not None:
            self.pnl_history.append(self.pnl)
        if self.net_cost is not None:
            self.net_cost_history.append(self.pnl)

        self.option_data = option_data
        self.positions = []
        self.pnl = 0
        self.net_cost = 0
        self.daily_params = daily_params

    def compute_curr_pnl_pct(self, curr_time: time) -> Optional[float]:
        initial_net_cost = 0
        curr_val = 0
        for pos in self.positions:
            price = self.option_data.get_price(pos.option_type, pos.strike, curr_time)
            if price is None:
                # No trade price, can't compute pnl accurately
                return None
            curr_val += price * pos.position * 100
            initial_net_cost += pos.price * pos.position * 100
        if initial_net_cost == 0:
            return 0
        return (curr_val-initial_net_cost) / abs(initial_net_cost) * 100

    def close_leg(self, idx: int, curr_time: time):
        pos = self.positions[idx]
        price = self.option_data.get_price(pos.option_type, pos.strike, curr_time)
        if price is None:
            # Not enough liquidity to close
            return
        self.pnl += (pos.position * price * 100) - (pos.position * pos.price * 100)
        self.net_cost += pos.position * pos.price * 100
        self.positions.pop(idx)

    def close_all(self, curr_time: time):
        left = []

        for pos in self.positions:
            price = self.option_data.get_price(pos.option_type, pos.strike, curr_time)
            if price is None:
                # Not enough liquidity to close
                left.append(pos)
                continue
            self.pnl += (pos.position * price * 100) - (pos.position * pos.price * 100)
            self.net_cost += pos.position * pos.price * 100
            self.pnl -= 0.13    # Fees

        self.positions = left

    @abstractmethod
    def run_strategy(self, curr_time: time):
        pass
