from datetime import datetime

def generate_basename_from_url(url):
    values = url.split("/")
    if "wikipedia.org" in url:
        post_title = values[4]
        return f"wikipedia-{post_title}"
    if "www.reddit.com" in url:
        community = values[4]
        post_title = values[7]
        return f"reddit-{community}-{post_title}"
    return None


def get_save_path_for_txt(url):
    timeinfo = datetime.now().strftime("%Y%m%d%H%M%S")
    basename = generate_basename_from_url(url)
    return f"{timeinfo}-{basename}.txt"

