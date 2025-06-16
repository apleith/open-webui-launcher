# Open WebUI Local Assistant

A Python-based launcher that runs [Open WebUI](https://github.com/open-webui/open-webui) locally via Docker and automatically loads the DeepSeek-R1 8B model in Ollama.

## Features

- Auto-pulls DeepSeek-R1 8B model from Ollama
- Starts Open WebUI in Docker
- Opens browser after the interface is ready
- Includes `.bat` launcher for easy use on Windows

## Requirements

- [Python 3.9+](https://www.python.org/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Ollama](https://ollama.com/)

## Usage

### One-click Launcher (Windows)

Just double-click:

```bat
run_webui_assistant.bat
````

Or run in a terminal:

```bash
python launch_webui_assistant.py
```