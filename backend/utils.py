import math

def normalize_01(val, min_val, max_val):
    """Normalize a value to 0-1 range based on given min/max."""
    if max_val == min_val:
        return 0.5
    return (val - min_val) / (max_val - min_val)

def extract_highlights(hotel_data, sentiment, fake_score, keyword_counts, user_type):
    """Generate dynamic highlights for a hotel based on its scores and the persona."""
    highlights = []
    
    if hotel_data["rating"] >= 4.5:
        highlights.append(f"Excellent overall rating ({hotel_data['rating']}⭐)")
        
    if sentiment > 0.4:
        highlights.append("Glowing guest sentiment in recent reviews")
        
    if fake_score < 0.1:
        highlights.append("Highly trustworthy reviews (low fake risk)")
    elif fake_score > 0.5:
        highlights.append("Warning: Higher than usual fake review risk")
        
    if hotel_data["location_distance_km"] < 2.0:
        highlights.append("Prime location near city center")
        
    # User type specific highlights
    if user_type == "honeymoon" and keyword_counts.get("couple", 0) > 2:
        highlights.append("Top choice for couples and honeymooners")
    elif user_type == "family" and keyword_counts.get("family", 0) > 2:
        highlights.append("Highly recommended for families with kids")
    elif user_type == "budget" and keyword_counts.get("budget", 0) > 2:
        highlights.append("Exceptional value for money")
        
    if not highlights:
        highlights.append("A solid balanced choice")
        
    return highlights[:3] # Return top 3 highlights
