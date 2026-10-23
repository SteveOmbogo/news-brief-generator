
import os
import requests
from dotenv import load_dotenv


# --------------------------------------------------
# 1. LOAD THE API KEY
# --------------------------------------------------

load_dotenv()
api_key = os.getenv("NEWS_API_KEY")


# --------------------------------------------------
# 2. ASK THE USER TO CHOOSE A CATEGORY
# --------------------------------------------------

def choose_category():
    print("\n" + "=" * 50)
    print("             NEWS BRIEF GENERATOR")
    print("=" * 50)
    print("Choose a news category:")
    print("1. Technology")
    print("2. Business")
    print("3. Health")

    choices = {
        "1": "technology",
        "2": "business",
        "3": "health"
    }

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice in choices:
            return choices[choice]

        print("Invalid choice. Please enter 1, 2, or 3.")


# --------------------------------------------------
# 3. PREPARE THE API REQUEST
# --------------------------------------------------

def get_news(category):

    if category == "health":
        # Search for health-related news articles
        url = "https://newsapi.org/v2/everything"

        params = {
            "q": "health OR healthcare OR medical",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 5
        }

    else:
        # Fetch top headlines for technology or business
        url = "https://newsapi.org/v2/top-headlines"

        params = {
            "category": category,
            "language": "en",
            "pageSize": 5
        }

    headers = {"X-Api-Key": api_key}

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=15
    )

    return response


# --------------------------------------------------
# 4. DISPLAY THE NEWS BRIEF
# --------------------------------------------------

def display_news(category, articles, total_results):

    print("\n" + "=" * 70)
    print(f"              YOUR {category.upper()} NEWS BRIEF")
    print("=" * 70)

    print(f"\nTotal matching articles reported by API: {total_results}")
    print(f"Articles displayed: {len(articles)}")

    if not articles:
        print("\nNo articles were returned. Please try again later.")
        return

    for number, article in enumerate(articles, start=1):

        title = article.get("title") or "No title available"
        description = (
            article.get("description")
            or "No description available."
        )

        source = article.get("source") or {}
        publisher = source.get("name") or "Unknown publisher"

        published_at = (
            article.get("publishedAt") or "Unknown date"
        )

        article_url = article.get("url") or "No link available"

        print(f"\n{number}. {title}")
        print(f"   Publisher: {publisher}")
        print(f"   Published: {published_at}")
        print(f"   Summary: {description}")
        print(f"   Read more: {article_url}")
        print("-" * 70)


# --------------------------------------------------
# 5. RUN THE APPLICATION
# --------------------------------------------------

def main():

    if not api_key:
        print("Error: NEWS_API_KEY was not found in your .env file.")
        return

    category = choose_category()

    try:
        response = get_news(category)
        data = response.json()

        if response.status_code == 200 and data.get("status") == "ok":

            articles = data.get("articles", [])
            total_results = data.get("totalResults", 0)

            display_news(category, articles, total_results)

            print("\nNews brief completed successfully.")

        else:
            print("\nThe API request was unsuccessful.")
            print("HTTP status code:", response.status_code)
            print("Reason:", data.get("message", "Unknown API error"))

    except requests.exceptions.Timeout:
        print("\nThe request timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        print("\nConnection failed. Check your internet connection.")

    except requests.exceptions.RequestException as error:
        print("\nA request error occurred:", error)

    except ValueError:
        print("\nThe API response could not be decoded as JSON.")


if __name__ == "__main__":
    main()

