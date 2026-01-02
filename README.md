# 🚀 Multi-Agent AI Reasoning System

![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-green)
![LLM](https://img.shields.io/badge/LLM-Local%20(Ollama)-purple)
![RAG](https://img.shields.io/badge/RAG-FAISS-orange)
![Status](https://img.shields.io/badge/status-active-success)

A **production-style multi-agent AI system** built from scratch that runs **fully locally** using open‑source LLMs.  
It supports **conditional multi-agent execution**, **Retrieval‑Augmented Generation (RAG)**, and an **interactive web dashboard** with full reasoning traces.

> Optimized to run on low‑resource machines (~8 GB RAM)

---

## 📑 Table of Contents
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Agents](#-agents)
- [How to Run (Step‑by‑Step)](#-how-to-run-step-by-step)
- [Dashboard Demo](#-dashboard-demo)
- [API Usage](#-api-usage)
- [Performance Notes](#-performance-notes)
- [Future Improvements](#-future-improvements)

---

## ✨ Key Features

- 🧠 **Multi‑Agent Architecture** (Planner, Reasoner, optional Critic)
- ⚡ **Conditional Execution** (only required agents run)
- 📚 **RAG with FAISS** for document‑grounded answers
- 🖥️ **Interactive Dashboard**
- 🔍 **Explainable AI** with trace & confidence score
- 🔒 **100% Local** (no cloud APIs)

---

## 🧱 System Architecture

```
User Query
   ↓
Planner Agent
   ↓
Reasoner Agent ───▶ (Optional) RAG Retriever
   ↓
(Optional) Critic Agent
   ↓
Final Answer + Confidence + Trace
```

---

## 🧠 Agents

<details>
<summary><strong>🧠 Planner Agent</strong></summary>

- Breaks the user query into short steps  
- Improves reasoning structure  
- Runs on every request  

</details>

<details>
<summary><strong>🤔 Reasoner Agent</strong></summary>

- Generates the final answer  
- Uses retrieved documents if RAG is enabled  
- Cites sources when available  

</details>

<details>
<summary><strong>🧐 Critic Agent (Optional)</strong></summary>

- Reviews the answer for correctness  
- Runs only in **strict mode**  
- Adds critique notes to output  

</details>

---

## ▶️ How to Run (Step‑by‑Step)

### 1️⃣ Prerequisites
- Python **3.10+**
- Git
- Ollama → https://ollama.com

```bash
ollama pull llama3.2:3b
```

---

### 2️⃣ Clone Repo
```bash
git clone https://github.com/ujjwal0909/Multi-Agent-Reasoning-System-.git
cd multi_agent_system
```

---

### 3️⃣ Setup Virtual Environment

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS**
```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 5️⃣ (Optional) Enable RAG

Add documents to:
```
data/docs/
```

Run ingestion:
```bash
python scripts/ingest_docs.py
```

---

### 6️⃣ Start Server
```bash
python -m uvicorn app.main:app --reload
```

---

### 7️⃣ Open Dashboard
```
http://127.0.0.1:8000/
```

---

## 🎥 Dashboard Demo

(Add `assets/demo.gif` here)

---

## 🧪 API Usage

```bash
curl -X POST http://127.0.0.1:8000/query   -H "Content-Type: application/json"   -d '{
    "query": "Explain multi-agent AI in simple words",
    "use_rag": false,
    "strict": false
  }'
```

---

## ⚡ Performance Notes

- Optimized for **8 GB RAM**
- Uses **2 agents by default**
- Critic agent runs only when enabled

---

## 🔮 Future Improvements

- SQLite-backed storage
- Streaming responses
- Agent timeline visualization

---

## 👤 Author

**Ujjwal Patel**
