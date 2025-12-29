# Autonomous Research Agent 🤖📊

An intelligent, autonomous AI research assistant powered by **LangGraph**, **FastAPI**, and **Google Gemini-2.5-Flash**. The agent takes a user's research query, autonomously plans its search strategy, browses the web, scrapes relevant URLs, and synthesizes its findings into a comprehensive, deeply detailed Markdown report.

The backend communicates with a **React + Vite** frontend in real-time via WebSockets, allowing you to watch the agent "think", see what tools it is calling, and progressively receive the final research report.

---

## 🌟 Key Features

- **Autonomous Agent Workflow:** Built with LangGraph, the agent determines when to search, what to read, and when it has enough information to compile the report.
- **Real-Time Streaming:** Uses WebSockets to stream the agent's thought process, tool executions, and state updates directly to the frontend UI.
- **Intelligent Tool Use:** Equipped with tools to search the web and intelligently scrape/extract data from high-value URLs.
- **Google GenAI Integration:** Powered by the fast and capable Gemini-2.5-Flash model.
- **Markdown Reports:** Output is beautifully formatted into rich Markdown with headers, bullet points, and source citations.

---

## 🛠️ Technology Stack

**Backend:**
- Python 3.x
- [FastAPI](https://fastapi.tiangolo.com/) (REST & WebSocket endpoints)
- [LangChain](https://python.langchain.com/docs/get_started/introduction) & [LangGraph](https://python.langchain.com/docs/langgraph)
- Google Generative AI (`gemini-2.5-flash`)
- Uvicorn

**Frontend:**
- React 18
- Vite
- TailwindCSS (removed to avoid native binding errors) / Custom CSS
- WebSockets for real-time reactivity

---

## 📂 Project Structure

```text
autonomous_research_agent/
│
├── backend/                  # FastAPI & LangGraph Backend
│   ├── agent/                # Agent Logic
│   │   ├── graph.py          # StateGraph definitions and model binding
│   │   ├── state.py          # Agent state definitions
│   │   └── tools.py          # Custom search and web scraping tools (Langchain DDG)
│   ├── main.py               # FastAPI server and WebSocket routes with keepalive ping
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # React + Vite Frontend
│   ├── src/                  # Components and source code
│   └── package.json          # Node dependencies
│
├── run_app.bat               # Windows execution script
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js & npm (v16+)
- A Google API Key (`GEMINI_API_KEY` or equivalent in `.env`)

### 1. Configure Environment Variables
You need to create `.env` files for both the backend and frontend (if needed).

**Backend `.env`** (`backend/.env`):
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 2. Quick Start (Windows)
If you are on Windows, you can launch both the frontend and backend simultaneously using the provided batch script:
```cmd
.\run_app.bat
```
*Note: Make sure you have installed the requirements first before running this script.*

### 3. Manual Setup

**Backend Setup:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
python main.py
```
The FastAPI server will run on `http://localhost:8001`.

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```
The React app will typically run on `http://localhost:5173`.

---

## 🤝 How It Works
1. The user inputs a query into the React frontend.
2. The query is sent via WebSocket to the FastAPI backend.
3. The LangGraph agent `call_model` node is triggered. It acts as an orchestrator, deciding whether to call a tool or render a final response.
4. If a tool (`search` or `scrape`) is called, execution transitions to the `ToolNode`, runs the tool, and loops back to the model.
5. All updates (`tool_call`, `message`) are streamed asynchronously back to the React client via WebSockets.
6. Once the model outputs a final non-tool message, the execution ends, and the final report is rendered.

---

> Built with ❤️ for Advanced AI Research Automation.
