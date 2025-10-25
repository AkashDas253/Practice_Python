import socket

HOST = '127.0.0.1'  # Change to server IP if needed
PORT = 65432

class TicTacToeClient:
    def __init__(self, host=HOST, port=PORT):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        print(f"[CLIENT] Connected to server at {host}:{port}")
        self.player_id = None

    def display_board(self, board):
        print("\nCurrent Board:")
        for i in range(0, 9, 3):
            print(' | '.join(board[i:i+3]))
            if i < 6:
                print("---------")

    def run(self):
        try:
            waiting_for_game = True
            while True:
                data = self.client.recv(1024).decode()
                print(f"[CLIENT] Received: {data}")
                if data.startswith("WELCOME"):
                    self.player_id = int(data.split(":")[1])
                    print(f"You are Player {self.player_id + 1} ({'X' if self.player_id == 0 else 'O'})")
                    print("Waiting for another player to join...")
                elif len(data) == 9 and set(data).issubset({'X','O',' '}):
                    waiting_for_game = False
                    board = list(data)
                    self.display_board(board)
                elif data.startswith("WINNER"):
                    winner = data.split(":")[1]
                    print(f"Game Over! Winner: {winner}")
                    break
                elif data == "DRAW":
                    print("Game Over! It's a draw.")
                    break
                elif data == "INVALID":
                    print("Invalid move. Try again.")
                elif data == "YOUR_TURN":
                    while True:
                        move = input("Your move (0-8): ")
                        if move.isdigit() and int(move) in range(9):
                            self.client.sendall(move.encode())
                            print(f"[CLIENT] Sent move: {move}")
                            break
                        else:
                            print("Invalid input. Enter a number from 0 to 8.")
                elif waiting_for_game:
                    print("Waiting for another player to join...")
        except KeyboardInterrupt:
            print("\n[CLIENT] Client stopped by user.")
        finally:
            try:
                self.client.close()
            except:
                pass

if __name__ == "__main__":
    try:
        TicTacToeClient().run()
    except KeyboardInterrupt:
        print("\nClient stopped by user.")
