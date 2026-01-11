import tkinter as tk
from tkinter import ttk
import cv2
import os
import sys
import time
import datetime
from PIL import Image, ImageTk
from filters import FilterLibrary

class RealTimePipeline:
    def __init__(self, root):
        self.root = root
        self.root.title("Modular Filter Engine")
        
        self.base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.snapshot_path = os.path.join(self.base_path, "snapshots")
        if not os.path.exists(self.snapshot_path):
            os.makedirs(self.snapshot_path)

        self.cap = cv2.VideoCapture(0)
        self.prev_time = time.time()
        self.last_frame = None
        
        self.available_filters = {
            "Grayscale": FilterLibrary.grayscale,
            "Gaussian Blur": FilterLibrary.blur,
            "Canny Edges": FilterLibrary.edges,
            "Invert Colors": FilterLibrary.invert,
            "Posterize": FilterLibrary.posterize,
            "Sepia Tone": FilterLibrary.sepia,
            "Thermal Vision": FilterLibrary.thermal,
            "Sketch Mode": FilterLibrary.sketch,
            "Cartoonify": FilterLibrary.cartoon,
            "Live Histogram": FilterLibrary.histogram_overlay,
            "Pixelate": FilterLibrary.pixelate,
            "Sharpen": FilterLibrary.sharpen,
            "HSV Hue Shift": FilterLibrary.hsv_shift,
            "Adaptive Threshold": FilterLibrary.adaptive_threshold,
            "Emboss": FilterLibrary.emboss
        }
        
        self.active_pipeline = []
        self.setup_ui()
        self.update_frame()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=640, height=480, bg="#1a1a1a")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.ctrl_panel = ttk.Frame(self.root, padding="10")
        self.ctrl_panel.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(self.ctrl_panel, text="Step 1: Choose Filter", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        self.filter_listbox = tk.Listbox(self.ctrl_panel, height=10, exportselection=False)
        for name in sorted(self.available_filters.keys()):
            self.filter_listbox.insert(tk.END, name)
        self.filter_listbox.pack(fill=tk.X, pady=5)
        
        ttk.Button(self.ctrl_panel, text="Add Filter >>", command=self.add_filter).pack(fill=tk.X, pady=2)
        ttk.Separator(self.ctrl_panel, orient='horizontal').pack(fill='x', pady=15)

        ttk.Label(self.ctrl_panel, text="Step 2: Sequence Order", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        self.pipeline_listbox = tk.Listbox(self.ctrl_panel, height=8, selectmode=tk.SINGLE)
        self.pipeline_listbox.pack(fill=tk.X, pady=5)

        nav_frame = ttk.Frame(self.ctrl_panel)
        nav_frame.pack(fill=tk.X)
        ttk.Button(nav_frame, text="▲ Up", command=lambda: self.move_filter(-1)).pack(side=tk.LEFT, expand=True)
        ttk.Button(nav_frame, text="▼ Down", command=lambda: self.move_filter(1)).pack(side=tk.LEFT, expand=True)
        
        ttk.Button(self.ctrl_panel, text="Remove Selected", command=self.remove_filter).pack(fill=tk.X, pady=(10,2))
        ttk.Button(self.ctrl_panel, text="Reset All", command=self.reset_pipeline).pack(fill=tk.X, pady=2)
        
        ttk.Separator(self.ctrl_panel, orient='horizontal').pack(fill='x', pady=15)
        ttk.Button(self.ctrl_panel, text="SAVE SNAPSHOT", command=self.take_snapshot).pack(fill=tk.X, ipady=5)
        
        self.status_lbl = ttk.Label(self.ctrl_panel, text=f"Folder: snapshots/", foreground="gray", font=("Arial", 8))
        self.status_lbl.pack(pady=5)

    def add_filter(self):
        selection = self.filter_listbox.curselection()
        if selection:
            name = self.filter_listbox.get(selection[0])
            self.active_pipeline.append(name)
            self.pipeline_listbox.insert(tk.END, name)

    def remove_filter(self):
        idx = self.pipeline_listbox.curselection()
        if idx:
            self.active_pipeline.pop(idx[0])
            self.pipeline_listbox.delete(idx[0])

    def reset_pipeline(self):
        self.active_pipeline.clear()
        self.pipeline_listbox.delete(0, tk.END)

    def move_filter(self, direction):
        idx = self.pipeline_listbox.curselection()
        if not idx: return
        old_idx = idx[0]
        new_idx = old_idx + direction
        if 0 <= new_idx < len(self.active_pipeline):
            self.active_pipeline[old_idx], self.active_pipeline[new_idx] = \
                self.active_pipeline[new_idx], self.active_pipeline[old_idx]
            name = self.pipeline_listbox.get(old_idx)
            self.pipeline_listbox.delete(old_idx)
            self.pipeline_listbox.insert(new_idx, name)
            self.pipeline_listbox.selection_set(new_idx)

    def take_snapshot(self):
        if self.last_frame is not None:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snap_{ts}.png"
            full_path = os.path.join(self.snapshot_path, filename)
            
            cv2.imwrite(full_path, cv2.cvtColor(self.last_frame, cv2.COLOR_RGB2BGR))
            
            log_path = os.path.join(self.snapshot_path, "manifest.log")
            pipeline_str = " -> ".join(self.active_pipeline) if self.active_pipeline else "None"
            
            with open(log_path, "a") as f:
                f.write(f"[{ts}] File: {filename} | Filters: {pipeline_str}\n")
            
            self.status_lbl.config(text=f"Saved: {filename}", foreground="#00ff00")
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            for filter_name in self.active_pipeline:
                try:
                    frame = self.available_filters[filter_name](frame)
                except Exception as e:
                    print(f"Filter Error ({filter_name}): {e}")
            self.last_frame = frame
            now = time.time()
            fps = 1 / (now - self.prev_time)
            self.prev_time = now
            cv2.putText(frame, f"FPS: {int(fps)}", (15, 30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 1)
            self.img_tk = ImageTk.PhotoImage(Image.fromarray(frame))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
        self.root.after(10, self.update_frame)