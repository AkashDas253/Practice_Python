# AI-Powered Flashcard App

A simple offline flashcard application with spaced repetition and basic AI features, built in Python. Supports CLI and can be extended with a GUI.


## Features
- Add, review, and tag flashcards
- Spaced repetition (intervals in hours)
- AI-suggested flashcard (prioritizes cards you're likely to forget)
- Fuzzy logic support (score field for adaptive review)
- Simple GUI built with Tkinter


## How to Use
### CLI
1. Run `main.py` to start the app.
2. Use the menu to add, review, or get AI-suggested flashcards.
3. Flashcards are stored in `flashcards.json`.
4. You can edit or import/export flashcards as needed.

### GUI
1. Run `gui.py` to launch the graphical interface.
2. Use buttons to add, review, or get AI-suggested flashcards.
3. All features from the CLI are available in the GUI.

## Project Structure
```
ai_powered_flashcard/
    main.py
    flashcard_core.py
    flashcards.json
    readme.md
```

## AI Logic
The app uses simple AI logic to suggest which flashcard you should review next:
- Each card has an `interval` (hours between reviews) and a `score` (tracks how often you get it right or wrong).
- When you choose "AI-suggested flashcard," the app picks the card with the lowest interval and longest time since last review, or highest score (most often wrong).
- The `score` field is updated: +1 for wrong, -1 for right. Cards with higher scores are prioritized for review.
- This is a basic form of fuzzy logic, adapting to your learning pattern.


## GUI Details
- The GUI is built with Tkinter and provides buttons for all main actions.
- The core logic is in `flashcard_core.py` for easy integration and extension.

## Example Flashcard JSON
```json
[
  {
    "question": "What is the capital of France?",
    "answer": "Paris",
    "tags": ["geography", "europe"],
    "last_reviewed": null,
    "interval": 1,
    "score": 0
  }
]
```

## Requirements
- Python 3.x
- Tkinter (usually included with Python standard library)

## Installation & Usage
1. Clone or download this repository.
2. Install Python 3.x from https://www.python.org/ if not already installed.
3. (Optional) Create a virtual environment: `python -m venv venv`
4. Run `main.py` for CLI or `gui.py` for GUI.
5. Flashcards are stored in `flashcards.json`.

## License
MIT
