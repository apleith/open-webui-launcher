"""
Splash Screen UI for Open WebUI Assistant.
Displays splash_image.png as background, overlays live status,
and sets the window icon to logo.ico.
Keeps itself always-on-top until explicitly closed.
"""
import sys
import tkinter as tk
from pathlib import Path

class SplashScreen:
	def __init__(self, log_path):
		self.root = tk.Tk()
		self.root.overrideredirect(True)
		# Keep on top
		self.root.lift()
		self.root.attributes('-topmost', True)

		# Locate resources
		if getattr(sys, 'frozen', False):
			base = Path(sys._MEIPASS) / 'common'
		else:
			base = Path(__file__).parent

		# set window icon
		ico_path = base / 'logo.ico'
		if ico_path.exists():
			try:
				# for Windows .ico
				self.root.iconbitmap(str(ico_path))
			except Exception:
				pass

		# background image
		img_path = base / 'splash_image.png'
		self.bg_image = tk.PhotoImage(file=str(img_path))
		w, h = self.bg_image.width(), self.bg_image.height()

		# Center window
		x = (self.root.winfo_screenwidth() - w) // 2
		y = (self.root.winfo_screenheight() - h) // 2
		self.root.geometry(f"{w}x{h}+{x}+{y}")

		# Canvas & background
		self.canvas = tk.Canvas(self.root, width=w, height=h, highlightthickness=0)
		self.canvas.pack()
		self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image)

		# Ensure log exists
		self.log_path = Path(log_path)
		self.log_path.parent.mkdir(parents=True, exist_ok=True)
		self.log_path.touch(exist_ok=True)

		# Overlay status text
		cream = '#FBF1C7'
		self.text_id = self.canvas.create_text(
			w//2, h-40,
			text="Starting…",
			fill=cream,
			font=("Arial", 14, "bold")
		)

		# Draggable window
		self._drag = {"x": 0, "y": 0}
		self.root.bind("<ButtonPress-1>", self.on_press)
		self.root.bind("<B1-Motion>",	self.on_drag)

		# begin updating status
		self.update()

	def on_press(self, event):
		self._drag["x"], self._drag["y"] = event.x, event.y

	def on_drag(self, event):
		x = self.root.winfo_x() + event.x - self._drag["x"]
		y = self.root.winfo_y() + event.y - self._drag["y"]
		self.root.geometry(f"+{x}+{y}")

	def update(self):
		# re-ensure topmost
		self.root.lift()
		self.root.attributes('-topmost', True)

		try:
			lines = self.log_path.read_text().splitlines()
			if lines:
				last = lines[-1]
				if "] " in last:
					msg = last.split("] ", 1)[1]
				else:
					msg = last
				self.canvas.itemconfig(self.text_id, text=msg)
		except Exception:
			pass

		self.root.after(500, self.update)

	def close(self):
		self.root.destroy()

if __name__ == "__main__":
	import os
	log = os.path.join(
		os.getenv('LOCALAPPDATA', os.getcwd()),
		'OpenWebUIAssistant','logs','assistant.log'
	)
	splash = SplashScreen(log)
	splash.root.mainloop()
