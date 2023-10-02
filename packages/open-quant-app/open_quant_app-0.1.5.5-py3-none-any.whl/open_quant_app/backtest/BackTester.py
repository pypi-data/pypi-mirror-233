from typing import List, Dict
from datetime import datetime
import os

from open_quant_app.manager.PositionManager import PositionManager
from open_quant_app.model.BarData import BarData
from xtquant import xtconstant
from xtquant.xttype import XtPosition

from loguru import logger
import pandas as pd
import matplotlib.pyplot as plt


class BackPosition:
    def __init__(self, stock_id: str, price: float = 0.0, volume: int = 0):
        self.price = price
        self.avg_price = price
        self.volume = volume
        self.stock_id = stock_id

    def buy(self, price: float, volume: int):
        if volume == 0:
            return
        self.price = price
        self.avg_price = (self.avg_price * self.volume + price * volume) / (self.volume + volume)
        self.volume += volume

    def sell(self, price: float, volume: int) -> float:
        self.price = price
        self.volume -= volume
        return price * volume

    def value(self):
        return self.price * self.volume


class BackAccount:
    def __init__(self, cash: float = 0.0):
        self.initial_cash = cash
        self.cash = cash

    def deposit(self, money: float):
        self.cash += money

    def withdraw(self, money: float):
        self.cash -= money


class BackOrder:
    def __init__(self, order_type: int, price: float, volume: int, stock_id: str, strategy_id: int):
        self.order_type = order_type
        self.price = price
        self.volume = volume
        self.stock_id = stock_id
        self.strategy_id = strategy_id


class BackTester:
    def __init__(self, config: dict, cash: float = 100000, stock_list: List[str] = None):
        self.account = BackAccount(cash)
        self.stock_ids = config['stock']['stock_ids']
        self.stocks: Dict[str, BackPosition] = {}
        for stock_id in self.stocks:
            self.stocks[stock_id] = BackPosition(stock_id)
        self.position_manager = PositionManager(config)
        self.records: List[BackOrder] = []
        self.asset_records: Dict[datetime, float] = {}
        self.bar_data_records: Dict[str, Dict[datetime, BarData]] = {}
        self.begin: datetime = datetime.now()
        self.end: datetime = datetime.now()

    def set_time_seg(self, begin: datetime, end: datetime):
        self.begin = begin
        self.end = end

    # info functions
    def info(self):
        logger.info(f"initial cash = {self.account.cash}")

    def value(self) -> float:
        total_assets = 0
        for stock_id in self.stocks:
            total_assets += self.stocks[stock_id].value()
        total_assets += self.account.cash
        return total_assets

    # record functions
    def record_assets(self, timestamp: datetime):
        self.asset_records[timestamp] = self.value()

    def record_bar_data(self, bar_data: BarData):
        if bar_data.stock_id not in self.bar_data_records:
            self.bar_data_records[bar_data.stock_id] = {}
        self.bar_data_records[bar_data.stock_id][bar_data.timestamp] = bar_data

    # trade sim functions
    def query_position(self, stock_id: str) -> int:
        if stock_id in self.stocks:
            return self.stocks[stock_id].volume
        else:
            return 0

    def close_position(self, stock_id: str):
        if stock_id not in self.stocks:
            return
        position = self.stocks[stock_id]
        money = self.stocks[stock_id].sell(position.price, position.volume)
        self.account.deposit(money)

    def can_buy(self, volume: int, price: float, strategy_id: int) -> bool:
        xt_positions = []
        for stock_id in self.stock_ids[strategy_id]:
            back_position = self.stocks[stock_id]
            # simulate position data
            xt_position = XtPosition('backtester', stock_id, back_position.volume, back_position.volume, 0, 0, 0, 0, 0,
                                     back_position.avg_price)
            xt_positions.append(xt_position)
        total_assets = self.value()
        return not self.position_manager.is_position_limit(xt_positions, strategy_id, volume, price, total_assets)

    def can_sell(self, stock_id: str, volume: int, strategy_id: int) -> bool:
        if stock_id not in self.stocks:
            logger.warning(f"you have 0 position for stock {stock_id}, cannot sell !")
            return False
        else:
            position = self.stocks[stock_id]
            if position.volume < volume:
                logger.warning(f"position available volume = {position.volume} < sell volume {volume}, cancel !")
                return False
            else:
                return True

    def order_stock(self, stock_id: str, order_type: int, volume: int, price: float, strategy_id: int) -> int:
        if stock_id not in self.stocks:
            self.stocks[stock_id] = BackPosition(stock_id)
        if order_type == xtconstant.STOCK_BUY and self.can_buy(volume, price, strategy_id):
            self.stocks[stock_id].buy(price, volume)
            self.account.withdraw(price * volume)
            self.records.append(BackOrder(xtconstant.STOCK_BUY, price, volume, stock_id, strategy_id))
            return 0
        elif order_type == xtconstant.STOCK_SELL and self.can_sell(stock_id, volume, strategy_id):
            money = self.stocks[stock_id].sell(price, volume)
            self.account.deposit(money)
            self.records.append(BackOrder(xtconstant.STOCK_SELL, price, volume, stock_id, strategy_id))
            return 0
        else:
            return -1

    # report functions
    def check_output_dirs(self):
        dirs = ['../output/trade', '../output/bars', '../output/asset']
        for _dir in dirs:
            if not os.path.exists(_dir):
                os.makedirs(_dir)

    def report(self, strategy_id: int, save_as_file: bool = True,
               plot_assets: bool = True, plot_bars: bool = True):
        self.check_output_dirs()
        # log assets & ratio
        logger.critical(
            f"init = {self.account.initial_cash}, curr = {self.value()}, "
            f"ratio = {(self.value() - self.account.initial_cash) / self.account.initial_cash}")
        # save orders
        if not save_as_file:
            for i in range(len(self.records)):
                record = self.records[i]
                logger.info(
                    f"[{i}], stock id = {record.stock_id}, type = {'buy' if record.order_type == xtconstant.STOCK_BUY else 'sell'}"
                    f", price = {record.price}, volume = {record.volume}")
        elif len(self.records) != 0:
            df = pd.DataFrame([vars(record) for record in self.records])
            df[df['strategy_id'] == strategy_id].to_csv(f'../output/trade/strategy-{strategy_id}.csv')
        # plot assets curve
        if plot_assets:
            self.plot_asset_curve()
        if plot_bars:
            self.plot_bars()

    def plot_asset_curve(self):
        timestamps = list(self.asset_records.keys())
        assets = list(self.asset_records.values())

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, assets)
        plt.title("Datetime vs Pure Assets")
        plt.xlabel("Datetime")
        plt.ylabel("Pure Assets")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('../output/asset/assets-curve.jpg')
        plt.show()

    def plot_bars(self):
        for stock_id in self.bar_data_records:
            bar_data_dict = self.bar_data_records[stock_id]
            timestamps = list(bar_data_dict.keys())
            bar_data = list(bar_data_dict.values())
            close = [i.close for i in bar_data]

            plt.figure(figsize=(10, 5))
            plt.plot(timestamps, close)
            plt.title(f"Datetime vs Close [{stock_id}]")
            plt.xlabel("Datetime")
            plt.ylabel("Close")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'../output/bars/{stock_id}.jpg')
            plt.show()
