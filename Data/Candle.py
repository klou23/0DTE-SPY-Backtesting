from dataclasses import dataclass


class Candle:
    def __init__(self, json=None, val=None):
        if json is None:
            self.open = val
            self.high = val
            self.low = val
            self.close = val
        if val is None:
            self.open = json['open']
            self.high = json['high']
            self.low = json['low']
            self.close = json['close']

