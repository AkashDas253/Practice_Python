import socket
import threading
import tkinter as tk
from tkinter import messagebox
import time

class TicTacToeClientGUI:
    def __init__(self):
        self.client = None
        self.player_id = None
        self.board = [' '] * 9
        self.my_turn = False
        self.room_name = None
        self.symbol = None
        self.root = tk.Tk()
        self.root.title('Tic Tac Toe Client')
        self.status_label = tk.Label(self.root, text='Enter server info', font=('Arial', 14))
        self.status_label.pack(pady=10)
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
        self.connect_btn = tk.Button(self.entry_frame, text='Connect', command=self.connect_to_server)
        self.connect_btn.grid(row=2, column=0, columnspan=2, pady=5)
        self.board_frame = None
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.mainloop()

    def show_room_choice(self):
        self.room_frame = tk.Frame(self.root)
        self.room_frame.pack(pady=10)
        tk.Label(self.room_frame, text='Create new room or join existing?').pack()
        tk.Button(self.room_frame, text='Create Room', command=self.create_room).pack(side='left', padx=10)
        tk.Button(self.room_frame, text='Join Room', command=self.join_room).pack(side='right', padx=10)

    def connect_to_server(self):
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        if not ip or not port:
            messagebox.showerror('Error', 'Please enter server IP and port.')
            return
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((ip, int(port)))
        except Exception as e:
            messagebox.showerror('Connection Error', f'Could not connect: {e}')
            return
        self.status_label.config(text='Connected!')
        self.entry_frame.pack_forget()
        self.show_room_choice()

    def create_room(self):
        self.room_frame.pack_forget()
        threading.Thread(target=self.room_flow, args=('new',), daemon=True).start()

    def join_room(self):
        self.room_frame.pack_forget()
        self.join_frame = tk.Frame(self.root)
        self.join_frame.pack(pady=10)
        tk.Label(self.join_frame, text='Enter Room Number:').pack(side='left')
        self.room_entry = tk.Entry(self.join_frame)
        self.room_entry.pack(side='left')
        tk.Button(self.join_frame, text='Join', command=self.send_join_room).pack(side='left', padx=5)

    def send_join_room(self):
        room = self.room_entry.get().strip()
        if not room:
            messagebox.showerror('Error', 'Please enter a room number.')
            return
        self.join_frame.pack_forget()
        threading.Thread(target=self.room_flow, args=('join', room), daemon=True).start()

    def room_flow(self, mode, room=None):
        try:
            self.client.settimeout(120)
            data = self.client.recv(1024).decode()
            if data.startswith('Do you want to start'):
                self.client.sendall(mode.encode())
                data = self.client.recv(1024).decode()
                if mode == 'new':
                    if data.startswith('Your new room number is:'):
                        self.room_name = data.split(':')[1].strip()
                        self.status_label.config(text=f'Room: {self.room_name} | Waiting for opponent...')
                    else:
                        self.status_label.config(text=data)
                        return
                elif mode == 'join':
                    if data.startswith('Enter room number:'):
                        self.client.sendall(room.encode())
                        self.room_name = room
                        self.status_label.config(text=f'Room: {self.room_name} | Waiting for opponent...')
                    else:
                        self.status_label.config(text=data)
                        return
            self.client.settimeout(None)
            self.wait_for_game()
        except Exception as e:
            messagebox.showerror('Error', f'Connection error: {e}')
            self.root.destroy()

    def wait_for_game(self):
        board_created = False
        while True:
            try:
                data = self.client.recv(1024).decode()
                print(f"[Client] Received: {repr(data)}")
            except Exception as e:
                print(f"[Client] Socket error: {e}")
                break
            if not data:
                print("[Client] Empty data received, closing.")
                break
            # Split multiple messages if received together
            messages = data.split('\n')
            for msg in messages:
                msg = msg.strip()
                if not msg:
                    continue
                print(f"[Client] Handling message: {repr(msg)}")
                if msg.startswith('OPPONENT_JOINED'):
                    self.status_label.config(text=f'Room: {self.room_name} | Opponent joined!')
                    messagebox.showinfo('Game Start', 'Opponent has joined! Game is starting.')
                elif msg.startswith('WELCOME'):
                    try:
                        self.player_id = int(msg.split(':')[1])
                        self.symbol = "X" if self.player_id == 0 else "O"
                        self.status_label.config(text=f'Room: {self.room_name} | You are {self.symbol}')
                        if not board_created:
                            self.create_board()
                            board_created = True
                    except Exception as e:
                        print(f"[Client] Error parsing WELCOME: {e}")
                elif len(msg) == 9 and set(msg).issubset({'X','O',' '}):
                    self.board = list(msg)
                    self.status_label.config(text=f'Room: {self.room_name} | You are {self.symbol} | Game started!')
                    self.update_board()
                elif msg.startswith('WINNER'):
                    winner = msg.split(':')[1]
                    self.status_label.config(text=f'Game Over! Winner: {winner}')
                    messagebox.showinfo('Game Over', f'Winner: {winner}')
                    return
                elif msg == 'DRAW':
                    self.status_label.config(text="Game Over! It's a draw.")
                    messagebox.showinfo('Game Over', "It's a draw.")
                    return
                elif msg == 'INVALID':
                    messagebox.showinfo('Invalid Move', 'Invalid move. Try again.')
                elif msg == 'YOUR_TURN':
                    self.my_turn = True
                    self.status_label.config(text=f'Room: {self.room_name} | You are {self.symbol} | Your turn!')
                elif msg == 'Room full. Try another room.':
                    self.status_label.config(text='Room full. Try another room.')
                    messagebox.showerror('Room Full', 'Room is full. Try another room.')
                    return
                else:
                    print(f"[Client] Unhandled message: {repr(msg)}")
                    self.status_label.config(text=f'Room: {self.room_name} | Waiting for opponent...')
        try:
            self.client.close()
        except Exception as e:
            print(f"[Client] Error closing socket: {e}")

    def create_board(self):
        if self.board_frame:
            self.board_frame.destroy()
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.board_frame, text=' ', width=6, height=3,
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

    def on_close(self):
        try:
            if self.client:
                self.client.close()
        except:
            pass
        self.root.destroy()

if __name__ == '__main__':
    TicTacToeClientGUI()
