import enum
import time
from typing import Dict, List
from datetime import datetime, timedelta

from loguru import logger
import xtquant.xtconstant as xtconstant
import xtquant.xtdata as xt_data
from xtquant.xttype import XtOrder

from open_quant_app.trade.Trader import Trader
from open_quant_app.manager.OrderManager import OrderStatus


class OrderManagerV2:
    def __init__(self, trader: Trader, strategy_id: int, stock_ids: List[str], delay: float = 1,
                 sliding_point: float = 0.0005):
        self.strategy_id: int = strategy_id
        self.trader: Trader = trader
        self.stock_ids: List[str] = stock_ids
        self.delay: float = delay
        self.sliding_point: float = sliding_point
        self.finished: Dict[int, bool] = {}

    def sync_finished_orders(self):
        for order in self.trader.query_orders():
            self.finished[order.order_id] = True

    def if_sliding_point(self, curr_price: float, ref_price: float) -> bool:
        if (abs(curr_price - ref_price) / ref_price) > self.sliding_point:
            logger.error(f"sliding point potential detected: curr = {curr_price}, ref = {ref_price}")
            return True
        else:
            return False

    def get_latest_price(self, stock_id: str) -> dict:
        # get data
        timestamp = datetime.now()
        end_timestamp = (timestamp + timedelta(minutes=1)).strftime("%Y%m%d%H%M%S")
        prev_timestamp = (timestamp + timedelta(minutes=-1)).strftime("%Y%m%d%H%M%S")
        data = xt_data.get_market_data(field_list=['askPrice', 'bidPrice'],
                                       stock_list=[stock_id], period='tick', count=1,
                                       start_time=prev_timestamp, end_time=end_timestamp,
                                       dividend_type='front', fill_data=True)
        # subtract price
        ask_price = data[stock_id]['askPrice'][-1][0] if len(data[stock_id]['askPrice']) != 0 else -1
        bid_price = data[stock_id]['bidPrice'][-1][0] if len(data[stock_id]['bidPrice']) != 0 else -1

        if ask_price == -1 or bid_price == -1:
            logger.critical(f"0 value detected in OrderManagerV2: ask price or bid price")
            return None

        return {
            "ask_price": ask_price,
            "bid_price": bid_price,
        }

    def handle_once(self, order_id: int):
        pass

    def handle(self):
        pass

    def detect(self) -> List[int]:
        pass