import os
from dotenv import load_dotenv
from utils import extract
from utils import connect_browser
from utils import generate
from utils import path

load_dotenv()
urls_path = os.getenv("TARGET_URLS_PATH")
prompt_dir = os.getenv("PROMPT_DIR")
result_dir = os.getenv("RESULT_DIR")

if __name__ == "__main__":

    with open(urls_path, "r", encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
        print(urls)

    prompt_path = os.path.join(prompt_dir, "generate_text_from_wikipedia.txt")
    with open(prompt_path, "r", encoding='utf-8') as f:
        prompt = f.read()

    for url in urls:
        print("処理対象：", url)
        content = extract.get_text_from_wikipedia(url)
        save_path = os.path.join(result_dir, path.get_save_path_for_txt(url))
        generate.generate_txt(
            connect_browser.page, 
            prompt + "\n" + content, 
            save_path
        )