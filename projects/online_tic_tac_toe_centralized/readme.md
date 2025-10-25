# Online Tic-Tac-Toe

This project implements an online Tic-Tac-Toe game in Python using sockets.

## How to Run

### Server
1. Open a terminal and run:
   ```powershell
   python server.py
   ```
2. Wait for two clients to connect.

### Client
1. On two separate machines or terminals, run:
   ```powershell
   python client.py
   ```
2. Enter your moves when prompted (positions 0-8).

## Notes
- The server must be started before clients connect.
- Change `HOST` in `client.py` to the server's IP address if running on different machines.
- The board positions are numbered 0-8 as follows:

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```
