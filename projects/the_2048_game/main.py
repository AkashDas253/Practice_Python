import tkinter as tk
import random

SIZE = 4
NEW_TILE_VALUES = [2, 4]

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.cells = [[None] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.setup_ui()
        self.start_game()
        self.master.bind("<Key>", self.key_handler)

    def setup_ui(self):
        frame = tk.Frame(self.master, bg="#bbada0")
        frame.grid()
        for i in range(SIZE):
            for j in range(SIZE):
                cell = tk.Label(frame, text="", width=4, height=2, font=("Arial", 24, "bold"),
                                bg="#cdc1b4", fg="#776e65", borderwidth=2, relief="ridge")
                cell.grid(row=i, column=j, padx=5, pady=5)
                self.cells[i][j] = cell
        self.score_label = tk.Label(self.master, text="Score: 0", font=("Arial", 16))
        self.score_label.grid(row=1, column=0, columnspan=SIZE)

    def start_game(self):
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()

    def add_new_tile(self):
        empty = [(i, j) for i in range(SIZE) for j in range(SIZE) if self.board[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = random.choice(NEW_TILE_VALUES)

    def update_ui(self):
        for i in range(SIZE):
            for j in range(SIZE):
                value = self.board[i][j]
                self.cells[i][j].config(text=str(value) if value else "", bg=self.get_bg_color(value))
        self.score_label.config(text=f"Score: {self.score}")

    def get_bg_color(self, value):
        colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
            32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", 512: "#edc850",
            1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#3c3a32")

    def key_handler(self, event):
        key = event.keysym
        moved = False
        if key == "Up":
            moved = self.move_up()
        elif key == "Down":
            moved = self.move_down()
        elif key == "Left":
            moved = self.move_left()
        elif key == "Right":
            moved = self.move_right()
        if moved:
            self.add_new_tile()
            self.update_ui()
            if self.is_game_over():
                self.game_over()

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        moved = False
        for i in range(SIZE):
            original = list(self.board[i])
            row = self.compress(self.board[i])
            row = self.merge(row)
            row = self.compress(row)
            self.board[i] = row
            if self.board[i] != original:
                moved = True
        return moved

    def move_right(self):
        moved = False
        for i in range(SIZE):
            original = list(self.board[i])
            row = self.board[i][::-1]
            row = self.compress(row)
            row = self.merge(row)
            row = self.compress(row)
            self.board[i] = row[::-1]
            if self.board[i] != original:
                moved = True
        return moved

    def move_up(self):
        moved = False
        for j in range(SIZE):
            col = [self.board[i][j] for i in range(SIZE)]
            original = list(col)
            col = self.compress(col)
            col = self.merge(col)
            col = self.compress(col)
            for i in range(SIZE):
                self.board[i][j] = col[i]
            if [self.board[i][j] for i in range(SIZE)] != original:
                moved = True
        return moved

    def move_down(self):
        moved = False
        for j in range(SIZE):
            col = [self.board[i][j] for i in range(SIZE)][::-1]
            original = [self.board[i][j] for i in range(SIZE)]
            col = self.compress(col)
            col = self.merge(col)
            col = self.compress(col)
            col = col[::-1]
            for i in range(SIZE):
                self.board[i][j] = col[i]
            if [self.board[i][j] for i in range(SIZE)] != original:
                moved = True
        return moved

    def is_game_over(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == 0:
                    return False
        for i in range(SIZE):
            for j in range(SIZE - 1):
                if self.board[i][j] == self.board[i][j + 1]:
                    return False
        for j in range(SIZE):
            for i in range(SIZE - 1):
                if self.board[i][j] == self.board[i + 1][j]:
                    return False
        return True

    def game_over(self):
        over = tk.Toplevel(self.master)
        over.title("Game Over")
        tk.Label(over, text=f"Game Over!\nScore: {self.score}", font=("Arial", 18)).pack(padx=20, pady=20)
        tk.Button(over, text="Restart", command=lambda: [over.destroy(), self.restart()]).pack(pady=10)

    def restart(self):
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.start_game()
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
