import socket

HOST = ''  # Listen on all interfaces
PORT = 65432

board = [' ']*9
symbols = ['X', 'O']
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
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def main():
    import socket
    import connection_code_util
    # Get local IP
    local_ip = socket.gethostbyname(socket.gethostname())
    port = PORT
    # Check if port is available
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, port))
            break
        except OSError:
            print(f"Port {port} is in use. Please enter a different port:")
            port = int(input("Port: "))
    code = connection_code_util.encode_connection(local_ip, port)
    print(f"Hosting game on port {port}.")
    print(f"Share this code with your opponent:")
    print(code)
    s.listen(1)
    conn, addr = s.accept()
    print(f"Guest connected from {addr}")
    while True:
        global current_player
        display_board()
        if current_player == 0:
            while True:
                move = input("Your move (0-8): ")
                if move.isdigit() and int(move) in range(9) and board[int(move)] == ' ':
                    move = int(move)
                    board[move] = symbols[0]
                    conn.sendall(str(move).encode())
                    break
                else:
                    print("Invalid move. Try again.")
        else:
            print("Waiting for guest's move...")
            move = int(conn.recv(1024).decode())
            if board[move] == ' ':
                board[move] = symbols[1]
            else:
                print("Guest sent invalid move!")
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
    conn.close()
    s.close()

if __name__ == "__main__":
    main()
