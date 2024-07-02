from datetime import time, date
from typing import Optional

from Data.Candle import Candle
from Data.OptionType import OptionType
from Utils import RequestUtil, TimeUtil


class OptionData:
    """
    Used for option data for a single day
    """

    def __init__(self, query_date: date, spy_close: float):
        self.candle_data: dict[OptionType, dict[int, dict[time, Candle]]] = {
            OptionType.CALL: {},
            OptionType.PUT: {}
        }
        self.from_time = query_date.strftime("%Y%m%d")
        self.symbol = f'.SPY{query_date.strftime("%y%m%d")}'
        self.spy_close = spy_close

    def load_data(self, option_type: OptionType, strike: int):
        full_symbol = f'{self.symbol}{option_type.value}{strike}{{=5m}}'
        response = RequestUtil.request({
            'events': 'Candle',
            'symbols': full_symbol,
            'fromTime': self.from_time,
            'timeout': 60
        })
        self.candle_data[option_type][strike] = {}
        if 'Candle' in response:
            candle_list = response['Candle'][full_symbol]
            for candle in candle_list:
                candle_time = TimeUtil.unix_to_time(candle['time'])
                self.candle_data[option_type][strike][candle_time] = Candle(candle)
        # Market close candle, intrinsic value
        if option_type == OptionType.CALL:
            val = max(0.0, self.spy_close-strike)
            self.candle_data[option_type][strike][time(hour=16, minute=0)] = Candle(val=val)

    def get_price(self, option_type: OptionType, strike: int, query_time: time) -> Optional[float]:
        if strike not in self.candle_data[option_type]:
            self.load_data(option_type, strike)

        if query_time not in self.candle_data[option_type][strike]:
            return None

        return self.candle_data[option_type][strike][query_time].open