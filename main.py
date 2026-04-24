import argparse

from config import DEFAULT_CATEGORY, SUPPORTED_CATEGORIES
from services.news_service import NewsService
from services.speech_to_text import SpeechToTextService
from services.summarizer import NewsSummarizer
from services.text_to_speech import TextToSpeechService


def detect_category(user_text: str) -> str:
    """
    Detect a news category from the user's spoken question.
    """
    lowered_text = user_text.lower()

    for category in SUPPORTED_CATEGORIES:
        if category in lowered_text:
            return category

    if "tech" in lowered_text:
        return "technology"
    if "sport" in lowered_text:
        return "sports"
    if "health" in lowered_text:
        return "health"
    if "science" in lowered_text:
        return "science"
    if "business" in lowered_text:
        return "business"
    if "world" in lowered_text or "international" in lowered_text:
        return "world"

    return DEFAULT_CATEGORY


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


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Voice-Based AI News Assistant")
    parser.add_argument(
        "--text",
        action="store_true",
        help="Skip microphone input and use text input instead.",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="",
        help="Provide a question directly without interactive typing.",
    )
    parser.add_argument(
        "--category",
        type=str,
        default="",
        help="Force a category such as technology, sports, business, or health.",
    )
    parser.add_argument(
        "--country",
        type=str,
        default="",
        help="Optional two-letter country code such as in, us, or gb.",
    )
    parser.add_argument(
        "--voice",
        type=str,
        default="auto",
        choices=["auto", "male", "female"],
        help="Choose TTS voice: auto (default), male, or female.",
    )
    return parser.parse_args()


def main() -> None:
    print("Voice-Based AI News Assistant started.")
    args = parse_arguments()

    news_service = NewsService()
    summarizer = NewsSummarizer()
    tts_service = TextToSpeechService(voice_preference=args.voice)

    try:
        if args.query.strip():
            user_query = args.query.strip()
        elif args.text:
            user_query = input("Type your news question here: ").strip()
            if not user_query:
                raise RuntimeError("No question was provided in text input mode.")
        else:
            try:
                speech_service = SpeechToTextService()
                user_query = speech_service.listen()
            except RuntimeError as voice_error:
                print(f"Voice mode unavailable: {voice_error}")
                print("Switching to text input mode.")
                user_query = input("Type your news question here: ").strip()

                if not user_query:
                    raise RuntimeError("No question was provided in text input mode.")

        print(f"You said: {user_query}")

        category = args.category.strip().lower() or detect_category(user_query)
        print(f"Detected category: {category}")

        # Preprocess the query for better search results
        processed_query = preprocess_query(user_query)

        articles = news_service.get_top_headlines(
            category=category,
            country=args.country.strip().lower() or None,
            query=processed_query if processed_query else None,
        )
        print("\nLatest headlines:\n")
        print(summarizer.format_for_terminal(articles))

        spoken_response = summarizer.summarize(articles, category, user_query)
        print("Assistant response:")
        print(spoken_response)
        tts_service.speak(spoken_response)

    except RuntimeError as error:
        error_message = f"Error: {error}"
        print(error_message)
        tts_service.speak(error_message)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")


if __name__ == "__main__":
    main()
