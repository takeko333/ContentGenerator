import os
import time
import pyperclip
from dotenv import load_dotenv
from . import connect_browser

load_dotenv()
url = os.getenv("GEMINI_URL")
input_selector = os.getenv("GEMINI_INPUT_SELECTER")
img_selector = os.getenv("GEMINI_IMG_SELECTER")
txt_selector = os.getenv("GEMINI_TXT_SELECTER")

def generate_txt(target_page, input_text, save_path="output.txt"):
    try:
        target_page.goto(url)
        target_page.wait_for_selector(input_selector, timeout=10000)
        target_page.fill(input_selector, input_text)
        target_page.keyboard.press("Enter")
        last_text = ""
        stable_count = 0
        for _ in range(60):
            time.sleep(1)
            elements = target_page.query_selector_all(txt_selector)
            if elements:
                current_text = elements[-1].inner_text()
                if current_text == last_text and len(current_text) > 0:
                    stable_count += 1
                else:
                    stable_count = 0
                last_text = current_text
                if stable_count >= 5:
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(last_text)
                    print(f"テキスト保存完了: {save_path}")
                    return
        print("タイムアウトまたは生成失敗")
    except Exception as e:
        print(f"操作失敗: {e}")

def generate_img(target_page, input_text, save_path="output.png"):
    try:
        target_page.goto(url)
        target_page.wait_for_selector(input_selector, timeout=10000)
        target_page.fill(input_selector, input_text)
        target_page.keyboard.press("Enter")
        target_page.wait_for_selector(img_selector, timeout=90000)
        time.sleep(3)
        images = target_page.query_selector_all(img_selector)
        if not images:
            print("画像が見つかりませんでした。")
            return
        img_handle = images[0]
        src = img_handle.get_attribute("src")
        if src:
            new_page = target_page.context.new_page()
            try:
                response = new_page.goto(src)
                if response and response.status == 200:
                    buffer = response.body()
                    with open(save_path, "wb") as f:
                        f.write(buffer)
                    print(f"画像保存完了: {save_path}")
            finally:
                new_page.close()
        return
    except Exception as e:
        print(f"操作失敗: {e}")

