import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import threading
import time
import os
from pathlib import Path
import platform

# Configuration
BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "assistant.log"
IMAGE_PATH = BASE_DIR / "splash_image.png"
DONE_FLAG = BASE_DIR / ".splash_done"
LAUNCH_SCRIPT = BASE_DIR / "launch_webui_assistant.py"
IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"

# Track mouse dragging for window movement
def start_move(event):
	splash.x = event.x
	splash.y = event.y

def do_move(event):
	x = event.x_root - splash.x
	y = event.y_root - splash.y
	splash.geometry(f"800x450+{x}+{y}")

# Launch assistant in background
def run_launcher():
	with open(LOG_FILE, "a", encoding="utf-8") as log:
		process = subprocess.Popen(["python", str(LAUNCH_SCRIPT)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
		for line in process.stdout:
			log.write(line)
			log.flush()
			if "All systems ready" in line:
				DONE_FLAG.touch()
				break

# Update status label and check for done flag
def update_status():
	try:
		with open(LOG_FILE, "r", encoding="utf-8") as f:
			lines = f.readlines()
			if lines:
				status_label.config(text=lines[-1].strip())
	except Exception as e:
		status_label.config(text=f"[Error reading log: {e}]")
	if DONE_FLAG.exists():
		splash.destroy()
	else:
		splash.after(1000, update_status)

# UI Setup
splash = tk.Tk()
splash.title("Launching WebUI Assistant")
splash.geometry("800x450")
splash.overrideredirect(True)

# Center window
splash.update_idletasks()
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (450 // 2)
splash.geometry(f"800x450+{x}+{y}")

# Image background
if IMAGE_PATH.exists():
	bg_img = Image.open(IMAGE_PATH).resize((800, 450))
	bg_photo = ImageTk.PhotoImage(bg_img)
	bg_label = tk.Label(splash, image=bg_photo)
	bg_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
	splash.configure(bg="black")

# Draggable window
splash.bind("<Button-1>", start_move)
splash.bind("<B1-Motion>", do_move)

# Status bar
status_label = tk.Label(splash, text="Initializing...", font=("Arial", 12), bg="#1a1d1f", fg="#f2ecdb")
status_label.pack(side="bottom", pady=10)

# Launch + update loop
threading.Thread(target=run_launcher, daemon=True).start()
splash.after(1000, update_status)
splash.mainloop()
