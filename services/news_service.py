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
    TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
    SEARCH_URL = "https://newsapi.org/v2/everything"

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
        Fetch the latest headlines from NewsAPI.org.
        """
        if not self.api_key:
            raise RuntimeError(
                "Missing NEWS_API_KEY. Add your API key to the .env file."
            )

        params = {
            "apiKey": self.api_key,
            "pageSize": max_headlines,
            "language": language,
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
                error_data = response.json()
                if "message" in error_data:
                    details = error_data["message"]
                elif "error" in error_data:
                    details = error_data["error"]
                else:
                    details = response.text
            except Exception:
                details = response.text
            raise RuntimeError(f"News API request failed: {details}") from error
        except requests.exceptions.RequestException as error:
            raise RuntimeError(f"Failed to fetch news: {error}") from error

        articles = data.get("articles", [])
        if not articles:
            raise RuntimeError("No news articles were found for this category.")

        return articles
