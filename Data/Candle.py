from dataclasses import dataclass


class Candle:
    def __init__(self, json: dict):
        self.open = json['open']
        self.high = json['high']
        self.low = json['low']
        self.close = json['close']
