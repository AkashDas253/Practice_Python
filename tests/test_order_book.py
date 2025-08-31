import unittest
from app.order_book import Order, OrderBook
import time

class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.book = OrderBook(symbol='BTCUSD')

    def test_add_order(self):
        order1 = Order(order_id='1', symbol='BTCUSD', side='buy', price=100, quantity=1)
        order2 = Order(order_id='2', symbol='BTCUSD', side='sell', price=101, quantity=2)
        self.book.add_order(order1)
        self.book.add_order(order2)
        self.assertEqual(len(self.book.bids), 1)
        self.assertEqual(len(self.book.asks), 1)
        self.assertEqual(self.book.bids[0].order_id, '1')
        self.assertEqual(self.book.asks[0].order_id, '2')

    def test_modify_order(self):
        order = Order(order_id='1', symbol='BTCUSD', side='buy', price=100, quantity=1)
        self.book.add_order(order)
        self.book.modify_order('1', new_quantity=5, new_price=105)
        self.assertEqual(self.book.bids[0].quantity, 5)
        self.assertEqual(self.book.bids[0].price, 105)

    def test_cancel_order(self):
        order = Order(order_id='1', symbol='BTCUSD', side='buy', price=100, quantity=1)
        self.book.add_order(order)
        result = self.book.cancel_order('1')
        self.assertTrue(result)
        self.assertEqual(len(self.book.bids), 0)

    def test_l2_depth(self):
        self.book.add_order(Order(order_id='1', symbol='BTCUSD', side='buy', price=100, quantity=1))
        self.book.add_order(Order(order_id='2', symbol='BTCUSD', side='buy', price=100, quantity=2))
        self.book.add_order(Order(order_id='3', symbol='BTCUSD', side='sell', price=101, quantity=3))
        depth = self.book.get_l2_depth()
        self.assertEqual(depth['bids'], [(100, 3)])
        self.assertEqual(depth['asks'], [(101, 3)])

if __name__ == '__main__':
    unittest.main()
