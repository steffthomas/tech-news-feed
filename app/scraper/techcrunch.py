import requests
from bs4 import BeautifulSoup

def get_techcrunch_articles(limit=5):
    url = "https://techcrunch.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    posts = soup.select("a.post-block__title__link")

    for post in posts[:limit]:
        title = post.get_text(strip=True)
        link = post["href"]
        articles.append({
            "title": title,
            "link": link,
            "summary": "TechCrunch article",  # Could improve with deep scrape
            "source": "TechCrunch"
        })

    return articles
