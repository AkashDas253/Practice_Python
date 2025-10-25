import socket
import threading

HOST = '0.0.0.0'
PORT = 65432

class TicTacToeServer:
    def __init__(self, host=HOST, port=PORT):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        print(f"[SERVER] Listening on {host}:{port}")
        self.clients = []
        self.board = [' ']*9
        self.current_player = 0
        self.symbols = ['X', 'O']

    def broadcast(self, message):
        print(f"[SERVER] Broadcasting: {message}")
        for client in self.clients:
            client.sendall(message.encode())

    def send_to_player(self, player_id, message):
        print(f"[SERVER] Sending to Player {player_id}: {message}")
        self.clients[player_id].sendall(message.encode())

    def handle_client(self, client, player_id):
        while True:
            try:
                # Only prompt the current player for input
                if self.current_player == player_id:
                    self.send_to_player(player_id, "YOUR_TURN")
                    print(f"[SERVER] Waiting for move from Player {player_id}")
                    data = client.recv(1024).decode()
                    print(f"[SERVER] Received from Player {player_id}: {data}")
                    if not data:
                        print(f"[SERVER] Player {player_id} disconnected.")
                        break
                    move = int(data)
                    if self.board[move] == ' ':
                        self.board[move] = self.symbols[player_id]
                        print(f"[SERVER] Player {player_id} placed {self.symbols[player_id]} at {move}")
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
                print(f"[SERVER] Error: {e}")
                break
        client.close()

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

    def run(self):
        try:
            while len(self.clients) < 2:
                client, addr = self.server.accept()
                print(f"[SERVER] Client {addr} connected.")
                self.clients.append(client)
                client.sendall(f"WELCOME:{len(self.clients)-1}".encode())
            self.broadcast(self.get_board_state())
            threads = []
            for i, client in enumerate(self.clients):
                t = threading.Thread(target=self.handle_client, args=(client, i), daemon=True)
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
        except KeyboardInterrupt:
            print("\n[SERVER] Server stopped by user.")
        finally:
            for client in self.clients:
                try:
                    client.close()
                except:
                    pass
            self.server.close()

if __name__ == "__main__":
    try:
        TicTacToeServer().run()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
