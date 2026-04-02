import math
import numpy as np
from backend.utils import normalize_01, extract_highlights
from backend.analyzer import analyze_reviews
from backend.fake_review_detector import detect_fake_reviews

def score_and_rank_hotels(hotels, user_type):
    """
    Computes final scores for all hotels and ranks them.
    Includes NLP processing per hotel.
    """
    
    # 1. First pass: extract all raw metrics to compute min/max for normalization
    raw_data = []
    
    # Track extremes for normalization
    max_rev_count = max([h["review_count"] for h in hotels] + [1])
    min_rev_count = min([h["review_count"] for h in hotels] + [0])
    
    for h in hotels:
        # NLP Analysis with Fallback
        nlp_result = None
        try:
            from backend.analyzer_llm import analyze_reviews_llm
            nlp_result = analyze_reviews_llm(h.get("reviews", []))
        except ImportError:
            pass

        if not nlp_result:
            # Fallback to TextBlob
            nlp_result = analyze_reviews(h.get("reviews", []))
            
        sentiment = nlp_result["sentiment_score"]
        kw_counts = nlp_result["keyword_counts"]
        
        # Fake Detection
        fake_score = detect_fake_reviews(h.get("reviews", []))
        
        # Location Score
        dist = h.get("location_distance_km", 10.0)
        location_score = 1.0 / (dist + 1.0)
        
        # Personalized Keyword Score Computation
        base_kw_score = sum(kw_counts.values())
        
        # Boost specific keywords based on user_type
        if user_type == "honeymoon":
            kw_score = base_kw_score + (kw_counts.get("couple", 0) * 3)
        elif user_type == "family":
            kw_score = base_kw_score + (kw_counts.get("family", 0) * 3) + (kw_counts.get("cleanliness", 0) * 1)
        elif user_type == "budget":
            kw_score = base_kw_score + (kw_counts.get("budget", 0) * 3)
        else:
            kw_score = base_kw_score
            
        raw_data.append({
            "hotel": h,
            "rating": h["rating"],
            "review_count": h["review_count"],
            "sentiment": sentiment,
            "fake_score": fake_score,
            "location_score": location_score,
            "keyword_score_raw": kw_score,
            "kw_counts_dict": kw_counts
        })
        
    # Find max keyword score for normalization
    max_kw = max([d["keyword_score_raw"] for d in raw_data] + [1])
    
    results = []
    
    # 2. Second pass: Compute Final Normalized formula
    for data in raw_data:
        norm_rating = data["rating"] / 5.0
        
        # Log scaling for review counts (giving diminishing returns)
        log_rev = math.log10(data["review_count"] + 1)
        max_log_rev = math.log10(max_rev_count + 1)
        norm_log_rev = log_rev / max_log_rev if max_log_rev > 0 else 0
        
        # Sentiment maps from [-1, 1] to [0, 1]
        norm_sentiment = (data["sentiment"] + 1.0) / 2.0
        
        # Keyword norm
        norm_kw = data["keyword_score_raw"] / max_kw
        
        # Apply formula
        final_score = (
            0.35 * norm_rating +
            0.20 * norm_log_rev +
            0.15 * norm_sentiment +
            0.10 * norm_kw +
            0.10 * data["location_score"] -
            0.10 * data["fake_score"]
        )
        
        # Scale to 1-10 for frontend readability
        final_score_mapped = max(0.0, min(10.0, final_score * 10))
        
        highlights = extract_highlights(
            data["hotel"], 
            data["sentiment"], 
            data["fake_score"], 
            data["kw_counts_dict"], 
            user_type
        )
        
        # Generate generic reason based on persona
        reason = f"Ranked high for {user_type} due to overall quality and metrics."
        if user_type == "honeymoon": reason = "Top choice for a romantic stay based on review sentiment."
        elif user_type == "family": reason = "Excellent family-friendly environment and amenities."
        elif user_type == "budget": reason = "Outstanding value for money based on pricing keywords."
        else: reason = "Solid all-rounder based on AI analysis."
        
        results.append({
            "hotel_name": data["hotel"]["hotel_name"],
            "score": round(final_score_mapped, 1),
            "reason_for_recommendation": reason,
            "highlights": highlights,
            "metrics": {
                "sentiment_value": round(data["sentiment"], 2),
                "fake_risk_score": round(data["fake_score"], 2)
            }
        })
        
    # Sort descending by score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:5]
