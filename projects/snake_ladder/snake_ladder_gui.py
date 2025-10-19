import tkinter as tk
import random

BOARD_SIZE = 100
SNAKES = {
    16: 6,
    47: 26,
    49: 11,
    56: 53,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    98: 78
}
LADDERS = {
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    80: 100
}

class SnakeLadderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladder Game")
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()
        self.draw_board()
        self.positions = [0, 0]
        self.player_names = ["Player 1", "Player 2"]
        self.turn = 0
        self.status = tk.Label(root, text=f"{self.player_names[self.turn]}'s turn")
        self.status.pack()
        self.roll_btn = tk.Button(root, text="Roll Dice", command=self.roll_dice)
        self.roll_btn.pack()
        self.dice_label = tk.Label(root, text="Dice: ")
        self.dice_label.pack()
        self.player_labels = [
            tk.Label(root, text=f"Player 1 Position: 0"),
            tk.Label(root, text=f"Player 2 Position: 0")
        ]
        self.player_labels[0].pack()
        self.player_labels[1].pack()
        self.player_icons = [None, None]
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
        if self.positions[self.turn] == 100:
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
        if pos == 100:
            self.status.config(text=f"{self.player_names[self.turn]} wins!")
            self.roll_btn.config(state=tk.DISABLED)
        else:
            self.turn = 1 - self.turn
            self.status.config(text=f"{self.player_names[self.turn]}'s turn")

    def update_players(self):
        for i in range(2):
            if self.player_icons[i]:
                self.canvas.delete(self.player_icons[i])
            coords = self.get_coords(self.positions[i] if self.positions[i] > 0 else 1)
            color = "blue" if i == 0 else "orange"
            self.player_icons[i] = self.canvas.create_oval(
                coords[0]-15, coords[1]-15, coords[0]+15, coords[1]+15,
                fill=color, outline="black"
            )

def main():
    root = tk.Tk()
    app = SnakeLadderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
