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

def get_text_from_reddit_comments(url):
    url += ".json"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        comments = group_comments_by_parent(data)
        return comments
    except Exception as e:
        return f"エラー: {e}"

def extract_all_bodies_recursive(data, results):
    """
    特定のコメントツリー（枝）からすべてのbodyを再帰的に回収する
    """
    if isinstance(data, dict):
        if "body" in data:
            results.append("> " + data["body"])
        # replies や children を探索
        for key in ["replies", "children", "data"]:
            if key in data:
                extract_all_bodies_recursive(data[key], results)
    elif isinstance(data, list):
        for item in data:
            extract_all_bodies_recursive(item, results)

def group_comments_by_parent(json_data):
    """
    第2階層（親コメント）単位でリストにまとめる
    """
    grouped_results = []
    # RedditのJSONは通常 [リスティング1, リスティング2] の形式
    # 2番目の要素にコメントが含まれる
    if isinstance(json_data, list) and len(json_data) > 1:
        comments_listing = json_data[1]
    else:
        comments_listing = json_data
    # トップレベルのコメント（children）を取得
    top_level_children = comments_listing.get("data", {}).get("children", [])
    for child in top_level_children:
        parent_branch_bodies = []
        # この親コメントとその配下の全てのbodyを回収
        extract_all_bodies_recursive(child, parent_branch_bodies)        
        if parent_branch_bodies:
            grouped_results.append(parent_branch_bodies)

    return grouped_results

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

