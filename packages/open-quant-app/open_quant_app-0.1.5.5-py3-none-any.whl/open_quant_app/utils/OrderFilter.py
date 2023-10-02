from typing import List
from xtquant.xttype import XtOrder
import xtquant.xtconstant as xtconst


class OrderFilter:
    @staticmethod
    def filter(orders: List[XtOrder], stock_pool: List[str],
               filter_canceled: bool = True,
               filter_wrong_id: bool = True) -> List[XtOrder]:
        filtered_orders: List[XtOrder] = []
        for order in orders:
            if order.stock_code in stock_pool \
                    and (not filter_canceled or order.order_status != xtconst.ORDER_CANCELED) \
                    and (not filter_wrong_id or order.order_id > 0):
                filtered_orders.append(order)
        return filtered_orders

    @staticmethod
    def filter_order_type(orders: List[XtOrder], order_type: int) -> List[XtOrder]:
        filtered_orders: List[XtOrder] = []
        for order in orders:
            if order.order_type == order_type:
                filtered_orders.append(order)
        return filtered_orders

    @staticmethod
    def filter_order_status(orders: List[XtOrder], filtered_order_status: List[int]) -> List[XtOrder]:
        filtered_orders: List[XtOrder] = []
        for order in orders:
            if order.order_status not in filtered_order_status:
                filtered_orders.append(order)
        return filtered_orders
