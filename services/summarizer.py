from typing import Dict, List


class NewsSummarizer:
    def summarize(self, articles: List[Dict], category: str, query: str = "", language: str = "en") -> Dict[str, str]:
        """
        Create separate summaries for voice and display.
        Returns a dict with 'voice' and 'display' keys.
        """
        if not articles:
            if language == 'ar':
                return {
                    "voice": "لم أتمكن من العثور على أي مقالات لتلخيصها.",
                    "display": "لم أتمكن من العثور على أي مقالات لتلخيصها."
                }
            return {
                "voice": "I could not find any articles to summarize.",
                "display": "I could not find any articles to summarize."
            }

        # Create voice content (without sources)
        if language == 'ar':
            if query:
                voice_lines = [f"إليك أبرز الأخبار عن '{query}':"]
                display_lines = [f"إليك أبرز الأخبار عن '{query}':"]
            else:
                voice_lines = [f"إليك أبرز الأخبار في فئة {category}:"]
                display_lines = [f"إليك أبرز الأخبار في فئة {category}:"]
        else:
            if query:
                voice_lines = [f"Here are the latest news highlights about '{query}':"]
                display_lines = [f"Here are the latest news highlights about '{query}':"]
            else:
                voice_lines = [f"Here are the latest {category} news highlights:"]
                display_lines = [f"Here are the latest {category} news highlights:"]

        # Process articles for voice and display
        for index, article in enumerate(articles, start=1):
            title = article.get("title", "No title available").strip()
            source = article.get("source", {}).get("name", "Unknown source")
            description = (article.get("description") or "").strip()
            url = article.get("url", "")

            # Voice content - only title and description, no source mention
            if description:
                voice_point = f"{index}. {title}. {description}"
            else:
                voice_point = f"{index}. {title}."

            voice_lines.append(voice_point)

            # Display content - includes source and formatted for display
            display_point = f"{index}. {title}. Source: {source}. {description}"
            display_lines.append(display_point)

        return {
            "voice": " ".join(voice_lines),
            "display": " ".join(display_lines)
        }

    def format_for_terminal(self, articles: List[Dict]) -> str:
        """
        Create a readable output for the terminal.
        """
        formatted_lines = []
        for index, article in enumerate(articles, start=1):
            title = article.get("title", "No title available")
            source = article.get("source", {}).get("name", "Unknown source")
            url = article.get("url", "No link available")
            formatted_lines.append(
                f"{index}. {title}\n   Source: {source}\n   Link: {url}\n"
            )

        return "\n".join(formatted_lines)
