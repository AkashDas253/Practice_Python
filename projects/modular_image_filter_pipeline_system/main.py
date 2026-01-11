import tkinter as tk
from tkinter import ttk
from engine import RealTimePipeline

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    if 'clam' in style.theme_names():
        style.theme_use('clam')
    
    app = RealTimePipeline(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.cap.release(), root.destroy()))
    root.mainloop()