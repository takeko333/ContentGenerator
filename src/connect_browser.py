import os
import time
import atexit
import subprocess
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# 各設定値のロード
load_dotenv()
chrome_path = os.getenv("CHROME_PATH")
port = os.getenv("CHROME_PORT", "9222")
user_data_dir = os.getenv("CHROME_USER_DATA_DIR")

def launch_browser():    
    print(f"Chromeをデバッグモードで起動します...")
    # Chromeをバックグラウンドで起動
    subprocess.Popen([
        chrome_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run", # 初回起動時のセットアップをスキップ
        "--no-default-browser-check"
    ])
    # 起動を待つための待機（PCのスペックに合わせて調整）
    time.sleep(3)

def get_page():
    playwright_manager = sync_playwright().start()
    try:
        browser = playwright_manager.chromium.connect_over_cdp(f"http://localhost:{port}")
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.pages[0] if context.pages else context.new_page()        
        print("接続に成功しました！")
        return playwright_manager, browser, page
    except Exception as e:
        print(f"接続失敗: {e}")
        playwright_manager.stop()
        return None, None, None

def cleanup():
    page.close()
    playwright_manager.stop()

launch_browser()
playwright_manager, browser, page = get_page()
atexit.register(cleanup)
