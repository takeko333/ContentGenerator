import os
from dotenv import load_dotenv
from utils import connect_browser, extract, generate, path

if __name__ == "__main__":

    load_dotenv()
    input_dir = os.getenv("INPUT_DIRNAME")
    output_dir = os.getenv("OUTPUT_DIRNAME")

    url_data_path = os.path.join(input_dir, os.getenv("URL_DATA_FILENAME"))
    with open(url_data_path, "r", encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
        print(urls)

    prompt_path = os.path.join(input_dir, os.getenv("PROMPT_DIRNAME"))
    prompt_path = os.path.join(prompt_path, "generate_horror_story_from_reddit_comments.txt")
    with open(prompt_path, "r", encoding='utf-8') as f:
        prompt = f.read()

    used_urls = []
    generated_text_filename = os.getenv("GENERATED_TEXT_FILENAME")
    log_filename = os.getenv("LOG_FILENAME")
    try:
        for url in urls:
            print("処理対象：", url)
            contents = extract.get_text_from_reddit_comments(url)
            save_dir = os.path.join(output_dir, path.get_save_dirname(url))
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, generated_text_filename)
            log_path = os.path.join(save_dir, log_filename)
            with open(log_path, "w", encoding='utf-8') as f:
                f.write(f"URL:\n{url}\n\n")
                f.write(f"CONTENT:\n")
                for i, content in enumerate(contents):
                    text = content[0] # "\n".join(content)
                    generate.generate_txt(
                        connect_browser.page, 
                        prompt + "\n" + text, 
                        save_path.replace(".txt", f"_{str(i).zfill(3)}.txt")
                    )
                    f.write(f"{text}\n")
                    f.write(f"{'-' * 100}\n")
            used_urls.append(url)
    finally:
        print("done.")
        with open(url_data_path, "w", encoding='utf-8') as f:
            for url in urls:
                if url not in used_urls:
                    f.write(f"{url}\n")