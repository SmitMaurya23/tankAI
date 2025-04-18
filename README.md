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

Here’s the exact markdown-formatted README.md section you asked for, ready to paste directly:

## Python Dependencies

Install required libraries:

bash
pip install gitpython
(Optional but recommended)

pip install tqdm
Clone the Repo to Analyze
Edit the repo_url variable in tankAImodel.py:

repo_url = "https://github.com/<your-username>/<your-repo>.git"
This will clone the repo into a local directory (repo_clone by default).

##Usage
Run the entire script:

python tankAImodel.py
##It will:
Clone the target repo.
Extract project content, skipping binaries and config trash.
Chunk source code into functions, classes, imports, etc.
Use Ollama (Mistral model) to summarize each chunk and file.
Generate hierarchical summaries for each directory and the entire project.

##Output
The script builds structured dictionaries like:

project_content_code: raw content extracted from files

chunked_project_code: logically chunked code snippets

summarized_project_code: recursively summarized content with natural language explanations

You can save any of these dictionaries using the save_dict_to_txt() function.

##Internals
The project implements:

Recursive file system traversal with content filtering.

Regex-based chunking for Python, JS, Java, C/C++, PHP, and more.

Summary generation via local subprocess calls to ollama run mistral.

Robust error handling for binary files and decoding issues.

##Future Work
Support more languages and frameworks.

UI to visualize summaries and file structures.

LLM self-evaluation and rating of summaries.

##Note (Current Scope)
TankAI is in a premature development stage. While designed as a general-purpose GitHub analyzer, it currently supports MERN stack projects only (MongoDB, Express.js, React, Node.js). Support for other languages and frameworks is in progress.
