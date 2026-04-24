from typing import Dict, List

import requests

from config import (
    DEFAULT_CATEGORY,
    DEFAULT_COUNTRY,
    LANGUAGE,
    MAX_HEADLINES,
    NEWS_API_KEY,
)


class NewsService:
    TOP_HEADLINES_URL = "https://gnews.io/api/v4/top-headlines"
    SEARCH_URL = "https://gnews.io/api/v4/search"

    def __init__(self, api_key: str = NEWS_API_KEY) -> None:
        self.api_key = api_key

    def get_top_headlines(
        self,
        category: str = DEFAULT_CATEGORY,
        max_headlines: int = MAX_HEADLINES,
        country: str | None = DEFAULT_COUNTRY,
        query: str | None = None,
        language: str = LANGUAGE,
    ) -> List[Dict]:
        """
        Fetch the latest headlines from GNews.
        """
        if not self.api_key:
            raise RuntimeError(
                "Missing NEWS_API_KEY. Add your API key to the .env file."
            )

        params = {
            "lang": language,
            "max": max_headlines,
            "apikey": self.api_key,
        }
        
        if query:
            # Use search endpoint for specific queries
            url = self.SEARCH_URL
            params["q"] = query
            # When searching, we can still use category to narrow results
            if category and category != DEFAULT_CATEGORY:
                params["category"] = category
        else:
            # Use top-headlines endpoint for category-based news
            url = self.TOP_HEADLINES_URL
            params["category"] = category
            
        if country:
            params["country"] = country

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.ConnectionError as error:
            raise RuntimeError(
                "No internet connection. Please connect to the internet and try again."
            ) from error
        except requests.exceptions.Timeout as error:
            raise RuntimeError("The news API took too long to respond.") from error
        except requests.exceptions.HTTPError as error:
            details = ""
            try:
                details = response.json().get("errors", "")
            except Exception:
                details = response.text
            raise RuntimeError(f"News API request failed: {details}") from error
        except requests.exceptions.RequestException as error:
            raise RuntimeError(f"Failed to fetch news: {error}") from error

        articles = data.get("articles", [])
        if not articles:
            raise RuntimeError("No news articles were found for this category.")

        return articles
