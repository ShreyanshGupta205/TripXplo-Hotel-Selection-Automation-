from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from backend.scorer import score_and_rank_hotels

app = FastAPI(title="TripXplo AI Hotel Selection Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.database import get_hotels_data

class RecommendRequest(BaseModel):
    location: str
    user_type: str

@app.get("/api/hotels")
def get_hotels():
    """Returns all processed hotels without ranking."""
    data = get_hotels_data()
    if not data:
        raise HTTPException(status_code=404, detail="Mock data not found. Run scraper.py first.")
    return data

@app.post("/api/recommend")
def recommend_hotels(request: RecommendRequest):
    """Returns top 5 dynamically ranked hotels based on persona."""
    data = get_hotels_data()
    if not data:
        raise HTTPException(status_code=404, detail="Mock data not found. Run scraper.py first.")
        
    results = score_and_rank_hotels(data, request.user_type.lower())
    return results

# Mount static frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
