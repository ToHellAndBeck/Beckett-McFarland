import requests
from datetime import datetime, timedelta

API_KEY = "1f14fe829730415b8ed33c4a64e52847"
NEWS_API_URL = "https://newsapi.org/v2/everything"

def get_top_geopolitics_news(api_key, from_date, to_date, page_size=10):
    # Set the query to search for news related to geopolitics
    query = "geopolitics"

    params = {
        "apiKey": api_key,
        "pageSize": page_size,
        "from": from_date,
        "to": to_date,
        "q": query
    }
    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        return articles
    else:
        print("Error fetching news:", response.status_code)
        print("Error message:", response.json().get("message", "Unknown error"))
        return None

if __name__ == "__main__":
    # Calculate from and to dates for the past week
    to_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")  # Today's date
    from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")  # 7 days ago

    # Fetch the top 10 geopolitics news articles from the past week
    geopolitics_articles = get_top_geopolitics_news(API_KEY, from_date, to_date)

    if geopolitics_articles:
        print("Top 10 Geopolitics News Stories from the Past Week:\n")
        for index, article in enumerate(geopolitics_articles[:10], start=1):
            print(f"News {index}:")
            print("Title:", article.get("title"))
            print("Source:", article.get("source", {}).get("name"))
            print("Description:", article.get("description"))
            print("URL:", article.get("url"))
            print("Published At:", article.get("publishedAt"))
            print("\n")
    else:
        print("No geopolitics news articles found.")
