import socket
import connection_code_util

symbols = ['X', 'O']
board = [' ']*9
current_player = 0

def display_board():
    print("\nCurrent Board:")
    for i in range(0, 9, 3):
        print(' | '.join(board[i:i+3]))
        if i < 6:
            print("---------")

def check_winner():
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def main():
    print("[DEBUG] Waiting for connection code from host...")
    code = input("Enter connection code from host: ")
    print(f"[DEBUG] Received code: {code}")
    host, port = connection_code_util.decode_connection(code)
    print(f"[DEBUG] Decoded host: {host}, port: {port}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[DEBUG] Attempting to connect to {host}:{port}...")
    s.connect((host, port))
    print(f"Connected to host at {host}:{port}")
    while True:
        global current_player
        display_board()
        if current_player == 1:
            while True:
                move = input("Your move (0-8): ")
                if move.isdigit() and int(move) in range(9) and board[int(move)] == ' ':
                    move = int(move)
                    board[move] = symbols[1]
                    s.sendall(str(move).encode())
                    break
                else:
                    print("Invalid move. Try again.")
        else:
            print("Waiting for host's move...")
            move = int(s.recv(1024).decode())
            if board[move] == ' ':
                board[move] = symbols[0]
            else:
                print("Host sent invalid move!")
        winner = check_winner()
        if winner:
            display_board()
            print(f"Game Over! Winner: {winner}")
            break
        elif ' ' not in board:
            display_board()
            print("Game Over! It's a draw.")
            break
        current_player = 1 - current_player
    s.close()

if __name__ == "__main__":
    main()