import json
import random
import os

def generate_mock_data():
    hotel_templates = [
        {
            "hotel_name": "The Grand Horizon", "rating": 4.8, "review_count": 340, "location_distance_km": 1.2,
            "amenities": ["wifi", "pool", "spa", "restaurant"],
            "themes": ["luxury", "couples", "cleanliness"]
        },
        {
            "hotel_name": "Budget Inn Airport", "rating": 3.2, "review_count": 890, "location_distance_km": 15.0,
            "amenities": ["wifi", "parking"],
            "themes": ["budget", "service_issues"]
        },
        {
            "hotel_name": "Couples Retreat Beach Resort", "rating": 4.9, "review_count": 120, "location_distance_km": 4.5,
            "amenities": ["wifi", "pool", "spa", "private beach"],
            "themes": ["couples", "romantic", "luxury"]
        },
        {
            "hotel_name": "Family Fun Suites", "rating": 4.4, "review_count": 550, "location_distance_km": 8.0,
            "amenities": ["wifi", "pool", "kids area", "kitchen"],
            "themes": ["family", "cleanliness", "budget"]
        },
        {
            "hotel_name": "City Center Plaza", "rating": 4.1, "review_count": 1200, "location_distance_km": 0.5,
            "amenities": ["wifi", "gym", "restaurant", "bar"],
            "themes": ["service", "cleanliness"]
        },
        {
            "hotel_name": "Fake Paradise Resort", "rating": 5.0, "review_count": 25, "location_distance_km": 10.0,
            "amenities": ["pool"],
            "themes": ["fake"]
        },
        {
            "hotel_name": "Cozy Cabin Retreat", "rating": 4.7, "review_count": 85, "location_distance_km": 20.0,
            "amenities": ["kitchen", "fireplace", "parking"],
            "themes": ["couples", "romantic"]
        },
        {
            "hotel_name": "Backpacker Hostel Central", "rating": 3.8, "review_count": 450, "location_distance_km": 1.0,
            "amenities": ["wifi", "bar", "laundry"],
            "themes": ["budget", "young"]
        },
        {
            "hotel_name": "Oceanview Luxury Hotel", "rating": 4.6, "review_count": 410, "location_distance_km": 2.5,
            "amenities": ["wifi", "pool", "spa", "restaurant", "gym"],
            "themes": ["luxury", "couples", "service"]
        },
        {
            "hotel_name": "The Historic Manor", "rating": 4.5, "review_count": 210, "location_distance_km": 3.0,
            "amenities": ["wifi", "parking", "restaurant"],
            "themes": ["couples", "cleanliness"]
        },
        {
            "hotel_name": "Business Express", "rating": 4.0, "review_count": 800, "location_distance_km": 5.0,
            "amenities": ["wifi", "gym", "meeting rooms"],
            "themes": ["service", "cleanliness"]
        },
        {
            "hotel_name": "Green Eco Lodge", "rating": 4.7, "review_count": 150, "location_distance_km": 30.0,
            "amenities": ["restaurant", "hiking trails"],
            "themes": ["couples", "cleanliness"]
        },
        {
            "hotel_name": "Suburban Motel", "rating": 2.5, "review_count": 60, "location_distance_km": 12.0,
            "amenities": ["parking"],
            "themes": ["budget", "service_issues", "fake_bad"]
        },
        {
            "hotel_name": "Downtown Boutique", "rating": 4.8, "review_count": 300, "location_distance_km": 0.2,
            "amenities": ["wifi", "bar", "spa"],
            "themes": ["luxury", "couples", "service"]
        },
        {
            "hotel_name": "Riverside Family Camp", "rating": 4.2, "review_count": 400, "location_distance_km": 18.0,
            "amenities": ["pool", "kids area", "parking", "bbq"],
            "themes": ["family", "budget"]
        }
    ]

    review_pool = {
        "luxury": ["Absolutely stunning experience.", "Very luxurious and pristine.", "Worth every penny for the quality.", "High-end amenities and great views."],
        "couples": ["Perfect for our honeymoon!", "Very romantic vibe.", "My partner and I loved the private settings.", "A romantic getaway, highly recommended."],
        "family": ["Great for kids and the family loved it.", "The child care and kids area were fantastic.", "Spacious rooms for a large family.", "Safe and fun for children."],
        "cleanliness": ["Spotlessly clean rooms.", "The hygiene here is top notch.", "Clean and tidy.", "Bathroom was very clean."],
        "service": ["Staff was incredibly helpful and friendly.", "Excellent room service.", "The concierge went out of their way to help.", "Great service from the team."],
        "budget": ["Very affordable and cheap.", "Great value for money.", "Good price for what you get.", "Cheap but comfortable."],
        "service_issues": ["Staff was rude.", "Terrible service, waited for hours.", "Room was not ready on time.", "Unprofessional front desk."],
        "fake": ["good.", "nice.", "great.", "good.", "ok.", "good.", "perfect hotel no flaws 5 stars!!", "good."],
        "fake_bad": ["bad.", "bad.", "worst ever.", "bad.", "do not go here.", "bad."]
    }

    hotels = []
    for h in hotel_templates:
        hotel_reviews = []
        themes = h.pop("themes")
        
        # generate 15-30 reviews per hotel
        num_reviews = random.randint(15, 30)
        
        # Special case for fake bots (too many similar short reviews)
        if "fake" in themes:
            for _ in range(num_reviews):
                hotel_reviews.append(random.choice(review_pool["fake"]))
        else:
            for _ in range(num_reviews):
                chosen_theme = random.choice(themes)
                base_review = random.choice(review_pool.get(chosen_theme, review_pool["service"]))
                hotel_reviews.append(base_review)
                
        h["reviews"] = hotel_reviews
        hotels.append(h)

    from backend.database import save_hotels_data
    save_hotels_data(hotels)
    print(f"Successfully generated/saved mock data for {len(hotels)} hotels.")

if __name__ == "__main__":
    generate_mock_data()
