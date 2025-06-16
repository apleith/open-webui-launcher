# 🧠 Open WebUI Local Assistant

A lightweight Python-based launcher for running [Open WebUI](https://github.com/open-webui/open-webui) locally via Docker and automatically loading the [DeepSeek-R1 8B](https://huggingface.co/deepseek-ai/DeepSeek-V2) model in [Ollama](https://ollama.com/).

Designed for Windows users who want a one-click way to spin up a full local LLM research assistant interface — no CLI gymnastics required.

---

## 🚀 Features

- 🧩 Automatically pulls the DeepSeek-R1 8B model from Ollama
- 🐳 Boots up Open WebUI in a Docker container
- 🌐 Opens your browser only after the interface is fully ready
- 🖱️ Includes a `.bat` launcher for frictionless use on Windows
- 💡 Provides detailed output for debugging, model pulls, and Docker startup

---

## ⚙️ Requirements

Before using this launcher, make sure the following are installed:

- [Python 3.9+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Ollama](https://ollama.com/download)

Ensure both Docker and Ollama are **added to your system PATH** during installation.

---

## 🖥️ Usage

### 🔘 One-Click Method (Windows Only)

Double-click:

```

run\_webui\_assistant.bat

````

This will:
1. Verify you have Docker and Ollama
2. Pull the DeepSeek-R1 8B model
3. Start the Open WebUI container (if not already running)
4. Open your browser to `http://localhost:3000` when ready

### 🐍 Python Method

If you're working from a terminal:

```bash
python launch_webui_assistant.py
````

---

## 📁 Project Structure

```
webui-local-assistant/
├── launch_webui_assistant.py     # Main script
├── run_webui_assistant.bat       # Windows launcher
├── webui.ico                     # (Optional) icon for packaging
├── README.md                     # Project documentation
├── LICENSE                       # MIT or other open license
└── .gitignore                    # Python and PyInstaller build artifacts
```

---

## 🛡 License

[MIT License](LICENSE)

Feel free to adapt, fork, and share.

---

## 🤝 Credits

* [Open WebUI](https://github.com/open-webui/open-webui)
* [DeepSeek-R1](https://huggingface.co/deepseek-ai)
* [Ollama](https://ollama.com/)

Crafted for local-first LLM research and tinkering.
