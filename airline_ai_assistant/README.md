# Airline AI Assistant

A minimal airline travel assistant that exposes a FastAPI backend and a Streamlit frontend. The app accepts a destination city and returns a simple fare quote for a return trip.

## Prerequisites

- Docker
- Docker Compose

## Build and run

From this project directory:

```bash
cd airline_ai_assistant
docker compose up --build
```

To stop the stack:

```bash
docker compose down
```

## Access

- Streamlit UI: http://localhost:8501
- FastAPI API docs: http://localhost:8000/docs

## Notes

The backend is intentionally simple and uses a small SQLite database seeded with sample city prices. The frontend only communicates with the backend through HTTP requests, keeping the UI thin and client-side.
