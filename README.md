## Order Book + Matching Engine

### Features
- Add, modify, and cancel orders via REST API
- Real-time order matching engine
- L2 depth aggregation for each symbol
- Multi-symbol support (e.g., BTCUSD, ETHUSD)
- User-level PnL (Profit and Loss) tracking

### Running the Server
1. Install dependencies:
   ```powershell
   pip install flask
   ```
2. Start the server from the project root:
   ```powershell
   python -m app.routes
   ```

### API Endpoints
- `POST /order` — Add a new order
- `POST /order/modify` — Modify an existing order
- `POST /order/cancel` — Cancel an order
- `GET /depth?symbol=SYMBOL` — Get L2 depth for a symbol
- `POST /match` — Match orders for a symbol
- `GET /pnl?symbol=SYMBOL&user_id=USER` — Get user PnL

### Example PowerShell API Test
See `tests/test_api.ps1` for a script to test all main features from PowerShell.

### Data Storage
All data is stored in memory. Restarting the server will reset all order books and PnL.