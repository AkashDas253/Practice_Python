# Markdown Viewer TUI

A simple terminal-based Markdown viewer built with the [Textual](https://textual.textualize.io/) framework.

## Features
- View markdown (`.md`) files in the terminal with formatting
- File picker to select markdown files from a folder
- Keyboard navigation:
  - `↑`/`↓` to move selection in file picker
  - `Enter` to open selected file
  - `q` or `Q` to quit
  - `Esc` or `e` to return to file picker from viewer

## Usage

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Place your markdown files in the same folder as `main.py` or specify a folder path.
3. Run the app:
   ```sh
   python main.py [folder_path]
   ```
   - If no folder is provided, the current directory is used.
   - Use the file picker to select a markdown file to view.

## Project Structure
- `main.py` — Main application entry point (TUI app)
- `readme.md` — Project documentation
- `test.md` — Example markdown file for testing
- `debug.log` — Debug log output
- `__pycache__/` — Python bytecode cache

## Example

To test the viewer, run:
```sh
python main.py
```
and select `test.md` from the file picker.

---

Built with [Textual](https://textual.textualize.io/) and [Rich](https://rich.readthedocs.io/).
