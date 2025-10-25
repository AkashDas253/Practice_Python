
# Peer-to-Peer Online Tic-Tac-Toe

This project implements a peer-to-peer Tic-Tac-Toe game in Python using sockets. No central server is required; one player acts as the host, the other as the guest.

## How to Run

### Host (Player 1)
1. Open a terminal and run:
   ```powershell
   python peer_host.py  
   ```
2. When prompted, the host will display a connection code. Share this code with your opponent.

### Guest (Player 2)
1. On a different machine, run:
   ```powershell
   python peer_guest.py
   ```
2. Enter the connection code provided by the host when prompted. The guest will automatically decode and connect to the host.


## Notes
- The host must start first and share the connection code with the guest.
- If running both scripts on the same machine, use different ports for host and guest to avoid conflicts. The host will prompt for a new port if the default is busy.
- For internet play, you may need to set up port forwarding on your router.
- The board positions are numbered 0-8 as follows:

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```
