class PnLTracker:
    def __init__(self):
        # Maps user_id to {'realized': float, 'positions': {symbol: float}}
        self.user_pnl = {}

    def update_trade(self, buy_user, sell_user, symbol, price, quantity):
        # Buyer's position increases, seller's decreases
        self._update_position(buy_user, symbol, quantity, -price * quantity)
        self._update_position(sell_user, symbol, -quantity, price * quantity)

    def _update_position(self, user, symbol, qty_change, pnl_change):
        if user not in self.user_pnl:
            self.user_pnl[user] = {'realized': 0.0, 'positions': {}}
        self.user_pnl[user]['realized'] += pnl_change
        self.user_pnl[user]['positions'][symbol] = self.user_pnl[user]['positions'].get(symbol, 0.0) + qty_change

    def get_pnl(self, user):
        return self.user_pnl.get(user, {'realized': 0.0, 'positions': {}})
