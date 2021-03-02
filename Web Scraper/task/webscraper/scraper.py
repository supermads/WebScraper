import requests
from bs4 import BeautifulSoup
import string


def save_news_articles():
    url = "https://www.nature.com/nature/articles"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    articles = soup.find_all("article")
    saved_articles = []

    for i in range(len(articles)):
        article_type = articles[i].find("span", {"data-test": "article.type"}).text.strip()

        if article_type == "News":
            article_title = articles[i].find("h3", {"class": "c-card__title"}).text.strip().replace(" ", "_")

            for char in article_title:
                if char in string.punctuation and char != "_":
                    article_title = article_title.replace(char, "")

            file_name = f"{article_title}.txt"

            body_link = articles[i].find("a", {"data-track-action": "view article"})
            body_url = f"http://nature.com{body_link.get('href')}"

            r = requests.get(body_url)
            soup = BeautifulSoup(r.content, 'html.parser')

            with open(file_name, "wb") as f:
                body = soup.find("div", {"class": "article__body"}).text.strip()
                f.write(body.encode("UTF-8"))

            saved_articles.append(file_name)

    print("Saved articles\n", saved_articles)


save_news_articles()
