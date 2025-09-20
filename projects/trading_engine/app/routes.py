from flask import Flask, request, jsonify
from .order_book import OrderBook, Order
from .pnl import PnLTracker

app = Flask(__name__)

# For demo, use a single symbol and order book
order_books = {'BTCUSD': OrderBook('BTCUSD')}

@app.route('/order', methods=['POST'])
def add_order():
    data = request.json
    symbol = data.get('symbol', 'BTCUSD')
    if symbol not in order_books:
        order_books[symbol] = OrderBook(symbol)
    order = Order(
        order_id=data['order_id'],
        symbol=symbol,
        side=data['side'],
        price=float(data['price']),
        quantity=float(data['quantity'])
    )
    if 'user_id' in data:
        order.user_id = data['user_id']
    order_books[symbol].add_order(order)
    return jsonify({'status': 'ok'})

@app.route('/order/modify', methods=['POST'])
def modify_order():
    data = request.json
    symbol = data.get('symbol', 'BTCUSD')
    if symbol not in order_books:
        return jsonify({'status': 'not found'})
    result = order_books[symbol].modify_order(
        data['order_id'],
        float(data['quantity']),
        float(data['price']) if 'price' in data else None
    )
    return jsonify({'status': 'ok' if result else 'not found'})

@app.route('/order/cancel', methods=['POST'])
def cancel_order():
    data = request.json
    symbol = data.get('symbol', 'BTCUSD')
    if symbol not in order_books:
        return jsonify({'status': 'not found'})
    result = order_books[symbol].cancel_order(data['order_id'])
    return jsonify({'status': 'ok' if result else 'not found'})

@app.route('/depth', methods=['GET'])
def get_depth():
    symbol = request.args.get('symbol', 'BTCUSD')
    if symbol not in order_books:
        return jsonify({'bids': [], 'asks': []})
    depth = order_books[symbol].get_l2_depth()
    return jsonify(depth)

@app.route('/match', methods=['POST'])
def match():
    symbol = request.json.get('symbol', 'BTCUSD')
    if symbol not in order_books:
        return jsonify({'trades': []})
    trades = order_books[symbol].match_orders()
    return jsonify({'trades': trades})

@app.route('/pnl', methods=['GET'])
def get_pnl():
    symbol = request.args.get('symbol', 'BTCUSD')
    user_id = request.args.get('user_id')
    if symbol not in order_books:
        return jsonify({'realized': 0.0, 'positions': {}})
    pnl = order_books[symbol].pnl_tracker.get_pnl(user_id)
    return jsonify(pnl)

if __name__ == '__main__':
    app.run(debug=True)
