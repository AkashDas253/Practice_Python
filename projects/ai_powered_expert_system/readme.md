# Food Recommendation Expert System

This is a simple expert system app built with Python and experta. It recommends dishes from a configurable menu based on user preferences and allergies, using rule-based inference.

## Features
- Configurable menu (JSON)
- User input for taste, type, region, and multiple allergies (comma-separated)
- Dishes are recommended based on match accuracy
- Dishes containing any allergy ingredient (even partial match) are excluded
- Detailed dish info and explanation for each recommendation

## Setup Instructions

1. **Clone or copy the project files.**
2. **Create and activate a Python virtual environment (optional but recommended):**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Run the app:**
   ```powershell
   python main.py
   ```

## Usage
- Enter your preferences when prompted (leave blank to skip any field).
- For allergies, enter a comma-separated list (e.g., `peanut, butter`).
- The app will recommend suitable dishes and explain the reasoning for each.

## Files
- `main.py`: Main application logic
- `menu_config.json`: Sample menu configuration
- `requirements.txt`: Python dependencies

## Requirements
- Python 3.10 or newer
- experta
- frozendict==1.2 (experta requires this version)

---
