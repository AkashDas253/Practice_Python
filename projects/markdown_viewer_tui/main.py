

from textual.app import App, ComposeResult, Screen
from textual.widgets import Static, ListView, ListItem, Label
from textual.containers import VerticalScroll
from rich.markdown import Markdown
import sys
import os

class FilePickerScreen(Screen):
    def __init__(self, folder, **kwargs):
        super().__init__(**kwargs)
        self.folder = folder
        self.file_list = [f for f in os.listdir(folder) if f.lower().endswith('.md')]
        self.selected_index = 0

    def compose(self) -> ComposeResult:
        yield Static("Select a markdown file (use ↑/↓ and Enter):")
        yield ListView(*[ListItem(Label(f)) for f in self.file_list], id="file-list")

    def on_mount(self):
        self.query_one("#file-list", ListView).index = self.selected_index

    def on_key(self, event):
        list_view = self.query_one("#file-list", ListView)
        if event.key == "up":
            self.selected_index = max(0, self.selected_index - 1)
            list_view.index = self.selected_index
        elif event.key == "down":
            self.selected_index = min(len(self.file_list) - 1, self.selected_index + 1)
            list_view.index = self.selected_index
        elif event.key == "enter":
            idx = self.selected_index
            if 0 <= idx < len(self.file_list):
                md_path = os.path.join(self.folder, self.file_list[idx])
                self.app.push_screen(MarkdownScreen(md_path))
        elif event.key in ("q", "Q"):
            self.app.exit()

class MarkdownScreen(Screen):
    def __init__(self, md_path, **kwargs):
        super().__init__(**kwargs)
        self.md_path = md_path
        self.markdown_content = ""
        if self.md_path and os.path.exists(self.md_path):
            with open(self.md_path, "r", encoding="utf-8") as f:
                self.markdown_content = f.read()

    def compose(self) -> ComposeResult:
        if self.markdown_content:
            yield VerticalScroll(Static(Markdown(self.markdown_content)))
        else:
            yield Static("No markdown file loaded.")

    def on_key(self, event):
        if event.key in ("q", "Q"):
            self.app.exit()
        elif event.key == "escape" or event.key == "e":
            self.app.pop_screen()

class MainApp(App):
    CSS_PATH = None

    def __init__(self, folder=None, **kwargs):
        super().__init__(**kwargs)
        self.folder = folder or os.getcwd()

    def on_mount(self):
        self.push_screen(FilePickerScreen(self.folder))

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else None
    app = MainApp(folder=folder)
    app.run()
