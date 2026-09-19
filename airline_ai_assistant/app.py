from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DATABASE_PATH = Path(__file__).with_name("prices.db")


class FlightQuery(BaseModel):
    message: str = Field(..., min_length=1, description="User request about a destination city")


class FlightResponse(BaseModel):
    city: str
    price: float
    currency: str = "USD"
    summary: str


app = FastAPI(title="FlightAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def initialize_database() -> None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS prices (city TEXT PRIMARY KEY, price REAL)"
        )
        connection.execute(
            "INSERT OR IGNORE INTO prices (city, price) VALUES (?, ?)",
            ("london", 799),
        )
        connection.execute(
            "INSERT OR IGNORE INTO prices (city, price) VALUES (?, ?)",
            ("paris", 899),
        )
        connection.execute(
            "INSERT OR IGNORE INTO prices (city, price) VALUES (?, ?)",
            ("tokyo", 1420),
        )
        connection.execute(
            "INSERT OR IGNORE INTO prices (city, price) VALUES (?, ?)",
            ("sydney", 2999),
        )
        connection.commit()


def get_ticket_price(city: str) -> float | None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        row = connection.execute(
            "SELECT price FROM prices WHERE city = ?",
            (city.lower(),),
        ).fetchone()
    return float(row[0]) if row else None


@app.on_event("startup")
def startup_event() -> None:
    initialize_database()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat", response_model=FlightResponse)
def chat_with_flight_ai(query: FlightQuery) -> FlightResponse:
    city = query.message.strip()
    normalized_city = city.lower()

    if not normalized_city:
        raise HTTPException(status_code=400, detail="Message is required.")

    reference_city = None
    for candidate in ["london", "paris", "tokyo", "sydney"]:
        if candidate in normalized_city:
            reference_city = candidate
            break

    if reference_city is None:
        raise HTTPException(
            status_code=404,
            detail="I can only quote flights for London, Paris, Tokyo, or Sydney.",
        )

    price = get_ticket_price(reference_city)
    if price is None:
        raise HTTPException(
            status_code=404,
            detail=f"No flight data found for {reference_city.title()}.",
        )

    return FlightResponse(
        city=reference_city.title(),
        price=price,
        summary=f"A return ticket to {reference_city.title()} costs ${price:.0f} USD.",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
