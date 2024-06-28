import datetime
import DateUtil
import RequestUtil


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
            date = DateUtil.unix_to_date(candle['time'])
            spyc = SPYCandle(candle)
            self.data[date] = spyc

    def __init__(self, days: int):
        self.data: dict[datetime.date, SPYCandle] = {}
        self.get_data(days)

    def get_market_days(self) -> list[datetime.date]:
        return list(self.data.keys())


class SPYCandle:

    def __init__(self, json: dict):
        self.open = json['open']
        self.high = json['high']
        self.low = json['low']
        self.close = json['close']