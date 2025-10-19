# Snake and Ladder Game (Python)

## Overview
This project is a classic Snake and Ladder game implemented in Python with a graphical user interface (GUI) using Tkinter.
All gameplay is handled through the GUI. The game supports 2–4 players, with custom color selection and automatic ranking based on the order players reach the end.

## How to Run

### GUI Version
1. Make sure you have Python installed (Tkinter is included by default).
2. Open a terminal and navigate to this folder.
3. Run:
   ```
   python snake_ladder_gui.py
   ```

## Features
- 2–4 player gameplay
- Each player can select their own token color before starting
- Snakes and ladders are visually represented on the board
- Dice roll button and player position display
- Players must roll the exact number to finish (no bounce-back)
- Automatic ranking: see the order in which players finish
- Win detection and final ranking popup

## Requirements
- Python 3.x
- Tkinter (comes with standard Python installation)

## Customization
You can modify the snakes and ladders positions in the code (`snake_ladder_gui.py`) for different board setups.
You can also change the default player colors or extend the game logic for more features.

## License
This project is for educational purposes.