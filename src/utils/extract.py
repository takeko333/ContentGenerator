import json
import requests
import wikipedia
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) my_reddit_scraper/1.0"
}

wikipedia.set_lang("en")

def get_text_from_reddit_post(url):
    try:
        if url[-1] == "/":
            url += "/"
        response = requests.get(url + ".json", headers=headers)
        data = response.json()
        children = data[0]["data"]["children"]
        text = children[0]["data"]["selftext"]
        return text
    except Exception as e:
        print(f"エラー: {e}")
        return None

def get_text_from_wikipedia(url):
    try:
        title = url.split("/")[4]
        title = title.split("#")[0]
        title = title.split("?")[0]
        title = title.replace("_", " ")
        search_results = wikipedia.search(title)
        if not search_results:
            print("該当するページが見つかりませんでした。")
            return None
        data = wikipedia.page(search_results[0], auto_suggest=False)
        return data.content
    except Exception as e:
        print(f"エラー: {e}")
        return None
