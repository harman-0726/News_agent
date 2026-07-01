# 📰 AI News Assistant

An intelligent **AI-powered News Assistant** built with **LangChain, Groq, RAG, LangGraph, and WhatsApp Automation**. It delivers accurate AI news by combining Retrieval-Augmented Generation (RAG), live web search, conversation memory, and scheduled WhatsApp notifications.

Instead of relying solely on an LLM's internal knowledge, the assistant retrieves information from a vector database of AI news articles and automatically falls back to web search when needed, ensuring responses remain relevant and up to date.

---

# 🚀 Features

* 🧠 **Retrieval-Augmented Generation (RAG)** for accurate AI news retrieval
* 📚 **Vector Database Search** using semantic similarity
* 🌐 **Automatic Web Search Fallback** via DuckDuckGo when information isn't available locally
* 🤖 **LangChain Agent** with intelligent tool selection
* 💬 **Conversation Memory** powered by LangGraph for natural follow-up questions
* ⚡ **High-Speed Inference** using Groq-hosted LLMs
* 📰 **Automatic AI News Summarization**
* 📱 **Scheduled WhatsApp News Delivery**
* ⏰ **Daily AI News Digest** sent automatically at a configured time
* 🔗 **Source Attribution** for every response
* 📄 **RSS Feed Processing** from multiple AI news websites
* 🧩 **Modular Architecture** for easy extension

---

# 🏗️ Project Architecture

```text
                    AI RSS Sources
                           │
                           ▼
                 Fetch Latest Articles
                           │
                           ▼
                Extract Article Content
                           │
                           ▼
              Generate Text Embeddings
                           │
                           ▼
                  Store in Vector DB
                           │
         ┌─────────────────┴──────────────────┐
         │                                    │
         ▼                                    ▼
  User asks a question             Scheduled Time Trigger
         │                                    │
         ▼                                    ▼
   LangChain AI Agent               Retrieve Latest AI News
         │                                    │
         ▼                                    ▼
 Search Vector Database             Generate Daily Summary
         │                                    │
         ├───────────────┐                    ▼
         │               │            Send WhatsApp Message
         ▼               ▼
Answer Found      DuckDuckGo Search
         │               │
         └───────┬───────┘
                 ▼
        Generate Final Response
                 │
                 ▼
       Conversation Memory
```

---

# 🛠️ Tech Stack

### AI & LLM

* LangChain
* LangGraph
* Groq
* Qwen3-32B

### Retrieval

* Chroma Vector Database
* HuggingFace Embeddings

### News Processing

* Feedparser
* Trafilatura

### Search

* DuckDuckGo Search

### Automation

* WhatsApp Cloud API
* Python Scheduler

### Other

* Python
* dotenv

---

# 📂 Project Structure

```text
AI-News-Assistant/
│
├── tools.py                # AI Agent
├── vectorstore.py          # Chroma Vector Database
├── news.py                 # Fetch RSS News
├── extract.py              # Extract Article Content
├── ingest.py               # Store Articles in Vector DB
├── scheduler.py            # Daily WhatsApp Scheduler
├── whatsapp.py             # WhatsApp Cloud API
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/AI-News-Assistant.git
cd AI-News-Assistant
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key

HF_TOKEN=your_huggingface_token

VERIFY_TOKEN=your_verify_token

PHONE_NUMBER_ID=your_phone_number_id

WHATSAPP_TOKEN=your_whatsapp_cloud_api_token

OWNER_PHONE=your_whatsapp_number

DIGEST_HOUR=10
```

---

# ▶️ Running the Assistant

```bash
python tools.py
```

Example:

```text
Ask: What is Google Gemini?

Ask: Tell me more.

Ask: Compare Gemini and ChatGPT.

Ask: What happened today in AI?
```

---

# 📱 Automatic WhatsApp AI News

The assistant automatically sends a summarized AI News Digest to WhatsApp every day at the configured time.

### Workflow

1. Collect AI news from RSS feeds.
2. Extract article content.
3. Store articles in the vector database.
4. Retrieve the most important news.
5. Generate concise AI summaries.
6. Automatically deliver the digest to WhatsApp.

Example:

```text
📰 Daily AI News Digest

• Google introduces new AI features in Search.

• NVIDIA launches BioNeMo Agent Toolkit for drug discovery.

• Open-source reasoning models continue improving coding benchmarks.

Reply with any question to learn more.
```

---

# 🧠 Conversation Memory

The assistant remembers previous messages within a conversation using LangGraph Memory.

Example:

```text
User:
Tell me about Google Gemini.

Assistant:
...

User:
Who developed it?

Assistant:
Google developed Gemini.

User:
Compare it with ChatGPT.

Assistant:
...
```

This enables natural multi-turn conversations.

---

# 🔍 Retrieval Strategy

The assistant follows a retrieval-first approach:

1. Search the local AI News Vector Database.
2. If relevant information is unavailable, automatically perform a live DuckDuckGo search.
3. Generate a concise response using only retrieved information.
4. Include source information in the final response.

This reduces hallucinations and keeps answers current.

---

# 🌟 Future Improvements

* Persistent conversation memory (SQLite/PostgreSQL)
* Hybrid Search (Keyword + Semantic Search)
* Personalized AI news recommendations
* Web dashboard with Streamlit
* Multi-user conversation support
* Source citation links
* Streaming responses
* Voice interface
* Telegram and Discord integration

---

# 📸 Demo

Example questions:

* What is Google Gemini?
* Latest AI news today
* Tell me about NVIDIA BioNeMo
* Compare GPT-4 and Gemini
* What happened in AI this week?
* Summarize today's AI news

---

# 👨‍💻 Author

**Harmandeep Singh**

Aspiring AI Engineer passionate about Artificial Intelligence, Retrieval-Augmented Generation (RAG), Agentic AI, LLM-powered applications, and intelligent automation.

---

# ⭐ If You Like This Project

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and supports future development.

---

# 📄 License

This project is licensed under the MIT License.
