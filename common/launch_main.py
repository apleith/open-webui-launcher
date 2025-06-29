"""
Main launcher integrates splash screen and orchestrator
for Open WebUI Assistant.
"""
import threading
import os
from pathlib import Path
from common.splash_screen import SplashScreen
from common.launch_webui_assistant import main as orchestrator_main

def main():
	# Prepare log directory
	base = os.getenv('LOCALAPPDATA') or str(Path.home())
	log_dir = Path(base) / 'OpenWebUIAssistant' / 'logs'
	log_dir.mkdir(parents=True, exist_ok=True)
	log_path = log_dir / 'assistant.log'

	# Show splash screen
	splash = SplashScreen(log_path)

	# Run orchestrator in background; close splash when done
	def runner():
		orchestrator_main()
		splash.root.after(0, splash.close)

	worker = threading.Thread(target=runner, daemon=True)
	worker.start()

	# Enter Tk main loop until splash.close() is called
	splash.root.mainloop()
	worker.join()

if __name__ == '__main__':
	main()
