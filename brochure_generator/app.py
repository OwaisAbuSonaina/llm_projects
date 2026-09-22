from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import uvicorn

from service import prompt_and_generate_brochure

app = FastAPI()

class BrochureRequest(BaseModel):
    url: str
    company_name: str | None = None

@app.get("/")
def read_root():
    return {"message": "Brochure Generator is Ready!"}

@app.post("/generate")
def generate(payload: BrochureRequest):
    try:
        result = prompt_and_generate_brochure(payload.url, payload.company_name)
        return {
            "status": "success",
            "data": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)