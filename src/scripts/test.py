from glob import glob

path_list = glob("inputs/text-to-speech/*")
print(path_list)

import os
from pathlib import Path

original_path = path_list[-1]
clean_path = original_path.strip()

print(f"--- Debug Info ---")
print(f"Raw path (repr): {repr(original_path)}") # 改行があれば \n が見える
print(f"Is link?       : {os.path.islink(clean_path)}")
print(f"Path exists?   : {os.path.exists(clean_path)}")

if os.path.islink(clean_path):
    print(f"Link points to : {os.readlink(clean_path)}") # リンク先を表示
print(f"------------------")

# これで試してみてください
with open(clean_path, "r", encoding="utf-8") as f:
    content = f.read()