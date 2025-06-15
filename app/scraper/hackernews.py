import requests
from bs4 import BeautifulSoup

def get_hackernews_articles(limit=5):
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    links = soup.select(".athing")

    for link in links[:limit]:
        title = link.select_one(".titleline a")
        if title:
            articles.append({
                "title": title.text,
                "link": title["href"],
                "summary": "Hacker News article",  # HN doesn't have summary
                "source": "Hacker News"
            })

    return articles
