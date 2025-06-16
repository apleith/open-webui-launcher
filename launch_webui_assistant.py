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
ICON_PATH = "webui.ico"

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
        print(f"[✗] Command failed: {' '.join(cmd)}")
        print(f"    Error: {e}")
        sys.exit(1)

def check_ollama():
    print("[⋯] Checking Ollama...")
    if shutil.which("ollama") is None:
        print("[✗] Ollama is not installed. Visit https://ollama.com/download")
        sys.exit(1)
    print("[✓] Ollama is installed.")

def pull_model():
    print("[⋯] Pulling DeepSeek-R1 8B model...")
    run_command(["ollama", "pull", "deepseek-r1:8b"])

def ensure_docker_running():
    print("[⋯] Checking Docker status...")
    if shutil.which("docker") is None:
        print("[✗] Docker is not installed or not in PATH.")
        print("    Download from: https://www.docker.com/products/docker-desktop")
        sys.exit(1)

    try:
        subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[✓] Docker is running.")
    except Exception:
        print("[⋯] Docker not running. Attempting to launch Docker Desktop...")
        docker_path = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
        if not os.path.exists(docker_path):
            print("[✗] Docker Desktop not found at expected location.")
            sys.exit(1)
        subprocess.Popen([docker_path])
        print("[⋯] Waiting for Docker to initialize (up to 60 seconds)...")
        for _ in range(30):
            try:
                subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("[✓] Docker is now running.")
                return
            except:
                time.sleep(2)
        print("[✗] Docker failed to start within 60 seconds.")
        sys.exit(1)

def start_open_webui_docker():
    print("[⋯] Checking if Open WebUI Docker container is running...")
    check_cmd = ["docker", "ps", "-q", "-f", "name=open-webui"]
    result = subprocess.run(check_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if result.stdout.strip():
        print("[✓] Open WebUI is already running.")
    else:
        print("[⋯] Starting Open WebUI container using v0.6.13...")
        run_command([
            "docker", "run", "-d",
            "--name", "open-webui",
            "-p", "3000:3000",
            "-v", "ollama:/root/.ollama",
            "--add-host", "host.docker.internal:host-gateway",
            "-e", "PORT=3000",
            "-e", "HOST=0.0.0.0",
            "ghcr.io/open-webui/open-webui:main"
        ])
        print("[✓] Open WebUI container started.")


def open_browser():
    print("[⋯] Waiting for WebUI to become available...")
    for attempt in range(30):
        try:
            response = requests.get("http://localhost:3000/auth", timeout=1)
            if response.status_code == 200:
                print("[✓] WebUI is ready.")
                webbrowser.open("http://localhost:3000")
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(2)
    print("[✗] WebUI did not become available in time.")

def main():
    print("=== Local WebUI Assistant Launcher ===")
    check_ollama()
    pull_model()
    ensure_docker_running()
    start_open_webui_docker()
    open_browser()

if __name__ == "__main__":
    main()
