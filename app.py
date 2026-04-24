from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import DEFAULT_CATEGORY, SUPPORTED_CATEGORIES
from services.news_service import NewsService
from services.summarizer import NewsSummarizer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

news_service = NewsService()
summarizer = NewsSummarizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_news', methods=['POST'])
def get_news():
    data = request.get_json()
    user_query = data.get('query', '').strip()
    category = data.get('category', DEFAULT_CATEGORY)
    language = data.get('language', 'en')

    # Preprocess the query to extract better search terms
    processed_query = preprocess_query(user_query) if user_query else None

    if not category or category == "Auto-detect":
        category = detect_category(user_query) if user_query else DEFAULT_CATEGORY

    try:
        articles = news_service.get_top_headlines(
            category=category,
            country=None,
            query=processed_query,
            language=language,
        )
        summary_data = summarizer.summarize(articles, category, user_query, language)
        return jsonify({
            'success': True,
            'voice_summary': summary_data['voice'],
            'display_summary': summary_data['display'],
            'articles': articles
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def preprocess_query(query: str) -> str:
    """
    Clean up and improve the user's query for better search results.
    """
    if not query:
        return ""

    # Convert to lowercase
    query = query.lower()

    # Remove common question words and phrases
    question_starters = [
        "what", "what's", "what is", "what are", "what happened", "what happen",
        "what's happening", "what is happening", "what happened with",
        "tell me about", "give me", "show me", "news about", "latest",
        "who", "where", "when", "why", "how",
        "is there", "are there", "do you know", "can you tell me"
    ]

    # Remove question starters
    for starter in question_starters:
        if query.startswith(starter + " "):
            query = query[len(starter) + 1:]
            break

    # Remove filler words
    filler_words = ["about", "regarding", "concerning", "the", "a", "an", "in", "on", "at", "to"]
    words = query.split()
    filtered_words = [word for word in words if word not in filler_words]
    query = ' '.join(filtered_words)

    # Clean up common typos and improve terms
    replacements = {
        "nasa": "NASA",
        "real madrid": "Real Madrid",
        "manchester united": "Manchester United",
        "barcelona": "Barcelona",
        "covid": "COVID-19",
        "coronavirus": "COVID-19",
        "president": "President",
        "government": "government",
        "election": "election",
        "war": "war",
        "crisis": "crisis",
        "space": "space",
        "mission": "mission"
    }

    for old, new in replacements.items():
        query = query.replace(old, new)

    # Remove extra whitespace and punctuation
    import re
    query = re.sub(r'[^\w\s]', '', query)  # Remove punctuation
    query = ' '.join(query.split())  # Normalize whitespace

    # If query is too short or empty, try to extract key terms from original
    if len(query.split()) < 2:
        original_words = query.split()
        # Look for proper nouns (capitalized words) or known entities
        key_terms = []
        for word in original_words:
            if word in ["NASA", "COVID", "President"] or word[0].isupper():
                key_terms.append(word)
        if key_terms:
            query = ' '.join(key_terms)

    return query.strip()

def detect_category(user_text: str) -> str:
    """
    Detect a news category from the user's spoken question.
    """
    lowered_text = user_text.lower()

    for category in SUPPORTED_CATEGORIES:
        if category in lowered_text:
            return category

    # Extended keyword detection
    if "tech" in lowered_text or "technology" in lowered_text or "computer" in lowered_text:
        return "technology"
    if "sport" in lowered_text or "sports" in lowered_text or "football" in lowered_text or "soccer" in lowered_text:
        return "sports"
    if "health" in lowered_text or "medical" in lowered_text or "doctor" in lowered_text:
        return "health"
    if "science" in lowered_text or "nasa" in lowered_text or "space" in lowered_text or "mission" in lowered_text or "astronaut" in lowered_text:
        return "science"
    if "business" in lowered_text or "economy" in lowered_text or "market" in lowered_text:
        return "business"
    if "world" in lowered_text or "international" in lowered_text or "global" in lowered_text:
        return "world"

    return DEFAULT_CATEGORY

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)