import datetime
from Utils import RequestUtil, TimeUtil
from Data.Candle import Candle


class SPYData:

    def get_data(self, days: int):
        curr_date = datetime.date.today()
        start_date = curr_date - datetime.timedelta(days=days+1)
        end_date = curr_date - datetime.timedelta(days=1)
        from_time: str = start_date.strftime('%Y%m%d')
        to_time: str = end_date.strftime('%Y%m%d')
        candle_list = RequestUtil.request({
            'events': 'Candle',
            'symbols': 'SPY{=d}',
            'fromTime': from_time,
            'toTime': to_time,
            'timeout': 60
        })['Candle']['SPY{=d}']
        for candle in candle_list:
            date = TimeUtil.unix_to_date(candle['time'])
            spyc = Candle(candle)
            self.data[date] = spyc

    def __init__(self, days: int):
        self.data: dict[datetime.date, Candle] = {}
        self.get_data(days)

    def get_market_days(self) -> list[datetime.date]:
        return list(self.data.keys())

    def get_open_price(self, day: datetime.date) -> float:
        return self.data[day].open

    def get_close_price(self, day: datetime.date) -> float:
        return self.data[day].close
