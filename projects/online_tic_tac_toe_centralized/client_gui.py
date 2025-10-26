import socket
import threading
import tkinter as tk
from tkinter import messagebox

class TicTacToeClientGUI:
    def __init__(self):
        self.client = None
        self.player_id = None
        self.board = [' '] * 9
        self.my_turn = False
        self.root = tk.Tk()
        self.root.title('Tic Tac Toe Client')
        self.buttons = []
        self.status_label = tk.Label(self.root, text='Enter server info and room name')
        self.status_label.pack()
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=10)
        tk.Label(self.entry_frame, text='Server IP/Domain:').grid(row=0, column=0)
        self.ip_entry = tk.Entry(self.entry_frame)
        self.ip_entry.insert(0, '127.0.0.1')
        self.ip_entry.grid(row=0, column=1)
        tk.Label(self.entry_frame, text='Port:').grid(row=1, column=0)
        self.port_entry = tk.Entry(self.entry_frame)
        self.port_entry.insert(0, '65432')
        self.port_entry.grid(row=1, column=1)
        tk.Label(self.entry_frame, text='Room Name:').grid(row=2, column=0)
        self.room_entry = tk.Entry(self.entry_frame)
        self.room_entry.grid(row=2, column=1)
        self.connect_btn = tk.Button(self.entry_frame, text='Connect', command=self.connect_to_server)
        self.connect_btn.grid(row=3, column=0, columnspan=2, pady=5)
        self.board_frame = None
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.mainloop()

    def create_board(self):
        if self.board_frame:
            self.board_frame.destroy()
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.board_frame, text=' ', width=6, height=3,
                            font=('Arial', 20), command=lambda idx=i: self.send_move(idx))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

    def connect_to_server(self):
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        room = self.room_entry.get().strip()
        if not ip or not port or not room:
            messagebox.showerror('Error', 'Please enter all fields.')
            return
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((ip, int(port)))
        except Exception as e:
            messagebox.showerror('Connection Error', f'Could not connect: {e}')
            return
        self.status_label.config(text='Connected. Joining room...')
        self.entry_frame.pack_forget()
        self.create_board()
        threading.Thread(target=self.listen_to_server, args=(room,), daemon=True).start()

    def update_board(self):
        for i in range(9):
            self.buttons[i]['text'] = self.board[i]

    def send_move(self, idx):
        if self.my_turn and self.board[idx] == ' ':
            self.client.sendall(str(idx).encode())
            self.my_turn = False
        else:
            messagebox.showinfo('Invalid Move', 'Not your turn or cell occupied.')

    def listen_to_server(self, room):
        waiting_for_game = True
        try:
            # Wait for ROOM_NAME? prompt
            data = self.client.recv(1024).decode()
            if data == 'ROOM_NAME?':
                self.client.sendall(room.encode())
            while True:
                data = self.client.recv(1024).decode()
                if not data:
                    break
                if data.startswith('WELCOME'):
                    self.player_id = int(data.split(':')[1])
                    self.status_label.config(text=f'You are Player {self.player_id + 1} ({"X" if self.player_id == 0 else "O"})\nWaiting for another player...')
                elif len(data) == 9 and set(data).issubset({'X','O',' '}):
                    waiting_for_game = False
                    self.board = list(data)
                    self.update_board()
                elif data.startswith('WINNER'):
                    winner = data.split(':')[1]
                    self.status_label.config(text=f'Game Over! Winner: {winner}')
                    messagebox.showinfo('Game Over', f'Winner: {winner}')
                    break
                elif data == 'DRAW':
                    self.status_label.config(text="Game Over! It's a draw.")
                    messagebox.showinfo('Game Over', "It's a draw.")
                    break
                elif data == 'INVALID':
                    messagebox.showinfo('Invalid Move', 'Invalid move. Try again.')
                elif data == 'YOUR_TURN':
                    self.my_turn = True
                    self.status_label.config(text='Your turn! Click a cell.')
                elif data == 'Room full. Try another room.':
                    self.status_label.config(text='Room full. Try another room.')
                    messagebox.showerror('Room Full', 'Room is full. Try another room.')
                    break
                elif waiting_for_game:
                    self.status_label.config(text='Waiting for another player to join...')
        except Exception as e:
            pass
        try:
            self.client.close()
        except:
            pass

    def on_close(self):
        try:
            if self.client:
                self.client.close()
        except:
            pass
        self.root.destroy()

if __name__ == '__main__':
    TicTacToeClientGUI()

    def create_board(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(9):
            btn = tk.Button(frame, text=' ', width=6, height=3,
                            font=('Arial', 20), command=lambda idx=i: self.send_move(idx))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

    def update_board(self):
        for i in range(9):
            self.buttons[i]['text'] = self.board[i]

    def send_move(self, idx):
        if self.my_turn and self.board[idx] == ' ':
            self.client.sendall(str(idx).encode())
            self.my_turn = False
        else:
            messagebox.showinfo('Invalid Move', 'Not your turn or cell occupied.')

    def listen_to_server(self):
        waiting_for_game = True
        while True:
            try:
                data = self.client.recv(1024).decode()
                if not data:
                    break
                if data.startswith('WELCOME'):
                    self.player_id = int(data.split(':')[1])
                    self.status_label.config(text=f'You are Player {self.player_id + 1} ({"X" if self.player_id == 0 else "O"})\nWaiting for another player...')
                elif len(data) == 9 and set(data).issubset({'X','O',' '}):
                    waiting_for_game = False
                    self.board = list(data)
                    self.update_board()
                elif data.startswith('WINNER'):
                    winner = data.split(':')[1]
                    self.status_label.config(text=f'Game Over! Winner: {winner}')
                    messagebox.showinfo('Game Over', f'Winner: {winner}')
                    break
                elif data == 'DRAW':
                    self.status_label.config(text="Game Over! It's a draw.")
                    messagebox.showinfo('Game Over', "It's a draw.")
                    break
                elif data == 'INVALID':
                    messagebox.showinfo('Invalid Move', 'Invalid move. Try again.')
                elif data == 'YOUR_TURN':
                    self.my_turn = True
                    self.status_label.config(text='Your turn! Click a cell.')
                elif waiting_for_game:
                    self.status_label.config(text='Waiting for another player to join...')
            except Exception as e:
                break
        self.client.close()

    def on_close(self):
        try:
            self.client.close()
        except:
            pass
        self.root.destroy()

if __name__ == '__main__':
    TicTacToeClientGUI()
