
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import time
from app.pnl import PnLTracker

@dataclass
class Order:
    order_id: str
    symbol: str
    side: str  # 'buy' or 'sell'
    price: float
    quantity: float
    timestamp: float = field(default_factory=lambda: time.time())

class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.bids: List[Order] = []  # Buy orders
        self.asks: List[Order] = []  # Sell orders
        self.order_map: Dict[str, Order] = {}
        self.pnl_tracker = PnLTracker()

    def add_order(self, order: Order):
        if order.side == 'buy':
            self.bids.append(order)
            self.bids.sort(key=lambda x: (-x.price, x.timestamp))
        else:
            self.asks.append(order)
            self.asks.sort(key=lambda x: (x.price, x.timestamp))
        self.order_map[order.order_id] = order

    def modify_order(self, order_id: str, new_quantity: float, new_price: Optional[float] = None):
        order = self.order_map.get(order_id)
        if not order:
            return False
        order.quantity = new_quantity
        if new_price is not None:
            order.price = new_price
        # Re-sort after modification
        if order.side == 'buy':
            self.bids.sort(key=lambda x: (-x.price, x.timestamp))
        else:
            self.asks.sort(key=lambda x: (x.price, x.timestamp))
        return True

    def cancel_order(self, order_id: str):
        order = self.order_map.pop(order_id, None)
        if not order:
            return False
        if order.side == 'buy':
            self.bids = [o for o in self.bids if o.order_id != order_id]
        else:
            self.asks = [o for o in self.asks if o.order_id != order_id]
        return True

    def get_l2_depth(self):
        # Returns aggregated price levels for bids and asks
        def aggregate(orders):
            levels = {}
            for o in orders:
                levels[o.price] = levels.get(o.price, 0) + o.quantity
            return sorted(levels.items(), reverse=orders is self.bids)
        return {
            'bids': aggregate(self.bids),
            'asks': aggregate(self.asks)
        }

    def match_orders(self):
        """
        Matches buy and sell orders and returns a list of executed trades.
        Each trade is a dict: {'buy_order_id', 'sell_order_id', 'price', 'quantity'}
        Also updates PnL for users if user_id is present in Order.
        """
        trades = []
        while self.bids and self.asks and self.bids[0].price >= self.asks[0].price:
            buy = self.bids[0]
            sell = self.asks[0]
            trade_qty = min(buy.quantity, sell.quantity)
            trade_price = sell.price  # Price is usually the passive order's price
            trades.append({
                'buy_order_id': buy.order_id,
                'sell_order_id': sell.order_id,
                'price': trade_price,
                'quantity': trade_qty
            })
            # Update PnL if user_id is present in Order
            buy_user = getattr(buy, 'user_id', None)
            sell_user = getattr(sell, 'user_id', None)
            if buy_user and sell_user:
                self.pnl_tracker.update_trade(buy_user, sell_user, self.symbol, trade_price, trade_qty)
            buy.quantity -= trade_qty
            sell.quantity -= trade_qty
            if buy.quantity == 0:
                self.bids.pop(0)
                self.order_map.pop(buy.order_id, None)
            if sell.quantity == 0:
                self.asks.pop(0)
                self.order_map.pop(sell.order_id, None)
        return trades
