import requests
from bs4 import BeautifulSoup
import string
import os


def save_pages():
    num_pages = int(input())
    chosen_article_type = input()
    curr_dir = os.getcwd()
    url = "https://www.nature.com/nature/articles"

    for i in range(1, num_pages + 1):
        new_dir = curr_dir + f"/Page_{i}"
        os.mkdir(new_dir)

        if i > 1:
            url = url + f"?searchType=journalSearch&sort=PubDate&page={i}"

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all("article")

        for j in range(len(articles)):
            article_type = articles[j].find("span", {"data-test": "article.type"}).text.strip()

            if article_type == chosen_article_type:
                article_title = articles[j].find("h3", {"class": "c-card__title"}).text.strip().replace(" ", "_")

                for char in article_title:
                    if char in string.punctuation and char != "_":
                        article_title = article_title.replace(char, "")

                body_link = articles[j].find("a", {"data-track-action": "view article"})
                body_url = f"http://nature.com{body_link.get('href')}"

                r = requests.get(body_url)
                soup = BeautifulSoup(r.content, 'html.parser')

                os.chdir(new_dir)
                file_name = f"{article_title}.txt"

                with open(file_name, "wb") as f:
                    try:
                        body = soup.find("div", {"class": "article-item__body"}).text.strip()
                    except AttributeError:
                        body = soup.find("div", {"class": "article__body cleared"}).text.strip()

                    f.write(body.encode("UTF-8"))

                os.chdir(curr_dir)

    print("Saved all articles.")


save_pages()
