# This file is for common/shared logic
# Keep this in /common/launch_webui_assistant.py

import subprocess
import sys
import os
import shutil
import webbrowser
import platform
import time
import requests
from pathlib import Path

IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"
DEFAULT_PORT = 3000
BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "assistant.log"
DONE_FLAG = BASE_DIR / ".splash_done"


def log(message):
	print(message)
	with open(LOG_FILE, "a", encoding="utf-8") as f:
		f.write(message + "\n")


def run_command(cmd, suppress_output=False):
	kwargs = {"shell": IS_WINDOWS}
	if suppress_output:
		kwargs["stdout"] = subprocess.DEVNULL
		kwargs["stderr"] = subprocess.DEVNULL
	try:
		result = subprocess.run(cmd, **kwargs)
		if result.returncode != 0:
			raise subprocess.CalledProcessError(result.returncode, cmd)
	except Exception as e:
		log("[X] Command failed: {}".format(' '.join(cmd)))
		log("    Error: {}".format(e))
		sys.exit(1)


def check_ollama():
	log("Checking Ollama...")
	if shutil.which("ollama") is None:
		log("[X] Ollama is not installed. Visit https://ollama.com/download")
		sys.exit(1)
	log("[OK] Ollama is installed.")


def detect_model():
	try:
		import pynvml
		pynvml.nvmlInit()
		handle = pynvml.nvmlDeviceGetHandleByIndex(0)
		mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
		gpu_mem = mem_info.total / (1024 ** 3)
	except:
		gpu_mem = 0
	if gpu_mem >= 42:
		return "deepseek-r1:70b"
	elif gpu_mem >= 19:
		return "deepseek-r1:32b"
	elif gpu_mem >= 9:
		return "deepseek-r1:14b"
	else:
		return "deepseek-r1:8b"


def pull_model(model_name):
	log(f"Pulling {model_name} model...")
	run_command(["ollama", "pull", model_name])


def ensure_docker_running():
	log("Checking Docker status...")
	if shutil.which("docker") is None:
		log("[X] Docker is not installed or not in PATH.")
		sys.exit(1)

	def docker_ready():
		try:
			out = subprocess.check_output(["docker", "system", "info"], stderr=subprocess.STDOUT)
			return b"Server Version" in out
		except subprocess.CalledProcessError as e:
			log("[!] Docker not responding: {}".format(e))
			return False

	if docker_ready():
		log("[OK] Docker is running.")
		return

	if IS_WINDOWS:
		docker_path = os.path.expandvars(r"%ProgramFiles%\Docker\Docker\Docker Desktop.exe")
		if not os.path.exists(docker_path):
			log("[X] Docker Desktop not found.")
			sys.exit(1)
		log("Starting Docker Desktop...")
		subprocess.Popen([docker_path])
		for i in range(30):
			if docker_ready():
				log("[OK] Docker is now running.")
				return
			log(f"  - Retry {i+1}/30: Docker still starting...")
			time.sleep(3)
		log("[X] Docker failed to start within 90 seconds.")
		sys.exit(1)
	else:
		log("[!] Please ensure Docker is manually started on macOS/Linux.")
		sys.exit(1)


def get_docker_image():
	try:
		import pynvml
		pynvml.nvmlInit()
		handle = pynvml.nvmlDeviceGetHandleByIndex(0)
		name = pynvml.nvmlDeviceGetName(handle).decode()
		log(f"[OK] GPU Detected: {name}")
		return "ghcr.io/open-webui/open-webui:cuda"
	except:
		log("[!] No compatible GPU found. Falling back to CPU image.")
		return "ghcr.io/open-webui/open-webui:main"


def start_open_webui_docker(docker_image):
	log("Checking if Open WebUI container is running...")
	subprocess.run(["docker", "rm", "-f", "open-webui"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	log("Starting new Open WebUI container...")
	run_command([
		"docker", "run", "-d",
		"--name", "open-webui",
		"-p", f"{DEFAULT_PORT}:3000",
		"-v", "ollama:/root/.ollama",
		"--add-host", "host.docker.internal:host-gateway",
		"-e", "PORT=3000",
		"-e", "HOST=0.0.0.0",
		"-e", "WEBUI_AUTH=False",
		docker_image
	])
	log("[OK] Open WebUI container started.")


def open_browser():
	log("Waiting for WebUI to become available...")
	for attempt in range(30):
		try:
			resp = requests.get(f"http://localhost:{DEFAULT_PORT}/auth", timeout=1)
			if resp.status_code == 200:
				log("[OK] WebUI is ready.")
				webbrowser.open(f"http://localhost:{DEFAULT_PORT}")
				return True
		except requests.exceptions.RequestException:
			pass
		time.sleep(2)
	log("[X] WebUI did not become available in time.")
	return False


def main():
	LOG_FILE.write_text("Launching Open WebUI Assistant...\n", encoding="utf-8")
	if DONE_FLAG.exists():
		DONE_FLAG.unlink()

	log("Starting Open WebUI Assistant...")
	check_ollama()
	model_name = detect_model()
	pull_model(model_name)
	ensure_docker_running()
	docker_image = get_docker_image()
	start_open_webui_docker(docker_image)

	if open_browser():
		log("[OK] WebUI opened in browser. Waiting to finalize splash screen...")
		time.sleep(5)
		DONE_FLAG.touch()
		log("[\u2713] All systems ready. Exiting launcher.")
		os._exit(0)
	else:
		log("[X] WebUI failed to load.")
		sys.exit(1)


if __name__ == "__main__":
	main()
