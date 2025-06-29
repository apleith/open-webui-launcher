import subprocess
import logging
import os
import time
import webbrowser
import shutil
import re
from pathlib import Path
from logging.handlers import RotatingFileHandler

OLLAMA_PORT        = 11434
HOST_PORT          = 3000
CONTAINER_PORT     = 8080
VOLUME_NAME        = "open-webui-data"
CONTAINER_DATA_DIR = "/app/backend/data"

# ─── logging setup ─────────────────────────────────────────────────────────────
base    = os.getenv("LOCALAPPDATA") or str(Path.home())
log_dir = Path(base) / "OpenWebUIAssistant" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
LOG_PATH = log_dir / "assistant.log"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fmt   = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
fh    = RotatingFileHandler(LOG_PATH, maxBytes=5*1024*1024, backupCount=3)
fh.setFormatter(fmt)
logger.handlers = [fh]

# suppress Windows console windows
creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
startupinfo   = None
if os.name == "nt":
	startupinfo = subprocess.STARTUPINFO()
	startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# strip ANSI escapes
_ESCAPE_RE = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
def strip_ansi(line: str) -> str:
	return _ESCAPE_RE.sub("", line)

# ─── helpers ────────────────────────────────────────────────────────────────────
def ensure_tool(cmd: str) -> bool:
	p = shutil.which(cmd)
	if not p:
		logger.error(f"{cmd} not found on PATH.")
		return False
	logger.debug(f"Found {cmd} at {p}")
	return True

def ensure_docker() -> bool:
	try:
		subprocess.run(
			["docker", "info"],
			stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
			check=True, creationflags=creationflags, startupinfo=startupinfo
		)
		logger.debug("Docker Desktop is running")
		return True
	except:
		logger.warning("Docker not running; trying to start Docker Desktop")
		exe = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
		if os.path.exists(exe):
			os.startfile(exe)
			time.sleep(10)
			return ensure_docker()
		logger.error(f"Docker Desktop not found at {exe}")
		return False

