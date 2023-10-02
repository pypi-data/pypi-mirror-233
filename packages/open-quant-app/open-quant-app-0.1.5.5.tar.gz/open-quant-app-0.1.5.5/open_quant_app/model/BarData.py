from datetime import datetime

class BarData:
    def __init__(self, stock_id: str, timestamp: datetime, close: float, strategy_id: int = 0):
        self.stock_id: str = stock_id
        self.timestamp: datetime = timestamp
        self.close: float = close
        self.strategy_id: int = strategy_id