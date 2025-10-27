import socket
import threading
import random

class GameRoom:
    def __init__(self, room_name):
        self.room_name = room_name
        self.clients = []
        self.board = [' '] * 9
        self.current_player = 0
        self.symbols = ['X', 'O']
        self.lock = threading.Lock()
        self.active = True
        print(f"[GameRoom] Created room {room_name}")

    def broadcast(self, msg):
        print(f"[GameRoom {self.room_name}] Broadcasting: {msg}")
        for c in self.clients:
            try:
                c.sendall((msg + '\n').encode())
            except Exception as e:
                print(f"[GameRoom {self.room_name}] Broadcast error: {e}")

    def check_winner(self):
        b = self.board
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for i,j,k in wins:
            if b[i] == b[j] == b[k] and b[i] != ' ':
                return b[i]
        if ' ' not in b:
            return 'DRAW'
        return None

    def run_game(self, cleanup_callback=None):
        print(f"[GameRoom {self.room_name}] Game starting with {len(self.clients)} clients.")
        try:
            self.broadcast('OPPONENT_JOINED')
            for idx, c in enumerate(self.clients):
                print(f"[GameRoom {self.room_name}] Sending WELCOME to client {idx}")
                c.sendall((f'WELCOME:{idx}\n').encode())
            self.broadcast(''.join(self.board))
            while self.active:
                try:
                    print(f"[GameRoom {self.room_name}] Player {self.current_player} turn.")
                    self.clients[self.current_player].sendall('YOUR_TURN\n'.encode())
                    self.clients[self.current_player].settimeout(120)
                    move = self.clients[self.current_player].recv(1024).decode()
                    print(f"[GameRoom {self.room_name}] Received move: {move}")
                except Exception as e:
                    print(f"[GameRoom {self.room_name}] Network error or timeout: {e}")
                    self.active = False
                    break
                valid_move = False
                try:
                    move_int = int(move)
                    if move_int in range(9) and self.board[move_int] == ' ':
                        valid_move = True
                except Exception as e:
                    print(f"[GameRoom {self.room_name}] Invalid move data: {move} ({e})")
                if not valid_move:
                    try:
                        self.clients[self.current_player].sendall('INVALID\n'.encode())
                    except Exception as e:
                        print(f"[GameRoom {self.room_name}] Error sending INVALID: {e}")
                    continue
                with self.lock:
                    self.board[move_int] = self.symbols[self.current_player]
                print(f"[GameRoom {self.room_name}] Board updated: {self.board}")
                self.broadcast(''.join(self.board))
                winner = self.check_winner()
                if winner:
                    print(f"[GameRoom {self.room_name}] Game ended. Winner: {winner}")
                    if winner == 'DRAW':
                        self.broadcast('DRAW')
                    else:
                        self.broadcast(f'WINNER:{winner}')
                    self.active = False
                    break
                self.current_player = 1 - self.current_player
        except Exception as e:
            print(f"[GameRoom {self.room_name}] Game error: {e}")
        finally:
            for c in self.clients:
                try:
                    c.close()
                except Exception as e:
                    print(f"[GameRoom {self.room_name}] Error closing client: {e}")
            if cleanup_callback:
                cleanup_callback(self.room_name)

class Server:
    def __init__(self, host='0.0.0.0', port=65432):
        self.host = host
        self.port = port
        self.rooms = {}
        self.lock = threading.Lock()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(100)
        print(f'[Server] Listening on {self.host}:{self.port}')

    def cleanup_room(self, room_name):
        with self.lock:
            if room_name in self.rooms:
                del self.rooms[room_name]
                print(f"[Server] Room {room_name} cleaned up.")

    def client_handler(self, conn, addr):
        print(f"[Server] New connection from {addr}")
        try:
            conn.settimeout(60)
            conn.sendall('Do you want to start a new game or join? (new/join)\n'.encode())
            mode = conn.recv(1024).decode().strip()
            print(f"[Server] Client {addr} selected mode: {mode}")
            if mode == 'new':
                room_name = str(random.randint(1000,9999))
                with self.lock:
                    self.rooms[room_name] = GameRoom(room_name)
                conn.sendall((f'Your new room number is: {room_name}\n').encode())
                self.rooms[room_name].clients.append(conn)
                print(f"[Server] Client {addr} created room {room_name}")
                # Wait for second player with timeout
                wait_time = 0
                while len(self.rooms[room_name].clients) < 2 and wait_time < 120:
                    threading.Event().wait(1)
                    wait_time += 1
                if len(self.rooms[room_name].clients) < 2:
                    try:
                        conn.sendall('Timeout waiting for opponent.'.encode())
                    except Exception as e:
                        print(f"[Server] Error sending timeout: {e}")
                    with self.lock:
                        del self.rooms[room_name]
                    print(f"[Server] Room {room_name} deleted due to timeout.")
                    conn.close()
                    return
                print(f"[Server] Room {room_name} starting game.")
                threading.Thread(target=self.rooms[room_name].run_game, args=(self.cleanup_room,), daemon=True).start()
            elif mode == 'join':
                conn.sendall('Enter room number:\n'.encode())
                room_name = conn.recv(1024).decode().strip()
                print(f"[Server] Client {addr} joining room {room_name}")
                with self.lock:
                    room = self.rooms.get(room_name)
                if not room or len(room.clients) >= 2:
                    try:
                        conn.sendall('Room full. Try another room.\n'.encode())
                    except Exception as e:
                        print(f"[Server] Error sending room full: {e}")
                    conn.close()
                    return
                room.clients.append(conn)
                print(f"[Server] Client {addr} joined room {room_name}")
                # Wait for second player with timeout
                wait_time = 0
                while len(room.clients) < 2 and wait_time < 120:
                    threading.Event().wait(1)
                    wait_time += 1
                if len(room.clients) < 2:
                    try:
                        conn.sendall('Timeout waiting for opponent.\n'.encode())
                    except Exception as e:
                        print(f"[Server] Error sending timeout: {e}")
                    with self.lock:
                        del self.rooms[room_name]
                    print(f"[Server] Room {room_name} deleted due to timeout.")
                    conn.close()
                    return
                print(f"[Server] Room {room_name} starting game.")
                threading.Thread(target=room.run_game, args=(self.cleanup_room,), daemon=True).start()
            else:
                try:
                    conn.sendall('Invalid option.\n'.encode())
                except Exception as e:
                    print(f"[Server] Error sending invalid option: {e}")
                conn.close()
        except Exception as e:
            print(f"[Server] Client handler error: {e}")
            try:
                conn.close()
            except Exception as e:
                print(f"[Server] Error closing connection: {e}")

    def start(self):
        while True:
            conn, addr = self.sock.accept()
            threading.Thread(target=self.client_handler, args=(conn, addr), daemon=True).start()

if __name__ == '__main__':
    Server().start()
