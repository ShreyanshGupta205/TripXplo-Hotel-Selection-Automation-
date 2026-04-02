# TripXplo AI Hotel Selection Engine

An intelligent, multi-persona AI Hotel Recommendation System that relies on NLP review sentiment analysis and heuristic-based fake review detection to provide dynamic hotel rankings. 

This project was built securely as an internal prototype to evaluate hotels against user queries (e.g., Honeymoons, Family Retreats, Budget Stays) automatically highlighting relevant hotel pros while guarding against review manipulation.

## Features
- **Data Scraping Fallback (Mock Generator):** Generates varied hotels with themed reviews (luxury, couple, clean, faulty, fake). 
- **Sentiment Analysis (`textblob`):** Evaluates overall emotional sentiment in reviews.
- **Fake Review Bot Detection:** Checks for spam patterns such as exceptionally short reviews or duplicated bot templates.
- **Dynamic Scorer:** Weights raw rating, volume of logs, sentiment polarity, and specific keyword density against the user's Persona.
- **Beautiful UI Presentation:** Modern responsive dashboard.

## Tech Stack
- **Backend:** Python + FastAPI
- **NLP:** TextBlob / NLTK
- **Frontend:** Vanilla HTML/JS (No complex build step, lightweight)
- **Data:** JSON fallback

## Setup Instructions

**1. Create a Python environment & Install Dependencies**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**2. Generate Mock Data**
We provide a scraper fallback that populates realistic mock data in the database locally.
```bash
python backend/scraper.py
```
*This simulates web scraping and will populate `data/hotels.json`.*

**3. Run the Server**
```bash
uvicorn backend.main:app --reload
```

## API Usage

The system exposes RESTful endpoints:

### 1. `GET /api/hotels`
Fetch the raw datastore.

### 2. `POST /api/recommend`
Generates live AI-scored recommendations.
**Payload:**
```json
{
  "location": "Global",
  "user_type": "honeymoon"
}
```
**Response Sample:**
```json
[
  {
    "hotel_name": "Couples Retreat Beach Resort",
    "score": 9.4,
    "reason_for_recommendation": "Top choice for a romantic stay based on review sentiment.",
    "highlights": [
      "Excellent overall rating (4.9⭐)",
      "Glowing guest sentiment in recent reviews",
      "Highly trustworthy reviews (low fake risk)"
    ],
    "metrics": {
      "sentiment_value": 0.45,
      "fake_risk_score": 0.0
    }
  }
]
```
