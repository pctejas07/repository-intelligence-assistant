# GitHub Codebase Assistant

A GraphRAG-powered code intelligence assistant that helps developers understand, explore, and analyze Java and Python repositories using Hybrid Search, Knowledge Graphs, and Local LLMs.

## Features

### Repository Processing

* Clone GitHub repositories
* Scan repository structure
* Multi-language support:

  * Java
  * Python
* Automatic code chunking

### Hybrid Retrieval

* Semantic Vector Search using ChromaDB
* BM25 Keyword Search
* Hybrid Search (Vector + BM25)
* Reranking for improved retrieval quality

### Knowledge Graph Construction

* Class relationships
* Inheritance analysis
* Interface implementation analysis
* Dependency analysis
* Method call graph generation

### Code Intelligence

* Caller Analysis
* Callee Analysis
* Impact Analysis
* Call Chain Discovery
* Hierarchy Analysis
* Dependency Exploration

### GraphRAG Features

* Graph-aware context expansion
* Repository-aware question answering
* Class summaries
* Method summaries
* Graph-based reasoning

### AI Integration

* Local LLM inference using Ollama
* Qwen model support
* Context-aware code explanations

---

## Architecture

```text
GitHub Repository
        │
        ▼
Repository Scanner
        │
        ▼
Language Parsers
(Java / Python)
        │
        ▼
Chunking Engine
        │
        ├────────► ChromaDB
        │             │
        │             ▼
        │      Vector Search
        │
        ▼
Knowledge Graph
(NetworkX)
        │
        ▼
Graph Analysis
        │
        ▼
Hybrid Retrieval
(BM25 + Vector)
        │
        ▼
Reranker
        │
        ▼
Graph Context Expansion
        │
        ▼
Ollama LLM
        │
        ▼
Final Response
```

---

## Tech Stack

### Backend

* FastAPI
* Python 3.12

### Retrieval

* ChromaDB
* BM25

### Knowledge Graph

* NetworkX

### Parsing

* Tree-sitter (Java)
* Python AST

### LLM

* Ollama
* Qwen

### Data Processing

* Pydantic

---

## Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   └── services/
│       ├── chunkers/
│       ├── parsers/
│       ├── graph/
│       └── retrieval/
│
├── repositories/
├── graphs/
├── chroma_db/
└── logs/
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd github-codebase-assistant
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Ollama

Install Ollama and pull a model:

```bash
ollama pull qwen2.5-coder:3b
```

---

## Environment Configuration

Create a `.env` file:

```env
REPOSITORY_PATH=repositories
CHROMA_DB_PATH=chroma_db

OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=qwen2.5-coder:3b
```

---

## Running the Application

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## API Capabilities

### Repository APIs

* Clone Repository
* Scan Repository
* Generate Chunks
* Index Repository
* Search Repository
* Chat With Repository
* Repository Statistics
* Delete Repository

### Graph APIs

* Find Callers
* Find Callees
* Impact Analysis
* Call Chain Analysis
* Hierarchy Analysis
* Dependency Analysis
* Class Summary
* Method Summary

---

## Example Questions

### Repository Questions

* Explain the Owner class.
* How does Owner.addVisit work?
* What is the purpose of VetRepository?
* Show dependencies of Owner.

### Graph Questions

* Who calls Pet.add?
* What methods are impacted by Pet.add?
* Show call chain for Pet.addVisit.
* Explain Owner hierarchy.

---

## Supported Languages

### Java

* Classes
* Interfaces
* Inheritance
* Method Calls
* Imports

### Python

* Classes
* Functions
* Method Calls
* Imports
* Inheritance

---

## Future Enhancements

* JavaScript Support
* TypeScript Support
* Go Language Support
* Multi-Repository Search
* Docker Deployment
* CI/CD Pipeline
* PostgreSQL Metadata Layer
* Web-Based Chat UI

---

## Key Learnings

This project demonstrates:

* Retrieval-Augmented Generation (RAG)
* GraphRAG Architecture
* Knowledge Graph Construction
* Semantic Search
* Hybrid Retrieval Systems
* FastAPI Development
* LLM Integration
* Code Intelligence Systems
* Repository Analysis

---

## License

MIT License
