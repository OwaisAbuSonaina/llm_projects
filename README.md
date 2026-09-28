# LLM Projects

A collection of hands-on applications and experiments exploring practical Large Language Model (LLM) techniques, architectures, and deployments—including function calling, retrieval-augmented generation (RAG), multimodal generation, and agentic workflows.

---

## Repository Overview

Each subfolder is an independent module with its own implementation details:

| Project                           | Description                                                                                                             | Core Concepts                                          |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------- |
| **`airline_ai_assistant`**        | Multimodal conversational flight assistant featuring tool calling, TTS voice response, and contextual image generation. | Tool/Function calling, SQLite, Gradio, FastAPI, Docker |
| **`brochure_generator`**          | Automated generation of structured marketing brochures and company summaries from input URLs and prompts.               | Structured outputs, Web scraping, Prompt engineering   |
| **`meeting_minutes_creator`**     | Automated audio/transcript processing to extract executive summaries, action items, and discussion points.              | Speech-to-text, Summarization, Information extraction  |
| **`python_c++_converter`**        | Code translation and refactoring utility converting Python scripts into performant C++ implementations.                 | Code LLMs, AST alignment, Code verification            |
| **`rag_based_question_answerer`** | Question-answering pipeline using document embeddings and vector retrieval for accurate domain querying.                | RAG, Vector search, Embeddings, Context injection      |

---

## Tech Stack & Tooling

- **Language:** Python 3.11+, C++
- **Package Management:** `uv` (Fast Python package manager)
- **Serving & UI:** FastAPI, Gradio, Uvicorn
- **Containerization:** Docker & Docker Compose
- **Models & APIs:** OpenAI API (`gpt-4o-mini`, DALL·E / GPT-Image, TTS)

---

## Getting Started

### Prerequisites

- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) installed locally
- Docker & Docker Compose (optional, for containerized runs)
- An active OpenAI API key

### Environment Setup

1. **Clone the repository:**

```bash
   git clone https://github.com/OwaisAbuSonaina/llm_projects.git
   cd llm_projects

```

2. **Set your API credentials:**

```bash
cp .env.example .env
# Add your key inside .env:
# OPENAI_API_KEY=sk-...

```

3. **Install root dependencies with `uv`:**

```bash
uv sync

```

---

## Running a Project

Most subfolders contain dedicated entry points or Docker configurations.

### Option 1: Local execution

Navigate to the desired project directory and activate the environment:

```bash
# Example: Running the airline assistant backend
cd airline_ai_assistant
uv run python -m utils.initializing_database
uv run python api.py

```

### Option 2: Docker Compose (where applicable)

For projects equipped with multi-container setups (e.g., FastAPI backend + Gradio frontend):

```bash
cd <project_folder>
docker compose up --build

```

---
