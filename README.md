# 📌 Mini AI Call Insight Agent

An AI-powered system that uses RAG (Retrieval-Augmented Generation) and rule-based tool routing to analyze customer support calls and answer queries about call outcomes, sentiment, and summaries.

---

# 🚀 Features

- 🔍 Semantic search over call transcripts (RAG)
- 🤖 LLM-powered responses using Groq LLaMA 3.1
- 🧠 Rule-based tool routing:
  - Call outcome lookup
  - Sentiment summary
- 📦 Vector database: Pinecone
- ⚡ Smart multi-level retrieval strategy (Exact + Fuzzy + Semantic)
- 🖥️ CLI-based interaction

---

# 🧠 Architecture Overview

## 🔄 System Flow

```
User Query
   ↓
Call ID Detection (Regex)
   ↓
   ├── Tool Routing (Outcome / Sentiment)
   └── Retrieval System (RAG)
            ↓
        Context Generation
            ↓
        LLM Response (Groq)
```

---

# 📁 Project Structure

```
INTERNSHIP_ASSIGNMENT/
│── main.py
│── agent.py
│── rag.py
│── embed.py
│── tools.py
│── Call_Dataset.xlsx
│── .env
│── requirements.txt
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone the Repository

```
git clone https://github.com/AnshRajSingh70076/Internship_Assignment.git
cd Internship_Assignment
```

---

## 2️⃣ Create Virtual Environment

```
python -m venv venv
```

### Activate:

**Windows:**
```
venv\Scripts\activate
```

**Mac/Linux:**
```
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

OR manually:

```
pip install langchain langgraph langchain-community langchain-groq
pip install pinecone sentence-transformers pandas openpyxl python-dotenv
```

---

## 4️⃣ Setup Environment Variables (.env)

```
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Run Project

```
python main.py
```

---

# 💬 Example Queries

- What happened in CALL_001?
- What is the sentiment of CALL_002?
- What is the outcome of CALL_003?
- Summarize customer complaints about delivery delays

---

# 📊 Sample Outputs

**Query:**
What is the sentiment of CALL_001?

**Answer:**
Negative – delayed delivery

---

**Query:**
What happened in CALL_003?

**Answer:**
Customer contacted support for product information. The agent provided details. No escalation required.

---

# 🧩 Core Components

## 1. Data Processing (rag.py)
- Loads call data from Excel
- Combines:
  - Customer complaint
  - Agent action
- Converts into structured documents

---

## 2. Vector Store (embed.py)
- Uses `sentence-transformers/all-MiniLM-L6-v2`
- Stores embeddings in Pinecone
- Auto-creates index if not present

---

## 3. Smart Retrieval Strategy

### ✅ Level 1: Exact Match
- Detects CALL_ID using regex
- Uses metadata filtering
- Highest precision

### ✅ Level 2: Fuzzy Search
Handles:
- "call 1"
- "call_001"
- "CALL001"

Improves recall for noisy inputs

### ✅ Level 3: Semantic Search
- Embedding-based retrieval
- Returns top-2 relevant calls

---

## 4. Tools (tools.py)

- `get_call_outcome(call_id)`
- `get_sentiment_summary(call_id)`

Triggered using rule-based routing inside the agent.

---

## 5. Agent (agent.py)

- Detects CALL_ID using regex
- Routes queries:
  - Tool-based (outcome / sentiment)
  - RAG-based (general queries)
- Uses Groq LLM for final response
- Built using LangGraph (single-node flow)

---

## 6. Main Application (main.py)

- Loads dataset from `Call_Dataset.xlsx`
- Populates tool memory (`CALL_OUTCOMES`)
- Ingests data into Pinecone vector store
- Runs interactive CLI

👉 **Important:**  
If needed, update dataset path inside `main.py`:
```python
load_data("Call_Dataset.xlsx")
```

---

# 📦 Requirements

- Python 3.9+
- Pinecone account
- Groq API key

---

# ⚡ Performance Improvements

- Multi-level retrieval (Exact + Fuzzy + Semantic)
- Metadata filtering for fast lookup
- Embedding-based deduplication in Pinecone
- Rule-based tool routing reduces LLM load

---

# 🚀 Possible Future Improvements

- Replace rule-based routing with full tool-calling (LangChain Agents)
- Add SQL database for structured analytics (faster filtering of outcomes & sentiment)
- Add FastAPI backend for production deployment
- Add evaluation metrics (retrieval accuracy + response grounding score)

---

# ✨ Author

Built as part of an AI/ML Engineering Internship Assessment
