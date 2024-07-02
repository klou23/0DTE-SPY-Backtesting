from datetime import time

from Data.OptionType import OptionType
from Strategies.Strategy import Strategy
from Strategies.Trade import Trade


class LongCallStrat(Strategy):
    """
    Params:
        pct_otm: <float> Percentage OTM to buy call
        profit_target_pct: <float> Take profit percentage
        stop_loss_pct: <float> Stop loss percentage
        open_time: <time> Time to open position
        close_time: <time> Time to close position regardless of pnl
    Daily params:
        spy_open: <float> Opening price of SPY
    """

    def check_entry(self, curr_time: time):
        # Only enter at open_time
        if curr_time != self.params['open_time']:
            return

        # Get option data
        strike = round(self.daily_params['spy_open'] * (1+self.params['pct_otm']/100))
        price = self.option_data.get_price(OptionType.CALL, strike, curr_time)
        if price is None:
            # Not enough liquidity to enter
            return

        # Enter position
        self.positions.append(Trade(curr_time, 1, strike, OptionType.CALL, price))
        self.pnl -= 1.13    # Commissions + Fees

    def check_exit(self, curr_time: time):
        if curr_time >= self.params['close_time']:
            # Attempt to close everything
            self.close_all(curr_time)
            return

        curr_pnl_pct = self.compute_curr_pnl_pct(curr_time)
        if curr_pnl_pct is None:
            return
        if curr_pnl_pct >= self.params['profit_target_pct'] or curr_pnl_pct <= -self.params['stop_loss_pct']:
            self.close_all(curr_time)

    def run_strategy(self, curr_time: time):
        if len(self.positions) == 0:
            self.check_entry(curr_time)
        else:
            self.check_exit(curr_time)