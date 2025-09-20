import unittest
from app.order_book import Order, OrderBook

class TestOrderBookMatching(unittest.TestCase):
    def setUp(self):
        self.book = OrderBook(symbol='BTCUSD')

    def test_simple_match(self):
        # Add a buy order and a sell order that should match
        buy = Order(order_id='b1', symbol='BTCUSD', side='buy', price=101, quantity=2)
        sell = Order(order_id='s1', symbol='BTCUSD', side='sell', price=100, quantity=1)
        self.book.add_order(buy)
        self.book.add_order(sell)
        trades = self.book.match_orders()
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]['buy_order_id'], 'b1')
        self.assertEqual(trades[0]['sell_order_id'], 's1')
        self.assertEqual(trades[0]['price'], 100)
        self.assertEqual(trades[0]['quantity'], 1)
        # Buy order should have 1 left, sell order should be gone
        self.assertEqual(self.book.bids[0].quantity, 1)
        self.assertEqual(len(self.book.asks), 0)

    def test_multiple_matches(self):
        # Add multiple orders to test partial and multiple matches
        self.book.add_order(Order(order_id='b1', symbol='BTCUSD', side='buy', price=101, quantity=2))
        self.book.add_order(Order(order_id='b2', symbol='BTCUSD', side='buy', price=100, quantity=1))
        self.book.add_order(Order(order_id='s1', symbol='BTCUSD', side='sell', price=100, quantity=2))
        trades = self.book.match_orders()
        # Only one trade should occur: b1 (2) matches s1 (2) for 2
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]['buy_order_id'], 'b1')
        self.assertEqual(trades[0]['sell_order_id'], 's1')
        self.assertEqual(trades[0]['quantity'], 2)
        self.assertEqual(trades[0]['price'], 100)
        # After matching, b1 and s1 should be gone, b2 should remain
        self.assertEqual(len(self.book.bids), 1)
        self.assertEqual(self.book.bids[0].order_id, 'b2')
        self.assertEqual(self.book.bids[0].quantity, 1)
        self.assertEqual(len(self.book.asks), 0)

if __name__ == '__main__':
    unittest.main()
