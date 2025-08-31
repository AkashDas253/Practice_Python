import unittest
import json
from app.routes import app, order_books
from app.order_book import OrderBook

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Clear order_books for a clean test
        order_books.clear()

    def test_add_and_depth_multi_symbol(self):
        # Add order for BTCUSD
        resp = self.client.post('/order', json={
            'order_id': '1', 'symbol': 'BTCUSD', 'side': 'buy', 'price': 100, 'quantity': 1, 'user_id': 'u1'
        })
        self.assertEqual(resp.status_code, 200)
        # Add order for ETHUSD
        resp = self.client.post('/order', json={
            'order_id': '2', 'symbol': 'ETHUSD', 'side': 'sell', 'price': 200, 'quantity': 2, 'user_id': 'u2'
        })
        self.assertEqual(resp.status_code, 200)
        # Check depth for BTCUSD
        resp = self.client.get('/depth?symbol=BTCUSD')
        data = resp.get_json()
        self.assertEqual(data['bids'], [[100.0, 1.0]])
        self.assertEqual(data['asks'], [])
        # Check depth for ETHUSD
        resp = self.client.get('/depth?symbol=ETHUSD')
        data = resp.get_json()
        self.assertEqual(data['bids'], [])
        self.assertEqual(data['asks'], [[200.0, 2.0]])

    def test_match_and_pnl_multi_symbol(self):
        # Add buy and sell for BTCUSD
        self.client.post('/order', json={
            'order_id': '1', 'symbol': 'BTCUSD', 'side': 'buy', 'price': 101, 'quantity': 2, 'user_id': 'A'
        })
        self.client.post('/order', json={
            'order_id': '2', 'symbol': 'BTCUSD', 'side': 'sell', 'price': 100, 'quantity': 2, 'user_id': 'B'
        })
        # Match BTCUSD
        resp = self.client.post('/match', json={'symbol': 'BTCUSD'})
        trades = resp.get_json()['trades']
        self.assertEqual(len(trades), 1)
        # Check PnL for A and B
        resp = self.client.get('/pnl?symbol=BTCUSD&user_id=A')
        pnlA = resp.get_json()
        self.assertEqual(pnlA['positions']['BTCUSD'], 2)
        self.assertEqual(pnlA['realized'], -200)
        resp = self.client.get('/pnl?symbol=BTCUSD&user_id=B')
        pnlB = resp.get_json()
        self.assertEqual(pnlB['positions']['BTCUSD'], -2)
        self.assertEqual(pnlB['realized'], 200)

if __name__ == '__main__':
    unittest.main()
