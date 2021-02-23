import requests


def get_quote():
    url = input("Input the URL:\n")
    r = requests.get(url)
    try:
        print(r.json()["content"])
    except:
        print("Invalid quote resource!")


get_quote()
