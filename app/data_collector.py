import requests
import random

NEWS_API_KEY = "85ab8590fc1f447d908d02f9ba5d027e"  
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_headlines(country="us", page_size=10):
    categories = ["technology", "business", "health", "science", "sports"]
    category = random.choice(categories)
    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "category": category,
        "pageSize": page_size,
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [article["title"] for article in articles]
    else:
        print(f"Error fetching news: {response.status_code}")
        return []

if __name__ == "__main__":
    headlines = fetch_headlines()
    for i, headline in enumerate(headlines, 1):
        print(f"{i}. {headline}")