def detect_gpu_vram() -> float:
	try:
		import pynvml
		pynvml.nvmlInit()
		h = pynvml.nvmlDeviceGetHandleByIndex(0)
		m = pynvml.nvmlDeviceGetMemoryInfo(h)
		v = m.total / (1024**3)
		logger.debug(f"NVML reports {v:.1f} GB VRAM")
		return v
	except Exception:
		try:
			out = subprocess.check_output(
				["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
				encoding="utf-8", creationflags=creationflags, startupinfo=startupinfo
			)
			v = float(out.splitlines()[0]) / 1024
			logger.debug(f"nvidia-smi reports {v:.1f} GB VRAM")
			return v
		except:
			logger.debug("No GPU detected, assuming CPU-only")
			return 0.0

# ─── main orchestrator ─────────────────────────────────────────────────────────
def main():
	logger.info("Orchestrator starting")

	# 1) prereqs
	if not ensure_tool("docker"):   return
	if not ensure_tool("ollama"):   return
	if not ensure_docker():         return

	# 2) select model by VRAM
	gpu = detect_gpu_vram()
	if   gpu >= 128: tag = "deepseek-r1:671b"
	elif gpu >=  48: tag = "deepseek-r1:70b"
	elif gpu >=  24: tag = "deepseek-r1:32b"
	elif gpu >=  16: tag = "deepseek-r1:14b"
	elif gpu >=   8: tag = "deepseek-r1:8b"
	else:            tag = "deepseek-r1:1.5b"
	logger.info(f"Selected model: {tag}")

	# 3) check installed Ollama models
	try:
		out = subprocess.check_output(["ollama","list"], text=True)
		lines     = [l for l in out.splitlines()[1:] if l.strip()]
		installed = {l.split()[0] for l in lines}
	except Exception as e:
		logger.warning(f"Could not list Ollama models: {e}")
		installed = set()

	# alias latest for 1.5b
	alias = None
	if tag.endswith(":1.5b"):
		alias = tag.replace(":1.5b", ":latest")

	if tag in installed or (alias and alias in installed):
		logger.info(f"Model {tag} already installed; skipping pull")
	else:
		# pull model
		if tag.endswith(":1.5b"):
			# background pull + poll until installed
			logger.info(f"Pulling {tag} via Ollama (in background)...")
			subprocess.Popen(
				["ollama","pull", tag],
				stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
				creationflags=creationflags, startupinfo=startupinfo
			)
			for i in range(150):
				time.sleep(10)
				try:
					out = subprocess.check_output(["ollama","list"], text=True)
					if tag in out or (alias and alias in out):
						logger.info(f"{tag} now installed.")
						break
				except Exception:
					pass
				logger.debug(f"Waiting for {tag} installation ({i+1}/150)")
			else:
				logger.error(f"Timeout waiting for {tag} to finish downloading")
				return
		else:
			# live progress for larger models
			logger.info(f"Pulling model {tag} via Ollama")
			proc = subprocess.Popen(
				["ollama","pull", tag],
				stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
				bufsize=0, text=True,
				creationflags=creationflags, startupinfo=startupinfo
			)
			buffer = ""
			while True:
				chunk = proc.stdout.read(512)
				if not chunk:
					if proc.poll() is not None:
						break
					time.sleep(0.1)
					continue
				buffer += chunk
				parts = re.split(r"[\r\n]", buffer)
				for line in parts[:-1]:
					clean = strip_ansi(line).strip()
					if clean:
						logger.info(clean)
				buffer = parts[-1]
			if buffer.strip():
				logger.info(strip_ansi(buffer).strip())
			if proc.wait() != 0:
				logger.error("Ollama pull failed")
				return

	# 4) start Ollama HTTP server
	env = os.environ.copy()
	env["OLLAMA_HOST"] = f"127.0.0.1:{OLLAMA_PORT}"
	logger.info(f"Starting Ollama server on port {OLLAMA_PORT}")
	subprocess.Popen(
		["ollama","serve", tag],
		env=env, creationflags=creationflags, startupinfo=startupinfo
	)

	# 5) reuse or create Open WebUI container
	logger.info("Setting up Open WebUI Docker container")
	existing = subprocess.run(
		["docker","ps","-a","--filter","name=open-webui","--format","{{.Names}}"],
		capture_output=True, text=True
	).stdout.splitlines()

	image = "ghcr.io/open-webui/open-webui:cuda" if gpu >= 1 else "ghcr.io/open-webui/open-webui:main"
	if "open-webui" in existing:
		logger.info("Restarting existing 'open-webui'")
		subprocess.run(
			["docker","restart","open-webui"],
			check=True, creationflags=creationflags, startupinfo=startupinfo
		)
	else:
		logger.info("Creating new 'open-webui'")
		cmd = [
			"docker","run","-d","--name","open-webui",
			"-p", f"{HOST_PORT}:{CONTAINER_PORT}",
			"--add-host=host.docker.internal:host-gateway",
			"-e","WEBUI_AUTH=False",
			"-e",f"OLLAMA_BASE_URL=http://host.docker.internal:{OLLAMA_PORT}",
			"-v",f"{VOLUME_NAME}:{CONTAINER_DATA_DIR}"
		]
		if gpu >= 1:
			cmd += ["--gpus","all"]
		cmd.append(image)
		subprocess.run(cmd, check=True, creationflags=creationflags, startupinfo=startupinfo)

	# 6) poll until WebUI is ready
	url = f"http://localhost:{HOST_PORT}/"
	logger.info(f"Waiting for Open WebUI at {url}")
	for i in range(60):
		try:
			import requests
			r = requests.get(url, timeout=2)
			if r.status_code == 200 and len(r.text) > 200:
				logger.info("Open WebUI ready; opening browser")
				webbrowser.open(url)
				return
		except:
			pass
		time.sleep(1)

	logger.error("Timed out waiting for Open WebUI")

if __name__ == "__main__":
	main()
