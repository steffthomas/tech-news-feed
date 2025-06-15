import requests
from bs4 import BeautifulSoup

def get_hackernews_articles(limit=15):
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    links = soup.select(".athing")

    for link in links[:limit]:
        title_el = link.select_one(".titleline a")
        if not title_el:
            continue

        title = title_el.text
        link_url = title_el["href"]
        summary = "Click to read full article"

        # Try to fetch real content/summary from the article page
        try:
            article_page = requests.get(link_url, timeout=5)
            article_soup = BeautifulSoup(article_page.text, "html.parser")

            # Try og:description
            meta = article_soup.find("meta", property="og:description")
            if not meta:
                meta = article_soup.find("meta", attrs={"name": "description"})
            if meta and meta.get("content"):
                summary = meta["content"]
            else:
                # fallback to first paragraph
                first_p = article_soup.find("p")
                if first_p:
                    summary = first_p.get_text(strip=True)
        except Exception as e:
            print(f"[Warning] Could not fetch summary for: {link_url} — {e}")

        articles.append({
            "title": title,
            "link": link_url,
            "summary": summary,
            "source": "Hacker News"
        })

    return articles
