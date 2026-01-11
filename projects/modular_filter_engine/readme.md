# Modular Filter Engine

A real-time computer vision application that applies a sequential image-processing pipeline to a live webcam feed. This tool allows for dynamic layering of filters using a modular GUI built with Python, OpenCV, and Tkinter.

---

## Getting Started

### 1. Prerequisites

This application requires a local Python environment with a physical webcam. It will not work on headless servers or cloud IDEs (like Google Colab) as it requires a GUI window and local hardware access.

### 2. Installation

Install the required dependencies using pip:

```bash
pip install opencv-python numpy pillow

```

### 3. Running the Application

Ensure all three project files (`main.py`, `engine.py`, `filters.py`) are in the same folder, then execute:

```bash
python main.py

```

---

## How to Use

1. **Initialize**: The webcam feed appears on the left upon launch.
2. **Add Filters**: Select an effect from the list and click **Add Filter**. You can stack multiple effects.
3. **Manage Pipeline**:
* **Up/Down**: Change the processing order. The sequence significantly impacts the final result.
* **Remove/Reset**: Delete specific steps or clear the entire stack.


4. **Capture**: Click **SAVE SNAPSHOT** to export the current frame and log the metadata.

---

## Features

### Filter Categories

| Category | Filters Included |
| --- | --- |
| **Artistic** | Sketch, Cartoonify, Posterize, Sepia, Emboss |
| **Technical** | Canny Edges, Adaptive Threshold, Live Histogram |
| **Correction** | Sharpen, Gaussian Blur, Grayscale, Pixelate |
| **Color Space** | HSV Hue Shift, Thermal Vision, Invert Colors |

### Snapshot & Logging System

* **Storage**: Captures are saved in the `/snapshots` folder.
* **Naming**: Files use the `snap_YYYYMMDD_HHMMSS.png` format.
* **Manifest**: Every snapshot is logged in `manifest.log`, recording the timestamp and the exact filter sequence used (e.g., `Grayscale -> Pixelate`).

---

## Technical Architecture

### Sequential Processing Loop

The engine uses a "Pipeline" approach where the output of one filter becomes the input of the next.

### Modular Structure

* **`filters.py`**: Pure image processing logic. No GUI dependencies.
* **`engine.py`**: Handles the UI, webcam lifecycle, and the processing loop.
* **`main.py`**: Entry point that initializes the Tkinter root and theme.

---

## Extension Guide

To add a new filter:

1. **Logic**: Add a `@staticmethod` to `FilterLibrary` in `filters.py` that accepts and returns a frame.
2. **Registry**: Add the method to the `self.available_filters` dictionary in `engine.py`.

---