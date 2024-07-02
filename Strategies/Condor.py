from datetime import time
from typing import Optional, List

from Data.OptionData import OptionData
from Data.OptionType import OptionType
from Strategies.Trade import Trade


class Condor:

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
        self.call_strike = 0
        self.put_strike = 0
        self.historicalPnl: List[float] = []

    def reset(self, option_data, spy_open):
        if self.pnl is not None:
            self.historicalPnl.append(self.pnl)
        self.option_data = option_data
        self.call_strike = round(spy_open * (1 + self.pct_otm / 100))
        self.put_strike = round(spy_open * (1 - self.pct_otm / 100))
        self.positions = []
        self.pnl = 0

    def check_entry(self, curr_time: time):
        # Only enter on market open
        if curr_time.hour != 9 or curr_time.minute != 30:
            return

        # Get prices
        short_call_price = self.option_data.get_price(OptionType.CALL, self.call_strike, curr_time)
        long_call_price = self.option_data.get_price(OptionType.CALL, self.call_strike+1, curr_time)
        short_put_price = self.option_data.get_price(OptionType.PUT, self.put_strike, curr_time)
        long_put_price = self.option_data.get_price(OptionType.PUT, self.put_strike-1, curr_time)
        if short_call_price is None or long_call_price is None or short_put_price is None or long_put_price is None:
            # Not enough liquidity to enter
            return

        # Enter trade
        self.positions.append(Trade(curr_time, -1, self.call_strike, OptionType.CALL, short_call_price))
        self.positions.append(Trade(curr_time, 1, self.call_strike+1, OptionType.CALL, long_call_price))
        self.positions.append(Trade(curr_time, -1, self.put_strike, OptionType.PUT, short_put_price))
        self.positions.append(Trade(curr_time, 1, self.put_strike-1, OptionType.PUT, long_put_price))

    def compute_curr_pnl_pct(self, curr_time: time) -> Optional[float]:
        initial_net_cost = 0
        curr_val = 0
        for pos in self.positions:
            # Get curr price
            price = self.option_data.get_price(pos.option_type, pos.strike, curr_time)
            if price is None:
                return None
            curr_val += price * pos.position * 100
            initial_net_cost += pos.price * pos.position * 100
        if initial_net_cost == 0:
            return 1000
        pnl_pct = ((curr_val - initial_net_cost) / abs(initial_net_cost)) * 100
        return pnl_pct

    def close_strategy(self, curr_time: time):
        for pos in self.positions:
            # Get curr price
            price = self.option_data.get_price(pos.option_type, pos.strike, curr_time)
            if price is None:
                # Not enough liquidity to close
                #     self.pnl -= pos.position * pos.price * 100
                #     print(f"\t{pos.option_type}\t{pos.position}\t{pos.strike}\t{pos.price}\tN/A")
                continue
            self.pnl += (pos.position * price * 100) - (pos.position * pos.price * 100)
            # print(f"\t{pos.option_type}\t{pos.position}\t{pos.strike}\t{pos.price}\t{price}")
        self.positions = []
        # print(f"\tpnl: {self.pnl}")

    def check_exit(self, curr_time: time):
        if curr_time.hour == 16 and curr_time.minute == 00:
            # Last candle of trading, close position
            # print("\t Market close")
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
