import enum
from typing import List
import math

from open_quant_app.manager.PositionManager import PositionManager
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount, XtOrder, XtAsset, XtPosition, XtTrade
from xtquant import xtconstant
from open_quant_app.trade.CommonTradeCallback import CommonXtQuantTraderCallback
from open_quant_app.backtest.BackTester import BackTester
from open_quant_app.utils.OrderFilter import OrderFilter
from open_quant_app.utils.LogUtils import LogUtils

from loguru import logger
import numpy as np


class TradeMode(enum.Enum):
    MARKET = 1
    BACKTEST = 2


class Trader:
    def __init__(self, config: dict = None, mode: TradeMode = TradeMode.MARKET, cash: float = 100000):
        self.env_path = config['trade']['env_path']
        self.session_id = config['trade']['session_id']
        self.account_id = config['trade']['account_id']
        self.stock_ids = config['stock']['stock_ids']
        self.max_cash = config['assets']['max_cash']
        self.mode = mode

        self.xt_trader = XtQuantTrader(self.env_path, self.session_id)
        self.account = StockAccount(self.account_id)
        self.callback = CommonXtQuantTraderCallback()
        self.back_tester = BackTester(config, cash)
        self.position_manager = PositionManager(config)
        self.log_utils = LogUtils(config)

    def start(self):
        # start trade thread
        self.xt_trader.start()
        connection_result = self.xt_trader.connect()
        if connection_result != 0:
            logger.error("connect to QMT MINI failed !")
        else:
            logger.success("connect to QMT MINI success !")
        # subscribe trade acc
        subscribe_result = self.xt_trader.subscribe(self.account)
        if subscribe_result != 0:
            logger.error(f"subscribe to account id = {self.account_id} failed !")
        else:
            logger.success(f"subscribe to account id = {self.account_id} success !")

    def info(self):
        logger.info("begin checking basic status")
        if self.mode == TradeMode.MARKET:
            # check assets
            asset = self.query_stock_asset()
            logger.info("you are in MARKET MODE")
            logger.info(f"account id: {asset.account_id}")
            logger.info(f"total asset: {asset.total_asset}")
            logger.info(f"cash: {asset.cash}")
            logger.info(f"market value: {asset.market_value}")
            logger.info(f"frozen cash: {asset.frozen_cash}")
        elif self.mode == TradeMode.BACKTEST:
            logger.info("you are in BACKTEST MODE")
            self.back_tester.info()

    def order_stock(self, stock_id: str, order_type: int, volume: int, price: float, strategy_id: int,
                    price_type: int = xtconstant.FIX_PRICE, strategy_name: str = '', comment: str = '') -> int:
        if volume == 0:
            return 0
        order_id = -1
        if self.mode == TradeMode.MARKET:
            self.log_utils.log(f"stock_id={stock_id}, strategy_id={strategy_id}, vol={volume}, price={price}, "
                               f"type={'buy' if order_type == xtconstant.STOCK_BUY else 'sell'}, "
                               f"check={self.can_buy(volume, price, strategy_id) if order_type == xtconstant.STOCK_BUY else self.can_sell(stock_id, volume, strategy_id)}, "
                               f"reason={self.get_reason_can_sell(stock_id, volume) if order_type == xtconstant.STOCK_SELL else self.get_reason_can_buy(volume, price, strategy_id)}")

            if order_type == xtconstant.STOCK_BUY and self.can_buy(volume, price, strategy_id):
                order_id = self.xt_trader.order_stock(self.account, stock_id, order_type, volume
                                                      , price_type, price, strategy_name, comment)
            elif order_type == xtconstant.STOCK_SELL and self.can_sell(stock_id, volume, strategy_id):
                order_id = self.xt_trader.order_stock(self.account, stock_id, order_type, volume
                                                      , price_type, price, strategy_name, comment)
        elif self.mode == TradeMode.BACKTEST:
            order_id = self.back_tester.order_stock(stock_id, order_type, volume, price, strategy_id)
        if order_id != -1:
            logger.success(
                f"trading: {'buy' if order_type == xtconstant.STOCK_BUY else 'sell'} {stock_id} volume = {volume}"
                f", price = {price}")
        return order_id

    def cancel_order_stock(self, order_id: int) -> int:
        ret = self.xt_trader.cancel_order_stock(self.account, order_id)
        if ret != 0:
            print(f"Err: cancel order id = {order_id} failed !")
        return ret

    def clear_position(self, stock_id: str, price: float, strategy_id: int) -> int:
        if self.mode == TradeMode.MARKET:
            # TODO: FINISH THIS FEAT
            return -1
        elif self.mode == TradeMode.BACKTEST:
            total_volume = self.back_tester.query_position(stock_id)
            return self.back_tester.order_stock(stock_id, xtconstant.STOCK_SELL, total_volume, price, strategy_id)

    def query_orders(self) -> List[XtOrder]:
        orders = self.xt_trader.query_stock_orders(self.account)
        return orders

    def query_order_by_id(self, order_id) -> XtOrder:
        order = self.xt_trader.query_stock_order(self.account, order_id)
        return order

    def query_trades(self) -> List[XtTrade]:
        trades = self.xt_trader.query_stock_trades(self.account)
        return trades

    def query_positions(self) -> List[XtPosition]:
        positions = self.xt_trader.query_stock_positions(self.account)
        return positions

    def query_position_by_stock(self, stock_id: str) -> XtPosition:
        position = self.xt_trader.query_stock_position(self.account, stock_id)
        return position

    def query_stock_asset(self) -> XtAsset:
        asset = self.xt_trader.query_stock_asset(self.account)
        return asset

    def close(self):
        self.xt_trader.unsubscribe(self.account)
        self.xt_trader.stop()

    def can_sell(self, stock_id: str, volume: int, strategy_id: int) -> bool:
        position = self.query_position_by_stock(stock_id)
        if position is None:
            logger.warning(f"you have 0 position for stock {stock_id}, cannot sell !")
            return False
        elif volume > position.can_use_volume:
            logger.warning(f"position available volume = {position.can_use_volume} < sell volume {volume}, cancel !")
            return False
        else:
            return True

    def max_can_sell(self, stock_id: str, strategy_id: int, volume: int) -> int:
        can_use_vol = self.query_position_by_stock(stock_id).can_use_volume
        if self.query_position_by_stock(stock_id).can_use_volume < volume:
            logger.warning(f"cannot sell {volume}, choose max sell volume: {can_use_vol}")
            return can_use_vol
        else:
            return volume

    def get_reason_can_sell(self, stock_id: str, volume: int) -> str:
        position = self.query_position_by_stock(stock_id)
        if position is None:
            return f"None position on {stock_id}"
        elif volume > position.can_use_volume:
            return f"Not enough position of {stock_id}, vol={volume}, available={position.can_use_volume}"
        else:
            return f"can sell"

    def can_buy(self, volume: int, price: float, strategy_id: int) -> bool:
        # query position
        position_data = []
        stock_id_tuple = self.stock_ids[strategy_id]
        for stock_id in stock_id_tuple:
            position_data.append(self.query_position_by_stock(stock_id))
        # query assets
        total_assets = self.query_stock_asset().total_asset
        return not self.position_manager.is_position_limit(position_data, strategy_id, volume, price, total_assets)

    def max_can_buy(self, volume, price, strategy_id: int) -> int:
        # query position
        stock_id_tuple = self.stock_ids[strategy_id]
        position_val = 0.0
        for stock_id in stock_id_tuple:
            position = self.query_position_by_stock(stock_id)
            if position is None:
                continue
            # use open_price, because avg price may be 0
            position_val += (position.can_use_volume + position.frozen_volume) * position.open_price
        # query order
        order_val = 0.0
        orders = OrderFilter.filter(self.query_orders(), stock_id_tuple)
        orders = OrderFilter.filter_order_status(orders, [xtconstant.ORDER_CANCELED, xtconstant.ORDER_SUCCEEDED,
                                                          xtconstant.ORDER_JUNK])
        for order in orders:
            order_val += order.order_volume * order.price * (-1 if order.order_type == xtconstant.STOCK_SELL else 1)
        # query asset
        if self.query_stock_asset() is None:
            return 0
        total_asset = self.query_stock_asset().total_asset
        total_asset = min(total_asset, self.max_cash) * self.position_manager.positions[strategy_id]
        # check
        if price == 0 or volume == 0 or np.isnan((total_asset - position_val - order_val) / price / 10):
            return 0
        # calc max
        can_buy_vol = max(math.floor((total_asset - position_val - order_val) / price / 10), 0)
        if volume > can_buy_vol:
            logger.critical(f"id = {strategy_id}: cannot buy {volume}, choose max buy volume: {can_buy_vol}")
            return can_buy_vol
        else:
            return volume

    def get_reason_can_buy(self, volume: int, price: float, strategy_id: int) -> str:
        # query position
        stock_id_tuple = self.stock_ids[strategy_id]
        position_val = 0.0
        for stock_id in stock_id_tuple:
            position = self.query_position_by_stock(stock_id)
            if position is None:
                continue
            # use open_price, because avg price may be 0
            position_val += (position.can_use_volume + position.frozen_volume) * position.open_price
        # query order
        order_val = 0.0
        for order in self.query_orders():
            if order.stock_code in stock_id_tuple:
                order_val += order.order_volume * order.price * (-1 if order.order_type == xtconstant.STOCK_SELL else 1)
        # query asset
        if self.query_stock_asset() is None:
            return "query asset data failed"
        total_asset = self.query_stock_asset().total_asset
        total_asset = min(total_asset, self.max_cash) * self.position_manager.positions[strategy_id]
        # check
        if price == 0 or volume == 0 or np.isnan((total_asset - position_val - order_val) / price / 10):
            return "query stock data failed"
        # calc max
        can_buy_vol = max(math.floor((total_asset - position_val - order_val) / price / 10), 0)
        if volume > can_buy_vol:
            return f"cannot buy {volume}, choose max buy volume: {can_buy_vol}"
        else:
            return "can buy"
