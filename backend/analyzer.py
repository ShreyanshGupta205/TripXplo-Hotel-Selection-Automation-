from textblob import TextBlob
from collections import Counter

def analyze_reviews(reviews):
    """
    Analyzes a list of reviews and returns the average sentiment score
    and exact keyword counts for categorized aspects.
    """
    total_sentiment = 0.0
    
    # Target keywords as per user specs
    categories = {
        "family": ["kids", "child", "family", "children"],
        "couple": ["honeymoon", "romantic", "couple", "couples"],
        "budget": ["cheap", "affordable", "value", "price"],
        "cleanliness": ["clean", "hygiene", "tidy", "spotless"],
        "service": ["staff", "service", "helpful", "friendly", "concierge"]
    }
    
    keyword_counts = {cat: 0 for cat in categories.keys()}
    
    for review in reviews:
        blob = TextBlob(review)
        total_sentiment += blob.sentiment.polarity
        
        words = blob.words.lower()
        for cat, kw_list in categories.items():
            for kw in kw_list:
                if kw in words:
                    keyword_counts[cat] += 1
                    
    avg_sentiment = total_sentiment / len(reviews) if reviews else 0.0
    
    return {
        "sentiment_score": avg_sentiment,  # from -1.0 to 1.0
        "keyword_counts": keyword_counts
    }
