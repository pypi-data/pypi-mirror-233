from datetime import datetime
from typing import Type
from threading import Thread

from loguru import logger
from open_quant_app.trade.Trader import Trader, TradeMode
from open_quant_app.strategy.Strategy import Strategy


class QuantApp:
    def __init__(self, config: dict, strategy: Type[Strategy], mode: TradeMode = TradeMode.MARKET, cash: int = 200000):
        logger.info("=== STRATEGY INIT ===")
        self.config: dict = config
        self.mode: TradeMode = mode
        # init trader
        logger.info("initializing trader module ...")
        if self.mode == TradeMode.MARKET:
            self.trader = Trader(self.config)
        elif self.mode == TradeMode.BACKTEST:
            self.trader = Trader(self.config, mode, cash=cash)
        self.trader.start()
        self.trader.info()
        # init strategies
        logger.info("initializing strategy module ...")
        self.strategy: Type[Strategy] = strategy
        self.strategies = []
        for i in range(len(self.config['stock']['stock_ids'])):
            self.strategies.append(self.strategy(i, self.trader, self.config))
            logger.success(f"strategy-{i} created")

    def run(self, begin: datetime = None, end: datetime = None):
        logger.info("begin main loop")
        if self.mode == TradeMode.MARKET:
            for strategy in self.strategies:
                strategy_thread = Thread(target=strategy.main_loop, args=())
                strategy_thread.start()
        elif self.mode == TradeMode.BACKTEST:
            for strategy in self.strategies:
                strategy_thread = Thread(target=strategy.main_loop_back, args=(begin, end))
                strategy_thread.start()
