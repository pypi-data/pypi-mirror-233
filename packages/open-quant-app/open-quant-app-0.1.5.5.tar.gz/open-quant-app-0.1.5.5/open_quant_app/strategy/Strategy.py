from datetime import datetime
import time
from typing import List, Dict

import xtquant.xtdata as xtdata
from open_quant_app.trade.Trader import Trader
from open_quant_app.utils.FixedQueue import FixedQueue
from open_quant_app.manager.OrderManager import OrderManager
from open_quant_app.utils.TimeUtils import TimeUtils
from open_quant_app.model.BarData import BarData

from loguru import logger


class StrategyData:
    def __init__(self, strategy_id: int = 0, timestamp: datetime = datetime.now()):
        self.strategy_id: int = strategy_id
        self.timestamp: datetime = timestamp

    def empty(self) -> bool:
        return False


class Strategy:
    def __init__(self, strategy_id: int, trader: Trader, config: dict = None):
        self.strategy_id: int = strategy_id
        self.trader: Trader = trader
        self.stock_ids: [str] = config['stock']['stock_ids'][self.strategy_id]
        self.period: float = config['strategy']['periods']
        self.order_manager: OrderManager = OrderManager(trader, self.stock_ids)
        self.records: FixedQueue[StrategyData] = FixedQueue(config['ui']['record_length'])

    def subscribe_quotes(self, period_list: [str]):
        for stock_id in self.stock_ids:
            for period in period_list:
                xtdata.subscribe_quote(stock_id, period=period, callback=self.on_data_callback)

    def on_data_callback(self, data_cbk):
        pass

    def get_bar_data(self) -> Dict[str, BarData]:
        return {}

    def exec(self, timestamp: datetime = None) -> StrategyData:
        return StrategyData()

    def exec_before(self, timestamp: datetime = datetime.now()):
        pass

    def exec_after(self, timestamp: datetime = datetime.now()):
        pass

    def main_loop(self):
        self.exec_before()
        timestamp = datetime.now()
        while not TimeUtils.after_afternoon_end(timestamp):
            if TimeUtils.judge_trade_time(timestamp):
                record = self.exec(timestamp)
                if not record.empty():
                    self.records.append(record)
            else:
                logger.warning(f"curr timestamp =  {timestamp} not in trade time!")
            time.sleep(self.period)
        self.exec_after()

    def main_loop_back(self, start: datetime, end: datetime = datetime.now()):
        self.trader.back_tester.set_time_seg(start, end)
        curr_timestamp = start
        while curr_timestamp < end:
            record = self.exec(curr_timestamp)
            if not record.empty():
                self.records.append(record)
            # record asset
            self.trader.back_tester.record_assets(curr_timestamp)
            # record bar data
            bar_data_dict = self.get_bar_data()
            for stock_id in bar_data_dict:
                self.trader.back_tester.record_bar_data(bar_data_dict[stock_id])

            curr_timestamp = TimeUtils.next_trade_timestamp(curr_timestamp, self.period)
        self.trader.back_tester.report(self.strategy_id, save_as_file=True)
