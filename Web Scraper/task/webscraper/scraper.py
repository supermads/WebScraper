import requests
from bs4 import BeautifulSoup


def get_movie_info():
    movie_info = {}
    url = input("Input the URL:\n")
    r = requests.get(url)
    try:
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find("h1").get_text(strip=True)
        try:
            # If the movie year is included in the title, remove it
            movie_year = soup.find("span", {"id": "titleYear"}).text
            title = title.replace(movie_year, "")
        except AttributeError:
            pass
        movie_info["title"] = title
        movie_info["description"] = soup.find("div", {"class": "summary_text"}).get_text(strip=True)
        print(movie_info)
    except:
        print("Invalid movie page!")


get_movie_info()
