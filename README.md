# 🧠 Open WebUI Local Assistant

A cross-platform launcher for running [Open WebUI](https://github.com/open-webui/open-webui) locally via Docker, auto-loading the best-fit [DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-V2) model in [Ollama](https://ollama.com/), and providing a responsive splash screen while everything initializes.

Built for researchers, developers, and educators who want a local-first AI assistant with minimal setup and maximum control.

---

## 🚀 Features

- ✅ Automatically detects your GPU and selects the right DeepSeek-R1 model
- 🐳 Starts Open WebUI in a clean Docker container
- 🔁 Restarts Docker automatically if not running
- 🌐 Launches your browser only once Open WebUI is confirmed live
- 🪟 Splash screen shows real-time loading logs and closes on launch
- 🧼 No leftover containers or port errors—cleans itself
- 📦 Includes both Windows `.bat` launcher and standalone `.exe` builds

---

## ⚙️ Requirements

Install and configure the following:

- [Python 3.12+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Ollama](https://ollama.com/download)

⚠️ Ensure Docker and Ollama are in your system `PATH`.

---

## 🖥️ Usage

### 🔹 Windows Standard Launch

From the `windows/` folder, double-click:

```

run\_webui\_assistant.bat

```

You’ll see a visual splash screen. Once everything is ready, Open WebUI opens automatically.

### 📦 Portable `.exe` Launch

Navigate to `dist/` and run:

```

WebUI\_Assistant\_Portable.exe

````

This version has no terminal window and runs as a self-contained executable.

### 🐍 Python Development Mode

From the terminal in `common/`:

```bash
python splash_screen.py
````

---

## 🧰 Project Structure

```
webui-assistant-multiplatform/
├── common/
│   ├── splash_screen.py
│   ├── launch_webui_assistant.py
│   ├── splash_image.png / .ico
│   ├── assistant.log
│   ├── .splash_done
│   ├── *.spec (PyInstaller configs)
│   └── config.json (future settings)
│
├── windows/
│   └── run_webui_assistant.bat
│
├── dist/
│   ├── WebUI_Assistant.exe
│   └── WebUI_Assistant_Portable.exe
│
├── standalone/
│   └── run_webui_assistant_portable.bat
│
└── macos/
    └── run_webui_assistant.command (placeholder)
```

---

## 🔧 Recommended Tools for Academic Use

From the [Open WebUI Tools Directory](https://openwebui.com/tools), consider enabling:

| Tool Name                     | Function                                                   |
| ----------------------------- | ---------------------------------------------------------- |
| `web_search`                  | Real-time fact-checking, live search via SearXNG or Google |
| `ocr_scanned_pdf`             | OCRs scanned documents or print PDFs                       |
| `youtube_transcript_provider` | Extracts transcripts from lecture videos                   |
| `arxiv_search_tool`           | Pulls cutting-edge academic content directly from arXiv    |
| `convert_to_json`             | Converts output into structured JSON for export/use        |
| `calculator`                  | In-chat calculations/statistics                            |
| `chat_with_csv`               | Analyze CSVs in chat using pandas backend                  |
| `wolframalpha`                | Theory-heavy math and logic answers                        |
| `knowledgebase_tools`         | Document memory/search for research papers                 |

---

### 🛠 How to Activate These Tools

1. Navigate to **Tools** in Open WebUI and click the ➕ icon
2. Search for each plugin by name (e.g., "Web Search")
3. Click **Get** to install it
4. Then go to **Workspace → Models**, edit your model, and enable the tools
5. In-chat, click the ➕ icon to add tools for that session

📘 [Official Plugin Guide](https://docs.openwebui.com/features/plugin/tools/)

---

## 🧠 Suggested System Prompt (for academic/research use)

Paste this into your **System Prompt** in Open WebUI under `Models → Edit`:

```
You are a research assistant specializing in communication, media studies, and social science. Help summarize papers, translate methods, suggest research questions, and generate APA-style citations when appropriate. Prioritize academic accuracy, clarity, and source attribution.
```

✅ Combine this with enabled tools for full research utility.

---

## ☕ Support My Work

If this launcher saved you time or improved your workflow, consider donating to my coffee fund:

👉 **[ko-fi.com/apleith](https://ko-fi.com/apleith)**

Your support helps me maintain and improve open-source research tools.

---

## 🛡 License

[MIT License](LICENSE)

Fork it, remix it, improve it.

---

## 🧭 Credits

* [Open WebUI](https://github.com/open-webui/open-webui)
* [DeepSeek-R1](https://huggingface.co/deepseek-ai)
* [Ollama](https://ollama.com)
* [PyInstaller](https://pyinstaller.org)
