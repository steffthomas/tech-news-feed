import requests
from bs4 import BeautifulSoup

def get_techcrunch_articles(limit=15):
    url = "https://techcrunch.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    posts = soup.select("a.post-block__title__link")

    for post in posts[:limit]:
        title = post.get_text(strip=True)
        link = post["href"]

        # Default summary and image
        summary = "Click to read full article"
        image = "https://source.unsplash.com/400x200/?tech"

        try:
            article_page = requests.get(link, timeout=5)
            article_soup = BeautifulSoup(article_page.text, "html.parser")

            # Try to get meta description
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

            # Try to get og:image
            og_image = article_soup.find("meta", property="og:image")
            if og_image and og_image.get("content"):
                image = og_image["content"]
        except Exception as e:
            print(f"[Warning] Could not fetch TechCrunch details for: {link} — {e}")

        articles.append({
            "title": title,
            "link": link,
            "summary": summary,
            "source": "TechCrunch",
            "image": image
        })

    return articles
