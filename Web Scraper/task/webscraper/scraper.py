import requests


def write_page_to_file():
    url = input("Input the URL:\n")
    r = requests.get(url)
    status_code = r.status_code

    if status_code == 200:
        with open("source.html", "wb") as f:
            f.write(r.content)
        print("Content saved.")

    else:
        print(f"The URL returned {status_code}!")


write_page_to_file()
