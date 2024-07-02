from datetime import time
from typing import Optional, List

from Data.OptionData import OptionData
from Data.OptionType import OptionType
from Strategies.Trade import Trade


class LongCallStrategy:

    def __init__(self,
                 pct_otm: float,
                 profit_target_pct: float,
                 stop_loss_pct: float):
        self.pct_otm = pct_otm
        self.profit_target_pct = profit_target_pct
        self.stop_loss_pct = stop_loss_pct
        self.option_data: Optional[OptionData] = None
        self.positions: List[Trade] = []
        self.pnl = None
        self.strike = 0
        self.historicalPnl: List[float] = []

    def reset(self, option_data, spy_open):
        if self.pnl is not None:
            self.historicalPnl.append(self.pnl)
        self.option_data = option_data
        self.strike = round(spy_open * (1+self.pct_otm/100))
        self.positions = []
        self.pnl = 0

    def check_entry(self, curr_time: time):
        # Only enter on market open
        if curr_time.hour != 9 or curr_time.minute != 30:
            return

        # Get price
        price = self.option_data.get_price(OptionType.CALL, self.strike, curr_time)
        if price is None:
            # Not enough liquidity to enter
            return
        # Enter trade
        self.positions.append(Trade(curr_time, 1, self.strike, OptionType.CALL, price))

    def compute_curr_pnl_pct(self, curr_time: time) -> Optional[float]:
        initial_net_cost = 0
        curr_val = 0
        for pos in self.positions:
            # Get curr price
            price = self.option_data.get_price(pos.option_type, pos.strike, curr_time)
            if price is None:
                return None
            curr_val += price * pos.position * 100
            curr_val -= 0.13        # Fees
            initial_net_cost += pos.price * pos.position * 100
        pnl_pct = ((curr_val-initial_net_cost + self.pnl)/abs(initial_net_cost))*100
        return pnl_pct

    def close_strategy(self, curr_time: time):
        for pos in self.positions:
            # Get curr price
            price = self.option_data.get_price(pos.option_type, pos.strike, curr_time)
            if price is None:
                # Not enough liquidity to close
                continue
            self.pnl += (pos.position * price * 100) - (pos.position * pos.price * 100)
        self.positions = []
        # print(self.pnl)

    def check_exit(self, curr_time: time):
        if curr_time.hour == 16 and curr_time.minute == 00:
            # Last candle of trading, close position
            self.close_strategy(curr_time)
            return

        curr_pnl_pct = self.compute_curr_pnl_pct(curr_time)
        if curr_pnl_pct is None:
            return
        if curr_pnl_pct >= self.profit_target_pct or curr_pnl_pct <= -self.stop_loss_pct:
            self.close_strategy(curr_time)

    def run_strategy(self, curr_time: time):
        if len(self.positions) == 0:
            self.check_entry(curr_time)
        else:
            self.check_exit(curr_time)
