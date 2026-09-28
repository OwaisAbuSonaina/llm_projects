# FlightAI Assistant

A multimodal airline customer service assistant powered by OpenAI, FastAPI, and Gradio. The assistant can look up ticket prices, answer questions, generate promotional travel images for requested destinations, and speak responses back using text-to-speech.

## Features

- **Conversational Booking Assistant:** Short, courteous answers using OpenAI function calling.

- **Flight Pricing Database:** SQLite database holding destination prices.

- **Dynamic Image Generation:** Automatically generates a destination vacation image when a city is mentioned.

- **Voice Response:** Generates speech audio for assistant answers.

- **Interactive UI:** Gradio frontend supporting chat, image preview, and autoplaying audio.

## Tech Stack

- **Backend:** FastAPI, Uvicorn, SQLite3

- **Frontend:** Gradio

- **AI Services:** OpenAI API (Chat completions, TTS, Image generation)

- **Dependency Management & Containerization:** `uv`, Docker, Docker Compose

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/?utm_source=gemini) and Docker Compose installed.

- An [OpenAI API key](https://platform.openai.com/?utm_source=gemini).

### Setup Environment

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here

```

### Running with Docker Compose (Recommended)

Build and start both the backend and frontend containers:

```
docker compose up --build -d

```

- **Frontend (Gradio UI):** [http://localhost:7860](http://localhost:7860?utm_source=gemini)

- **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs?utm_source=gemini)

## Local Development (Without Docker)

1. **Install dependencies:**
   Ensure you have Python 3.11+ and `uv` installed, then run:

   ```
   uv sync

   ```

2. **Initialize the Database:**

   ```
   python -m utils.initializing_database

   ```

3. **Start the FastAPI Backend:**

   ```
   uvicorn api:app --host 0.0.0.0 --port 8000 --reload

   ```

4. **Start the Gradio Frontend:**

   ```
   python utils/gradio_work.py

   ```

## Project Structure

```
├── api.py                    # FastAPI application and chat endpoint
├── docker-compose.yml        # Docker compose setup for backend & frontend
├── Dockerfile.backend        # Backend service Dockerfile
├── Dockerfile.frontend       # Gradio UI Dockerfile
├── pyproject.toml            # Project dependencies and config
├── prices.db                 # SQLite database (generated on startup)
└── utils/
    ├── artist_and_talker.py  # OpenAI image generation and TTS logic
    ├── client.py             # OpenAI client configuration
    ├── core.py               # Chat flow and tool calling logic
    ├── db_call.py            # Database queries for ticket prices
    ├── gradio_work.py        # Gradio interface definition
    └── initializing_database.py # Database table creation and seed data

```
