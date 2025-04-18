# tankAI
# TankAIProject

**TankAIProject** is an advanced AI-powered project report generator designed to analyze any GitHub repository, extract its code and structure, and generate a hierarchical, chunked, and summarized representation of the entire codebase. It enables users (or other LLMs) to understand and regenerate code from natural language summaries — making it ideal for documentation, code comprehension, and showcasing project architecture to recruiters.

---

##  Features

- **Clone & Extract**: Clone any public GitHub repo and extract all file contents recursively, skipping irrelevant binaries or metadata files.
-  **Smart Chunking**: Break down code files into logical units like functions, classes, and imports using regex-based pattern matching.
- **Hierarchical Summarization**: Summarize code from the snippet level all the way up to the directory level using a local LLM like **Mistral via Ollama**.
- **Full Project Tree Representation**: The tool creates a structured dictionary capturing your entire repository’s file and folder hierarchy.
- **Reconstructable Summaries**: Summaries are designed so another LLM can accurately regenerate the original code — ideal for explainability and auditability.

---

## 🛠Setup Guidelines

### 1. Prerequisites

Make sure you have the following installed:

- Python 3.8+
- `git` and `gitpython` (for repo cloning)
- `ollama` (for running Mistral locally)
- Mistral model pulled locally using Ollama:  
  ```bash
  ollama pull mistral


Note (Current Scope)
TankAI is in a premature development stage. While designed as a general-purpose GitHub analyzer, it currently supports MERN stack projects only (MongoDB, Express.js, React, Node.js). Support for other languages and frameworks is in progress.
