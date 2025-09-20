import unittest
from app.order_book import OrderBook, Order
from app.pnl import PnLTracker

class TestPnLIntegration(unittest.TestCase):
    def setUp(self):
        self.book = OrderBook(symbol='BTCUSD')

    def test_pnl_update_on_trade(self):
        # Orders with user_id
        buy = Order(order_id='b1', symbol='BTCUSD', side='buy', price=101, quantity=2)
        buy.user_id = 'userA'
        sell = Order(order_id='s1', symbol='BTCUSD', side='sell', price=100, quantity=2)
        sell.user_id = 'userB'
        self.book.add_order(buy)
        self.book.add_order(sell)
        trades = self.book.match_orders()
        # Check trades
        self.assertEqual(len(trades), 1)
        # Check PnL
        pnlA = self.book.pnl_tracker.get_pnl('userA')
        pnlB = self.book.pnl_tracker.get_pnl('userB')
        # userA bought 2 at 100, userB sold 2 at 100
        self.assertEqual(pnlA['positions']['BTCUSD'], 2)
        self.assertEqual(pnlB['positions']['BTCUSD'], -2)
        self.assertEqual(pnlA['realized'], -200)
        self.assertEqual(pnlB['realized'], 200)

if __name__ == '__main__':
    unittest.main()
