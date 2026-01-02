# 🚀 Multi-Agent AI System (Local, RAG-enabled, Explainable)

A **production-style multi-agent AI system** built completely **from scratch**, running **locally** using open-source models.  
The system supports **conditional multi-agent execution**, **Retrieval-Augmented Generation (RAG)**, and an **interactive web dashboard** with full reasoning traces.

> Designed to run efficiently on low-resource machines (≈8 GB RAM).

---

## ✨ Key Features

- 🧠 **Multi-Agent Architecture**
  - Planner Agent → structures the approach
  - Reasoner Agent → generates final answers
  - Critic Agent → optional verification & critique (strict mode)

- ⚡ **Conditional Agent Execution**
  - Only required agents run per query
  - Faster responses, lower memory usage

- 📚 **RAG (Retrieval-Augmented Generation)**
  - FAISS vector search over your own documents
  - Source-grounded answers with citations

- 🖥️ **Interactive Web Dashboard**
  - Ask questions directly from UI
  - Toggle RAG & Strict mode
  - View answers, sources, and agent traces
  - Download run results as JSON

- 🔍 **Explainability & Traceability**
  - Full agent execution trace
  - Confidence score per response

- 🔒 **Fully Local**
  - No external APIs
  - Uses Ollama + open-source LLMs

---

## 🧱 System Architecture

User Query  
↓  
Planner Agent  
↓  
Reasoner Agent ────▶ (Optional) RAG Retriever (FAISS)  
↓  
(Optional) Critic Agent  
↓  
Final Answer + Confidence + Trace  
↓  
Saved & Visualized in Dashboard  

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Python  
- **LLM Runtime:** Ollama (local)  
- **Model:** LLaMA 3.x (3B recommended)  
- **Embeddings:** sentence-transformers (MiniLM)  
- **Vector Store:** FAISS  
- **Frontend:** Vanilla HTML/CSS/JS  
- **Storage:** JSON (SQLite upgrade supported)

---

## 🧠 Agents Explained

| Agent | Purpose | Runs When |
|-----|--------|----------|
| Planner | Breaks query into steps | Always |
| Reasoner | Generates final answer | Always |
| Retriever | Fetches documents | Only if RAG enabled |
| Critic | Reviews & critiques | Only if strict mode |

---

## 🚀 How to Run This Project (Step-by-Step)

### 1️⃣ Install Prerequisites

- Python **3.10 or higher**
- Git
- Ollama (local LLM runtime)

👉 Install Ollama: https://ollama.com

Pull a lightweight model (recommended for 8 GB RAM):

```bash
ollama pull llama3.2:3b
```

(Optional warm-up for faster first run)
```bash
ollama run llama3.2:3b "Say READY"
```

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

---

### 3️⃣ Create and Activate Virtual Environment

```bash
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5️⃣ (Optional) Enable RAG – Add Documents

Place your documents here:

```
data/docs/
```

Supported formats:
- `.pdf`
- `.txt`
- `.md`

Run ingestion:

```bash
python scripts/ingest_docs.py
```

This builds the FAISS vector index used for retrieval.

---

### 6️⃣ Start the Application

```bash
python -m uvicorn app.main:app --reload
```

You should see:

```
Uvicorn running on http://127.0.0.1:8000
```

---

### 7️⃣ Open the Dashboard

Open your browser and go to:

```
http://127.0.0.1:8000/
```

From the dashboard you can:
- Ask questions
- Enable/disable RAG
- Enable strict verification
- View agent traces
- Download results

---

## 🧪 Example API Request (Optional)

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
- Uses **2 agents by default** for speed
- Critic agent runs only when enabled
- RAG chunk sizes are capped to avoid memory issues

---

## 📌 Why This Project Matters

This project demonstrates:
- Real-world **multi-agent orchestration**
- Efficient **local LLM deployment**
- **Explainable AI** with traceability
- RAG without cloud dependencies
- Production-style system design

---

## 👤 Author

Built by **Ujjwal Patel**
