# Online Tic Tac Toe (Centralized)

A multi-room, multi-client Tic Tac Toe game using Python sockets and Tkinter GUI.

## Features
- Centralized server supports multiple game rooms.
- Each room allows two players to play Tic Tac Toe.
- Tkinter GUI client for easy play.
- Real-time board updates and game status.
- Handles disconnects, timeouts, and invalid moves.

## How to Run

### 1. Start the Server
Open a terminal and run:
```
python server.py
```


### 2. Start Clients
You can use either the GUI or CLI client, or mix both:

- For GUI client:
	```
	python client_gui.py
	```
- For CLI client:
	```
	python client_cli.py
	```

You can play with one player using the GUI and another using the CLI, or both using the same type.

### 3. Play
- Enter server IP and port (default: 127.0.0.1:65432).
- Choose to create a new room or join an existing room.
- Play Tic Tac Toe with real-time board updates.
- Game ends with win/draw notification.


## File Structure
- `server.py` — Centralized game server.
- `client_gui.py` — Tkinter GUI client.
- `client_cli.py` — Command-line client.
- `readme.md` — This documentation.

## Requirements
- Python 3.x
- Tkinter (usually included with Python)

## Notes
- Both server and clients must be on the same network or have network access.
- For remote play, use the server's public IP and ensure firewall allows the port.

## Troubleshooting
- If the game does not start, check server and client logs for errors.
- Make sure both clients connect to the same room number.
- If you see connection errors, check your network/firewall settings.

## License
MIT
