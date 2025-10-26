
# Multi-room Tic Tac Toe Server
import socket
import threading

HOST = '0.0.0.0'
PORT = 65432

class GameRoom:
    def __init__(self, room_name):
        self.room_name = room_name
        self.clients = []
        self.board = [' '] * 9
        self.current_player = 0
        self.symbols = ['X', 'O']
        self.lock = threading.Lock()

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.sendall(message.encode())
            except:
                pass

    def send_to_player(self, player_id, message):
        try:
            self.clients[player_id].sendall(message.encode())
        except:
            pass

    def get_board_state(self):
        return ''.join(self.board)

    def check_winner(self):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        return None

    def run_game(self):
        self.broadcast(self.get_board_state())
        threads = []
        for i, client in enumerate(self.clients):
            t = threading.Thread(target=self.handle_client, args=(client, i), daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def handle_client(self, client, player_id):
        while True:
            try:
                if self.current_player == player_id:
                    self.send_to_player(player_id, "YOUR_TURN")
                    data = client.recv(1024).decode()
                    if not data:
                        break
                    move = int(data)
                    with self.lock:
                        if self.board[move] == ' ':
                            self.board[move] = self.symbols[player_id]
                            self.broadcast(self.get_board_state())
                            winner = self.check_winner()
                            if winner:
                                self.broadcast(f"WINNER:{winner}")
                                break
                            elif ' ' not in self.board:
                                self.broadcast("DRAW")
                                break
                            self.current_player = 1 - self.current_player
                        else:
                            client.sendall("INVALID".encode())
                else:
                    import time
                    time.sleep(0.1)
            except Exception as e:
                break
        try:
            client.close()
        except:
            pass

class TicTacToeServer:
    def __init__(self, host=HOST, port=PORT):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(100)
        print(f"[SERVER] Listening on {host}:{port}")
        self.rooms = {}  # room_name -> GameRoom
        self.lock = threading.Lock()

    def client_handler(self, client, addr):
        try:
            client.sendall("ROOM_NAME?".encode())
            room_name = client.recv(1024).decode().strip()
            if not room_name:
                client.sendall("Invalid room name.".encode())
                client.close()
                return
            with self.lock:
                if room_name not in self.rooms:
                    self.rooms[room_name] = GameRoom(room_name)
                room = self.rooms[room_name]
                if len(room.clients) >= 2:
                    client.sendall("Room full. Try another room.".encode())
                    client.close()
                    return
                room.clients.append(client)
                client.sendall(f"WELCOME:{len(room.clients)-1}".encode())
            # Start game if two clients
            if len(room.clients) == 2:
                threading.Thread(target=room.run_game, daemon=True).start()
            else:
                client.sendall("Waiting for another player to join...".encode())
        except Exception as e:
            try:
                client.close()
            except:
                pass

    def run(self):
        try:
            while True:
                client, addr = self.server.accept()
                print(f"[SERVER] Client {addr} connected.")
                threading.Thread(target=self.client_handler, args=(client, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\n[SERVER] Server stopped by user.")
        finally:
            self.server.close()

if __name__ == "__main__":
    try:
        TicTacToeServer().run()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
