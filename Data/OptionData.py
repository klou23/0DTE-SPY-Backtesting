from datetime import time, date
from typing import Optional

from Data.Candle import Candle
from Data.OptionType import OptionType
from Utils import RequestUtil, TimeUtil


class OptionData:
    """
    Used for option data for a single day
    """

    def __init__(self, query_date: date):
        self.candle_data: dict[OptionType, dict[int, dict[time, Candle]]] = {
            OptionType.CALL: {},
            OptionType.PUT: {}
        }
        self.from_time = query_date.strftime("%Y%m%d")
        self.symbol = f'.SPY{query_date.strftime("%y%m%d")}'

    def load_data(self, option_type: OptionType, strike: int):
        full_symbol = f'{self.symbol}{option_type.value}{strike}{{=5m}}'
        candle_list = RequestUtil.request({
            'events': 'Candle',
            'symbols': full_symbol,
            'fromTime': self.from_time,
            'timeout': 60
        })['Candle'][full_symbol]
        self.candle_data[option_type][strike] = {}
        for candle in candle_list:
            candle_time = TimeUtil.unix_to_time(candle['time'])
            self.candle_data[option_type][strike][candle_time] = Candle(candle)

    def get_price(self, option_type: OptionType, strike: int, query_time: time) -> Optional[float]:
        if strike not in self.candle_data[option_type]:
            self.load_data(option_type, strike)

        if query_time not in self.candle_data[option_type][strike]:
            return None

        return self.candle_data[option_type][strike][query_time].open
