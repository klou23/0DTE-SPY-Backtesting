from datetime import time, datetime, timedelta
from Data.OptionData import OptionData
from Data.SPYData import SPYData


class BacktestEngine:
    def __init__(self, days, strategies):
        self.spy_data = SPYData(days)
        self.strategies = strategies

    def run(self):
        for market_day in self.spy_data.get_market_days():
            print(f"Simulating: {market_day}")
            option_data = OptionData(market_day, self.spy_data.get_close_price(market_day))
            for strategy in self.strategies:
                strategy.reset(option_data, self.spy_data.get_open_price(market_day))

            start_time = time(9, 30)
            end_time = time(16, 00)

            curr_datetime = datetime.combine(datetime.today(), start_time)
            end_datetime = datetime.combine(datetime.today(), end_time)

            while curr_datetime <= end_datetime:
                for strategy in self.strategies:
                    strategy.run_strategy(curr_datetime.time())
                curr_datetime += timedelta(minutes=5)
