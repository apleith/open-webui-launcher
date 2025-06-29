# 🚀 Open WebUI Launcher v2.0

A desktop launcher for running [Open WebUI](https://github.com/open-webui/open-webui) locally via Docker + Ollama, with automatic model selection and a clean splash screen.

---

## ⚙️ Requirements

- **Docker Desktop** (Windows)  
- **Ollama CLI** (must be on your `PATH`)  
- **Internet access** for model downloads  

---

## 🏁 Getting Started

1. **Download the Windows installer**  
   👉 [Open WebUI Launcher v2.0 for Windows (Installer)](https://github.com/apleith/open-webui-launcher/raw/refs/heads/main/releases/latest/download/Open_WebUI_Launcher_v2.0.exe)

2. **Run the installer**  
   - Double-click `Open_WebUI_Launcher_v2.0.exe` and follow the prompts.
   - This will install the app to `C:\Program Files\Open WebUI Launcher` by default and create Start Menu and Desktop shortcuts.

3. **Launch the App**  
   - From your Start Menu or Desktop, click **Open WebUI Launcher**.
   - A splash screen will appear showing live initialization logs.
   - Once ready, your default browser will open pointing to `http://localhost:3000/`.

---

## ✨ What It Does

- 🔍 **Detects your GPU** and auto-selects the best DeepSeek-R1 model (1.5B–671B).
- 🐋 **Ensures Docker & Ollama** are running, starting Docker Desktop if needed.
- 🚀 **Pulls & serves** the selected model via Ollama.
- 🔄 **Manages** an Open WebUI Docker container with persistent volume.
- 🌐 **Opens your browser** only when Open WebUI is fully live.
- 📺 **Displays a splash screen** with real-time logs during startup.
- 🧹 **Cleans up** leftover containers or port conflicts on each launch.

---

## 🐍 Developer / Portable Mode

If you’d rather run from source or use a portable standalone executable:

```bash
# Clone the repo
git clone https://github.com/apleith/open-webui-launcher.git
cd open-webui-launcher/common

# Python mode:
python splash_screen.py
````

Or copy `dist/Open_WebUI_Launcher_v2.0.exe` to any folder and run it directly—no install required.

---

## 📂 Project Layout

```
open-webui-launcher/
├── dist/
│   └── Open_WebUI_Launcher_v2.0.exe   # Windows installer & portable EXE
│
├── common/                            # Core Python scripts & assets
│   ├── launch_main.py
│   ├── launch_webui_assistant.py
│   ├── splash_screen.py
│   ├── logo.ico, logo.png
│   └── splash_image.png
│
├── windows/                           # Windows helper scripts & installer script
│   ├── launch_hidden.py
│   ├── run_webui_assistant.bat
│   └── Open_WebUI_Launcher.iss
│
├── open-webui-launcher.spec           # PyInstaller spec
├── .gitignore
└── README.md
```

---

## 🔧 Recommended Plugins

Enable these via Open WebUI’s **Tools** panel for research workflows:

| Plugin                        | Purpose                       |
| ----------------------------- | ----------------------------- |
| `web_search`                  | Live fact checking            |
| `ocr_scanned_pdf`             | OCR for scanned documents     |
| `youtube_transcript_provider` | Import lecture transcripts    |
| `arxiv_search_tool`           | Pull latest papers from arXiv |
| `convert_to_json`             | Structured JSON export        |
| `calculator`                  | In-chat math and statistics   |
| `chat_with_csv`               | Pandas-backed CSV analysis    |
| `wolframalpha`                | Advanced math and logic       |
| `knowledgebase_tools`         | Document memory & search      |

🔗 [Plugin setup guide](https://docs.openwebui.com/features/plugin/tools/)

---

## 📜 License

This project is Apache 2.0-licensed. See [LICENSE](https://www.apache.org/licenses/LICENSE-2.0) for details.

---

## 🙌 Acknowledgments

Built using excellent open-source software:

* 🌐 [Open WebUI](https://github.com/open-webui/open-webui)
* 🤖 [DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-V2)
* 🐋 [Docker](https://www.docker.com)
* 📦 [Ollama](https://ollama.com)
* 🐍 [PyInstaller](https://pyinstaller.org)
* 🛠 [Inno Setup](https://jrsoftware.org/isinfo.php)

---

## ❤️ Support

If you find **Open WebUI Launcher** useful, consider buying me a coffee:
☕ [ko-fi.com/apleith](https://ko-fi.com/apleith)

---

> Built with ❤️ by Alex P Leith, PhD · Powered by Docker, Ollama & Open WebUI