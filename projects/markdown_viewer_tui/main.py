from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import VerticalScroll
from rich.markdown import Markdown
import sys
import os



class MarkdownViewer(App):
    CSS_PATH = None

    def __init__(self, md_path=None, **kwargs):
        super().__init__(**kwargs)
        self.md_path = md_path
        self.markdown_content = ""
        # Load markdown content immediately
        with open("debug.log", "a", encoding="utf-8") as log:
            log.write(f"[DEBUG] md_path: {self.md_path}\n")
            if self.md_path:
                log.write(f"[DEBUG] Exists: {os.path.exists(self.md_path)}\n")
        if self.md_path and os.path.exists(self.md_path):
            with open(self.md_path, "r", encoding="utf-8") as f:
                self.markdown_content = f.read()

    def compose(self) -> ComposeResult:
        if self.markdown_content:
            yield VerticalScroll(Static(Markdown(self.markdown_content)))
        else:
            yield Static("No markdown file loaded.")

    def on_mount(self):
        pass

    def on_key(self, event):
        if event.key in ("q", "Q"):
            self.exit()

if __name__ == "__main__":
    md_file = sys.argv[1] if len(sys.argv) > 1 else None
    app = MarkdownViewer(md_path=md_file)
    app.run()
