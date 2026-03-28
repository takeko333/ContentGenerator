import json
import requests
import wikipedia
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
wikipedia.set_lang("en")

def get_text_from_reddit_post(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(strip=True, separator='\n')
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

get_text_from_wikipedia("https://en.wikipedia.org/wiki/Edward_Mordake")