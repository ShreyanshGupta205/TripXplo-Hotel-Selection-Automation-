import logging
from backend.scorer import score_and_rank_hotels

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("tripxplo-api")

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
    try:
        data = get_hotels_data()
        if not data:
            logger.warning("No hotel data found in database or JSON fallback.")
            raise HTTPException(status_code=404, detail="No hotel data found. Please run the scraper first.")
        logger.info(f"Successfully retrieved {len(data)} hotels.")
        return data
    except Exception as e:
        logger.error(f"Error fetching hotels: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching hotels.")

@app.post("/api/recommend")
def recommend_hotels(request: RecommendRequest):
    """Returns top 5 dynamically ranked hotels based on persona."""
    try:
        logger.info(f"Recommendation request received: Location={request.location}, Persona={request.user_type}")
        data = get_hotels_data()
        if not data:
            logger.warning("No hotel data found for recommendations.")
            raise HTTPException(status_code=404, detail="No hotel data available for ranking.")
            
        results = score_and_rank_hotels(data, request.user_type.lower())
        logger.info(f"Generated {len(results)} recommendations for {request.user_type}.")
        return results
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing recommendations: {str(e)}")

# Mount static frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
