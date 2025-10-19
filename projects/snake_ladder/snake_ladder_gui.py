import tkinter as tk
from tkinter import colorchooser, messagebox
import random

BOARD_SIZE = 100
SNAKES = {
    16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78
}
LADDERS = {
    1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100
}

DEFAULT_COLORS = ["blue", "orange", "green", "purple"]

class SetupScreen:
    def __init__(self, root, start_callback):
        self.root = root
        self.start_callback = start_callback
        self.frame = tk.Frame(root)
        self.frame.pack(pady=30)
        tk.Label(self.frame, text="Snake and Ladder Setup", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.frame, text="Select number of players (2-4):").pack()
        self.player_count_var = tk.IntVar(value=2)
        self.count_menu = tk.OptionMenu(self.frame, self.player_count_var, 2, 3, 4, command=self.update_colors)
        self.count_menu.pack()
        self.color_vars = []
        self.color_buttons = []
        self.colors_frame = tk.Frame(self.frame)
        self.colors_frame.pack(pady=10)
        self.update_colors(2)
        self.start_btn = tk.Button(self.frame, text="Start Game", command=self.start_game)
        self.start_btn.pack(pady=10)

    def update_colors(self, count):
        for btn in self.color_buttons:
            btn.destroy()
        self.color_vars = []
        self.color_buttons = []
        for i in range(self.player_count_var.get()):
            var = tk.StringVar(value=DEFAULT_COLORS[i % len(DEFAULT_COLORS)])
            self.color_vars.append(var)
            btn = tk.Button(self.colors_frame, text=f"Player {i+1} Color", bg=var.get(), command=lambda idx=i: self.choose_color(idx))
            btn.grid(row=0, column=i, padx=5)
            self.color_buttons.append(btn)

    def choose_color(self, idx):
        color = colorchooser.askcolor(title=f"Choose color for Player {idx+1}")[1]
        if color:
            self.color_vars[idx].set(color)
            self.color_buttons[idx].config(bg=color)

    def start_game(self):
        colors = [var.get() for var in self.color_vars]
        if len(set(colors)) < len(colors):
            messagebox.showerror("Color Error", "Each player must have a unique color.")
            return
        self.frame.destroy()
        self.start_callback(self.player_count_var.get(), colors)


class SnakeLadderGUI:
    def __init__(self, root, player_count=2, player_colors=None):
        self.root = root
        self.root.title("Snake and Ladder Game")
        self.player_count = player_count
        self.player_colors = player_colors or DEFAULT_COLORS[:player_count]
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()
        self.draw_board()
        self.positions = [0] * player_count
        self.player_names = [f"Player {i+1}" for i in range(player_count)]
        self.turn = 0
        self.finished = [False] * player_count
        self.ranking = []  # List of (player_index, player_name)
        self.status = tk.Label(root, text=f"{self.player_names[self.turn]}'s turn")
        self.status.pack()
        self.roll_btn = tk.Button(root, text="Roll Dice", command=self.roll_dice)
        self.roll_btn.pack()
        self.dice_label = tk.Label(root, text="Dice: ")
        self.dice_label.pack()
        self.player_labels = [tk.Label(root, text=f"{self.player_names[i]} Position: 0") for i in range(player_count)]
        for lbl in self.player_labels:
            lbl.pack()
        self.player_icons = [None] * player_count
        self.update_players()

    def draw_board(self):
        size = 50
        for i in range(10):
            for j in range(10):
                num = 100 - (i * 10 + (9-j if i%2==0 else j))
                x0, y0 = j*size, i*size
                x1, y1 = x0+size, y0+size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                self.canvas.create_text(x0+size/2, y0+size/2, text=str(num))
        # Draw snakes
        for head, tail in SNAKES.items():
            self.draw_line(head, tail, "red")
        # Draw ladders
        for start, end in LADDERS.items():
            self.draw_line(start, end, "green")

    def get_coords(self, pos):
        if pos < 1 or pos > 100:
            return None
        pos -= 1
        row = pos // 10
        col = pos % 10
        if row % 2 == 0:
            col = 9 - col
        x = col * 50 + 25
        y = (9 - row) * 50 + 25
        return x, y

    def draw_line(self, start, end, color):
        start_coords = self.get_coords(start)
        end_coords = self.get_coords(end)
        if start_coords and end_coords:
            self.canvas.create_line(*start_coords, *end_coords, fill=color, width=3, arrow=tk.LAST)

    def roll_dice(self):
        # Skip finished players
        if self.finished[self.turn]:
            self.next_turn()
            return
        roll = random.randint(1, 6)
        self.dice_label.config(text=f"Dice: {roll}")
        pos = self.positions[self.turn] + roll
        if pos > 100:
            pos = 100 - (pos - 100)
        if pos in SNAKES:
            self.status.config(text=f"Oops! Bitten by a snake at {pos}. Go down to {SNAKES[pos]}")
            pos = SNAKES[pos]
        elif pos in LADDERS:
            self.status.config(text=f"Yay! Climbed a ladder at {pos}. Go up to {LADDERS[pos]}")
            pos = LADDERS[pos]
        else:
            self.status.config(text=f"{self.player_names[self.turn]} moved to {pos}")
        self.positions[self.turn] = pos
        self.player_labels[self.turn].config(text=f"{self.player_names[self.turn]} Position: {pos}")
        self.update_players()
        if pos == 100 and not self.finished[self.turn]:
            self.finished[self.turn] = True
            self.ranking.append(self.turn)
            rank = len(self.ranking)
            self.status.config(text=f"{self.player_names[self.turn]} finished! Rank: {rank}")
            if all(self.finished):
                self.show_ranking()
                self.roll_btn.config(state=tk.DISABLED)
                return
        self.next_turn()

    def next_turn(self):
        # Find next unfinished player
        for _ in range(self.player_count):
            self.turn = (self.turn + 1) % self.player_count
            if not self.finished[self.turn]:
                break
        if not all(self.finished):
            self.status.config(text=f"{self.player_names[self.turn]}'s turn")

    def show_ranking(self):
        ranking_text = "\n".join([
            f"{i+1}. {self.player_names[idx]}" for i, idx in enumerate(self.ranking)
        ])
        messagebox.showinfo("Game Over", f"Final Ranking:\n{ranking_text}")

    def update_players(self):
        for i in range(self.player_count):
            if self.player_icons[i]:
                self.canvas.delete(self.player_icons[i])
            coords = self.get_coords(self.positions[i] if self.positions[i] > 0 else 1)
            color = self.player_colors[i]
            self.player_icons[i] = self.canvas.create_oval(
                coords[0]-15, coords[1]-15, coords[0]+15, coords[1]+15,
                fill=color, outline="black"
            )

def main():
    root = tk.Tk()
    def start_game(player_count, player_colors):
        SnakeLadderGUI(root, player_count, player_colors)
    SetupScreen(root, start_game)
    root.mainloop()

if __name__ == "__main__":
    main()
