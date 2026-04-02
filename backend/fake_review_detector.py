from collections import Counter

def detect_fake_reviews(reviews):
    """
    Implements heuristic-based detection of fake reviews.
    Returns a float score (higher = more suspicious).
    """
    if not reviews:
        return 0.0
        
    num_reviews = len(reviews)
    short_review_count = 0
    
    review_lengths = []
    
    normalized_reviews = [r.lower().strip() for r in reviews]
    counts = Counter(normalized_reviews)
    
    # Calculate duplicates
    duplicate_count = sum(count - 1 for count in counts.values() if count > 1)
    
    for r in reviews:
        words = r.split()
        if len(words) < 5:
            short_review_count += 1

    short_ratio = short_review_count / num_reviews
    duplicate_ratio = duplicate_count / num_reviews
    
    # Base formula for fake score
    fake_score = (short_ratio * 0.5) + (duplicate_ratio * 0.6)
    
    # Extreme bias could be added here (e.g., if all reviews are identical)
    # But for now, ratio of duplicates and exceptionally short flags are enough.
    
    # Normalize to roughly 0 - 1
    return min(fake_score, 1.0)
