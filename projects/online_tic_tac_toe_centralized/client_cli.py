
import socket
import sys
import logging

logging.basicConfig(filename='client_cli.log', level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s')

def log(msg):
    print(msg)
    logging.info(msg)

HOST = input('Enter server IP (default 127.0.0.1): ') or '127.0.0.1'
PORT = int(input('Enter server port (default 65432): ') or '65432')

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    log(f'Connected to {HOST}:{PORT}')
except Exception as e:
    log(f'Connection error: {e}')
    sys.exit(1)

def recv_msgs():
    data = b''
    while True:
        part = client.recv(1024)
        if not part:
            break
        data += part
        if b'\n' in part:
            break
    msgs = data.decode().split('\n')
    for msg in msgs:
        logging.debug(f'Received: {repr(msg)}')
    return msgs

# Room selection
msgs = recv_msgs()
for msg in msgs:
    if msg:
        log(msg)
mode = input('Type "new" to create a room or "join" to join: ').strip()
client.sendall((mode + '\n').encode())
msgs = recv_msgs()
for msg in msgs:
    if msg:
        log(msg)
if mode == 'new':
    if msgs[0].startswith('Your new room number is:'):
        room_name = msgs[0].split(':')[1].strip()
        log(f'Waiting for opponent in room {room_name}...')
    else:
        log(msgs[0])
        sys.exit(1)
elif mode == 'join':
    if msgs[0].startswith('Enter room number:'):
        room_name = input('Enter room number: ').strip()
        client.sendall((room_name + '\n').encode())
        log(f'Waiting for opponent in room {room_name}...')
    else:
        log(msgs[0])
        sys.exit(1)

# Game loop
symbol = None
while True:
    msgs = recv_msgs()
    board_updated = False
    for msg in msgs:
        msg = msg.replace('\n', '')
        if not msg:
            continue
        log(f'Handling message: {repr(msg)}')
        if msg.startswith('OPPONENT_JOINED'):
            log('Opponent joined! Game is starting.')
        elif msg.startswith('WELCOME'):
            try:
                player_id = int(msg.split(':')[1])
                symbol = 'X' if player_id == 0 else 'O'
                log(f'You are {symbol}')
            except Exception as e:
                log(f'Error parsing WELCOME: {e}')
        elif len(msg) == 9 and set(msg) <= {'X','O',' '}:
            board = list(msg)
            log('\nCurrent board:')
            log(f'{board[0]} | {board[1]} | {board[2]}')
            log('---------')
            log(f'{board[3]} | {board[4]} | {board[5]}')
            log('---------')
            log(f'{board[6]} | {board[7]} | {board[8]}')
            board_updated = True
        elif msg == 'YOUR_TURN':
            log('Your turn!')
            while True:
                move = input('Enter move (0-8): ').strip()
                if move.isdigit() and int(move) in range(9):
                    client.sendall(move.encode())
                    break
                else:
                    log('Invalid move. Try again.')
        elif msg == 'INVALID':
            log('Invalid move. Try again.')
        elif msg.startswith('WINNER'):
            if not board_updated:
                log('Board update before WINNER.')
            winner = msg.split(':')[1]
            log(f'Game Over! Winner: {winner}')
            sys.exit(0)
        elif msg == 'DRAW':
            if not board_updated:
                log('Board update before DRAW.')
            log("Game Over! It's a draw.")
            sys.exit(0)
        elif msg == 'Room full. Try another room.':
            log('Room is full. Try another room.')
            sys.exit(1)
        elif msg == 'Timeout waiting for opponent.':
            log('Timeout waiting for opponent.')
            sys.exit(1)
        else:
            log(msg)
