import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def analyze_reviews_llm(reviews):
    """
    Analyzes reviews using OpenAI if available, returning structured JSON metrics.
    If no API key, returns None to fallback to TextBlob.
    """
    if not client:
        return None
        
    combined_reviews = " ".join(reviews[:10]) # Limit to top 10 to save tokens
    
    prompt = f"""
    Analyze the following hotel reviews and provide structured metrics.
    Return ONLY a raw JSON string (no markdown formatting, no backticks).
    
    Metrics needed:
    - sentiment_score (float between -1.0 and 1.0)
    - keyword_counts (object counting occurrences of concepts relating to: family, couple, budget, cleanliness, service)
    
    Reviews:
    {combined_reviews}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a hotel review analysis API."},
                      {"role": "user", "content": prompt}],
            temperature=0.0
        )
        # Parse the JSON (safely removing potential markdown)
        result_text = response.choices[0].message.content.strip()
        if result_text.startswith("```json"):
            result_text = result_text.split("```json")[-1].split("```")[0].strip()
        import json
        return json.loads(result_text)
    except Exception as e:
        print(f"OpenAI Analysis Error: {e}")
        return None
